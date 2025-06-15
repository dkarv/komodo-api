from .responses import (
  AuthApi,
  ExecuteResponses, 
  ReadResponses, 
  UserResponses, 
  WriteResponses,
)

from .types import (
  AuthRequest, 
  BatchExecutionResponse, 
  ConnectContainerExecQuery, 
  ConnectDeploymentExecQuery, 
  ConnectStackExecQuery, 
  ConnectTerminalQuery,
  ExecuteRequest,
  ExecuteTerminalBody,
  ReadRequest,
  Update,
  UpdateListItem,
  UpdateStatus,
  UserRequest,
  WriteRequest,
  WsLoginMessage,
)

import aiohttp
import asyncio
import json
from typing import Any, Callable, Dict, Optional, Union, TypeVar
from enum import Enum

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
  def __init__(self, url: str, options: InitOptions):
    self.url = url
    self.state = options

  Req = TypeVar('Req')
  Res = TypeVar('Res')

  async def request(self, path: str, request: Req, clz: type[Res]) -> Res:
        print(f"Clz: {clz}")
        print(f"Self.Res: {self.Res}")
        headers = {
            "content-type": "application/json",
            **({"authorization": self.state.jwt} if self.state.type_ == "jwt" else {}),
            **(
                {
                    "x-api-key": self.state.key,
                    "x-api-secret": self.state.secret,
                }
                if self.state.type_ == "api-key"
                else {}
            ),
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.url}{path}", data=request.model_dump_json(), headers=headers
            ) as response:
                if response.status == 200:
                    text = await response.text()
                    print(f"Response text: {text}")
                    return clz.model_validate_json(text)
                else:
                    raise Exception(f"Request failed with status {response.status}")

  async def _auth(self, request: AuthRequest, clz: type[Res]) -> Res:
    return await self.request("/auth", request, clz)

#  async def user(self, type_: str, params: Dict[str, Any]) -> Any:
#    return await self.request("/user", params)

#  async def read(self, type_: str, params: Dict[str, Any]) -> Any:
#    return await self.request("/read", params)

#  async def write(self, type_: str, params: Dict[str, Any]) -> Any:
#    return await self.request("/write", params)

#  async def execute(self, type_: str, params: Dict[str, Any]) -> Any:
#    return await self.request("/execute", params)

  async def poll_update_until_complete(self, update_id: str) -> Any:
        while True:
            await asyncio.sleep(1)
            update = await self.read("GetUpdate", {"id": update_id})
            if update["status"] == "Complete":
                return update

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

  async def core_version(self) -> str:
        res = await self.read("GetVersion", {})
        return res["version"]

  async def get_update_websocket(
        self,
        on_update: Callable[[Dict[str, Any]], None],
        on_login: Optional[Callable[[], None]] = None,
        on_open: Optional[Callable[[], None]] = None,
        on_close: Optional[Callable[[], None]] = None,
    ):
        async with websockets.connect(self.url.replace("http", "ws") + "/ws/update") as ws:
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
