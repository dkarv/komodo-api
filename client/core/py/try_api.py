from komodo_api.lib import KomodoClient, ApiKeyInitOptions
from komodo_api.types import *
import asyncio

async def main():
    api = KomodoClient(
        # url = "https://echo.free.beeceptor.com",
        url = "https://komodo.dino.haus/",
                       options = ApiKeyInitOptions(
                           key = "K-pexdwoiJkNVD0kq58bREGLatSYJT6Wb67ujw9CVd",
                           secret = "S-b5b2jL1URlNe3XnMgnDyk1RvWeLbelkVoBzk6Ovw",
                       ))

    print(await api.auth.getUser(GetUser()))
    print(await api.auth.getLoginOptions(GetLoginOptions()))
    print(await api.read.listServers(ListServers()))
    print(await api.read.listStacks(ListStacks()))
    print(await api.read.listUpdates(ListUpdates()))
    print(await api.read.listAlerts(ListAlerts()))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
