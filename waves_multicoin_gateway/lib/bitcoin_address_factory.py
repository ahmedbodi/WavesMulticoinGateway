"""
BitcoinAddressFactory
"""

import waves_gateway as gw
from bitcoinrpc.authproxy import AuthServiceProxy


class BitcoinAddressFactory(gw.CoinAddressFactory):
    """
    Implements an AddressFactory using the getnewaddress function provided by the Bitcoin client.
    """

    def __init__(self, proxy: AuthServiceProxy) -> None:
        self.proxy = proxy

    def create_address(self) -> gw.CoinAddress:
        return self.proxy.getnewaddress()
