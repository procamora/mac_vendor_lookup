import asyncio
import logging
import os

import aiofiles
import aiohttp
from procamora_logging.logger import get_logging

logger: logging = get_logging(False, 'mac_lockup')

OUI_URL = "http://standards-oui.ieee.org/oui.txt"


class InvalidMacError(Exception):
    pass


class BaseMacLookup(object):
    cache_path = os.path.expanduser('~/.cache/mac-vendors.txt')

    @staticmethod
    def sanitise(_mac):
        mac = _mac.replace(":", "").replace("-", "").upper()
        try:
            int(mac, 16)
        except ValueError:
            raise InvalidMacError(f"{_mac} contains unexpected character")
        if len(mac) > 12:
            raise InvalidMacError(f"{_mac} is not a valid MAC address (too long)")
        return mac


class AsyncMacLookup(BaseMacLookup):
    def __init__(self):
        self.prefixes = None

    async def update_vendors(self, url=OUI_URL):
        logger.debug("Downloading MAC vendor list")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                async with aiofiles.open(AsyncMacLookup.cache_path, mode='wb') as f:
                    while True:
                        line: bytes = await response.content.readline()
                        print(len(line))
                        print(type(line))
                        if not line:
                            break
                        if b"(base 16)" in line:
                            prefix, vendor = (i.strip() for i in line.split(b"(base 16)", 1))
                            self.prefixes[prefix] = vendor
                            await f.write(prefix + b":" + vendor + b"\n")

    async def load_vendors(self):
        self.prefixes = {}
        if not os.path.exists(AsyncMacLookup.cache_path):
            try:
                os.makedirs("/".join(AsyncMacLookup.cache_path.split("/")[:-1]))
            except OSError:
                pass
            await self.update_vendors()
        else:
            logger.debug("Loading vendor list from cache")
            async with aiofiles.open(AsyncMacLookup.cache_path, mode='rb') as f:
                # Loading the entire file into memory, then splitting is
                # actually faster than streaming each line. (> 1000x)
                for l in (await f.read()).splitlines():
                    prefix, vendor = l.split(b":", 1)
                    self.prefixes[prefix] = vendor
        logger.debug(f"Vendor list successfully loaded: {len(self.prefixes)} entries")

    async def lookup(self, mac):
        mac = self.sanitise(mac)
        if not self.prefixes:
            await self.load_vendors()
        if type(mac) == str:
            mac = mac.encode("utf8")
        return self.prefixes[mac[:6]].decode("utf8")


class MacLookup(BaseMacLookup):
    def __init__(self):
        self.async_lookup = AsyncMacLookup()
        self.loop = asyncio.get_event_loop()

    def update_vendors(self, url=OUI_URL):
        return self.loop.run_until_complete(self.async_lookup.update_vendors(url))

    def lookup(self, mac):
        return self.loop.run_until_complete(self.async_lookup.lookup(mac))

    def load_vendors(self):
        return self.loop.run_until_complete(self.async_lookup.load_vendors())


def main():
    import sys

    loop = asyncio.get_event_loop()
    if len(sys.argv) < 2:
        logger.info(f"Usage: {sys.argv[0]} [MAC-Address]")
        sys.exit()
    try:
        logger.info(loop.run_until_complete(AsyncMacLookup().lookup(sys.argv[1])))
    except KeyError:
        logger.error("Prefix is not registered")
    except InvalidMacError as e:
        logger.error("Invalid MAC address:", e)


if __name__ == "__main__":
    main()
