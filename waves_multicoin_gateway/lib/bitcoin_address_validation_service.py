"""
BitcoinAddressValidationService
"""

import waves_gateway as wg
from bitcoinrpc.authproxy import AuthServiceProxy


class BitcoinAddressValidationService(wg.AddressValidationService):
    """
    Validates an Bitcoin address by using an RPC service.
    """

    def __init__(self, proxy: AuthServiceProxy) -> None:
        self.proxy = proxy

    def validate_address(self, address: str) -> bool:
        validation_result = self.proxy.validateaddress(address)
        return validation_result['isvalid']
