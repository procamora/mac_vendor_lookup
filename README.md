Mac Vendor Lookup
=================

This is a fork of [https://github.com/bauerj/mac_vendor_lookup][bauerj]. It has been modified to allow synchronous and asynchronous requests.

[bauerj]: https://github.com/bauerj/mac_vendor_lookup

This library provides an easy way to get vendor information from a MAC address. It downloads a local copy of the IEEE's
OUI prefix list. It has an asynchronous interface using Python 3's asyncio as well as a regular synchronous interface
for old-school usage.

## Installation

    pip install mac-vendor-lookup

## Basic Usage

```python
from mac_vendor_lookup_sync import MacLookup

print(MacLookup().lookup("00:80:41:12:FE"))
```

Output:

> VEB KOMBINAT ROBOTRON

## Pre-load the vendor list

The list of MAC vendors is currently about 4MB large. By default a lazy-loading mechanism is used,
that loads the list when it's needed. If it is clear that the list is needed and a wait time during the 
query is not desired, the list can also be loaded when the program is started:

### synchronous

```python
from mac_vendor_lookup_sync import MacLookup

mac = MacLookup()
mac.load_vendors()  # <- This can take a few seconds for the first download
    
def find_mac(mac_address):
    print(mac.lookup(mac_address))  # <- this will only take a few µs!
```


### asynchronous

```python
from mac_vendor_lookup_async import MacLookup

mac = MacLookup()
mac.load_vendors()  # <- This can take a few seconds for the first download
    
def find_mac(mac_address):
    print(mac.lookup(mac_address))  # <- this will only take a few µs!
```

## Interface

There is also an asynchronous interface available:

### synchronous


```python
from mac_vendor_lookup_sync import SyncMacLookup

async def main():
    mac = SyncMacLookup()
    print(mac.lookup("98:ED:5C:FF:EE:01"))
```

### asynchronous


```python
from mac_vendor_lookup_async import AsyncMacLookup

async def main():
    mac = AsyncMacLookup()
    print(await mac.lookup("98:ED:5C:FF:EE:01"))
```

Output:

> Tesla Motors, Inc

## Command line interface

This library provides a rudimentary command line interface:

```bash
$ mac_vendor_lookup 50-D3-7F-00-01-00
Yu Fly Mikly Way Science and Technology Co., Ltd.
$ python3 -m mac_vendor_lookup 00:26:12:12:FE
Space Exploration Technologies
```
