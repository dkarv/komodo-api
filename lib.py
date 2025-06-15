import asyncio
import json
import websockets
from typing import Any, Callable, Dict, Optional, Union

class CancelToken:
    def __init__(self):
        self.cancelled = False

    def cancel(self):
        self.cancelled = True


class KomodoClient:
    def __init__(self, url: str, options: Dict[str, Any]):
        self.url = url
        self.options = options
        self.state = {
            "jwt": options["params"]["jwt"] if options["type"] == "jwt" else None,
            "key": options["params"]["key"] if options["type"] == "api-key" else None,
            "secret": options["params"]["secret"] if options["type"] == "api-key" else None,
        }

    async def request(self, path: str, type_: str, params: Dict[str, Any]) -> Any:
        headers = {
            "content-type": "application/json",
            **({"authorization": self.state["jwt"]} if self.state["jwt"] else {}),
            **(
                {
                    "x-api-key": self.state["key"],
                    "x-api-secret": self.state["secret"],
                }
                if self.state["key"] and self.state["secret"]
                else {}
            ),
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.url}{path}/{type_}", json=params, headers=headers
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Request failed with status {response.status}")

    async def auth(self, type_: str, params: Dict[str, Any]) -> Any:
        return await self.request("/auth", type_, params)

    async def user(self, type_: str, params: Dict[str, Any]) -> Any:
        return await self.request("/user", type_, params)

    async def read(self, type_: str, params: Dict[str, Any]) -> Any:
        return await self.request("/read", type_, params)

    async def write(self, type_: str, params: Dict[str, Any]) -> Any:
        return await self.request("/write", type_, params)

    async def execute(self, type_: str, params: Dict[str, Any]) -> Any:
        return await self.request("/execute", type_, params)

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