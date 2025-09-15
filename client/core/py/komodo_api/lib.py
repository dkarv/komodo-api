from .responses import (
    AuthApi,
    ExecuteApi,
    ReadApi,
    UserApi,
    WriteApi,
)

from .types import (
    AuthRequest,
    ExecuteRequest,
    ReadRequest,
    UserRequest,
    WriteRequest,
    WsLoginMessage,
)

from .exceptions import KomodoException

import aiohttp
import asyncio
import json
from typing import Any, Callable, Dict, Optional, Union, TypeVar
from enum import Enum
from pydantic import TypeAdapter
import logging

_logger = logging.getLogger(__name__)

class InitOptions:
    type_: str


class JwtInitOptions(InitOptions):
    type_: str = "jwt"
    jwt: str

    def __init__(self, jwt: str):
        self.jwt = jwt


class ApiKeyInitOptions(InitOptions):
    type_: str = "api-key"
    key: str
    secret: str

    def __init__(self, key: str, secret: str):
        self.key = key
        self.secret = secret


class CancelToken:
    def __init__(self):
        self.cancelled = False

    def cancel(self):
        self.cancelled = True


class KomodoClient(AuthApi):
    auth: AuthApi
    read: ReadApi
    write: WriteApi
    user: UserApi
    execute: ExecuteApi
    url: str
    _session: aiohttp.ClientSession

    def __init__(self, url: str, options: InitOptions):
        self.url = url
        headers = {
            "content-type": "application/json",
            **({"authorization": options.jwt} if options.type_ == "jwt" else {}),
            **(
                {
                    "x-api-key": options.key,
                    "x-api-secret": options.secret,
                }
                if options.type_ == "api-key"
                else {}
            ),
        }
        self._session = aiohttp.ClientSession(headers=headers)

        self.auth = AuthApi(self.request)
        self.read = ReadApi(self.request)
        self.write = WriteApi(self.request)
        self.user = UserApi(self.request)
        self.execute = ExecuteApi(self.request)

    async def __aenter__(self):
        return self

    async def __aexit__(self, *err):
        await self.close()

    async def close(self):
        await self._session.close()

    Req = TypeVar("Req")
    Res = TypeVar("Res")

    async def request(self, path: str, request: Req, clz: type[Res]) -> Res:
        async with self._session.post(
            f"{self.url}{path}",
            data=request.model_dump_json(exclude_none=True),
        ) as response:
            if response.status == 200:
                text = await response.text()
                _logger.debug(f"Response: {text}")
                try:
                    return TypeAdapter(clz).validate_json(text)
                except Exception as e:
                    raise Exception(
                        f"Failed to parse response: {e}\nResponse text: {text}"
                    )
            else:
                error = await response.json()
                _logger.warning(f"Api error {error}")
                raise KomodoException(error, response.status)

    # CAUTION: completely untested!
    async def poll_update_until_complete(self, update_id: str) -> Any:
        while True:
            await asyncio.sleep(1)
            update = await self.read("GetUpdate", {"id": update_id})
            if update["status"] == "Complete":
                return update

    # CAUTION: completely untested!
    async def execute_and_poll(self, type_: str, params: Dict[str, Any]) -> Any:
        res = await self.execute(type_, params)
        if isinstance(res, list):
            return await asyncio.gather(
                *[
                    self.poll_update_until_complete(item["data"]["_id"]["$oid"])
                    for item in res
                    if item["status"] != "Err"
                ]
            )
        else:
            return await self.poll_update_until_complete(res["_id"]["$oid"])

    # CAUTION: completely untested!
    async def core_version(self) -> str:
        res = await self.read("GetVersion", {})
        return res["version"]

    # CAUTION: completely untested!
    async def get_update_websocket(
        self,
        on_update: Callable[[Dict[str, Any]], None],
        on_login: Optional[Callable[[], None]] = None,
        on_open: Optional[Callable[[], None]] = None,
        on_close: Optional[Callable[[], None]] = None,
    ):
        async with websockets.connect(
            self.url.replace("http", "ws") + "/ws/update"
        ) as ws:
            if on_open:
                on_open()
            login_msg = (
                {"type": "Jwt", "params": {"jwt": self.options["params"]["jwt"]}}
                if self.options["type"] == "jwt"
                else {
                    "type": "ApiKeys",
                    "params": {
                        "key": self.options["params"]["key"],
                        "secret": self.options["params"]["secret"],
                    },
                }
            )
            await ws.send(json.dumps(login_msg))
            async for message in ws:
                if message == "LOGGED_IN":
                    if on_login:
                        on_login()
                else:
                    on_update(json.loads(message))
            if on_close:
                on_close()

    # CAUTION: completely untested!
    async def subscribe_to_update_websocket(
        self,
        on_update: Callable[[Dict[str, Any]], None],
        on_login: Optional[Callable[[], None]] = None,
        on_open: Optional[Callable[[], None]] = None,
        on_close: Optional[Callable[[], None]] = None,
        retry: bool = True,
        retry_timeout_ms: int = 5000,
        cancel: CancelToken = CancelToken(),
        on_cancel: Optional[Callable[[], None]] = None,
    ):
        while not cancel.cancelled:
            try:
                await self.get_update_websocket(on_update, on_login, on_open, on_close)
            except Exception as e:
                print(f"WebSocket error: {e}")
                if retry:
                    await asyncio.sleep(retry_timeout_ms / 1000)
                else:
                    break
        if cancel.cancelled and on_cancel:
            on_cancel()
