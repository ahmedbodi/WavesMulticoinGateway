"""
BitcoinGateway
"""

import logging
from logging.handlers import RotatingFileHandler
from typing import List

import bitcoinrpc.authproxy as authproxy
import pymongo
import waves_gateway as wg
import waves_multicoin_gateway.lib as lib
from .base_gateway import BaseGateway

class BitcoinGateway(BaseGateway):
    """
    Implements an BTC Gateway.
    """

    def __init__(self, config: wg.GatewayConfigFile) -> None:
        print(dir(config))
        super(BitcoinGateway, self).__init__(config)
        self.proxy = wg.ProxyGuard(authproxy.AuthServiceProxy(config.coin_node), max_parallel_access=1)
        self.address_factory = lib.BitcoinAddressFactory(self.proxy)
        self.chain_query_service = lib.BitcoinChainQueryService(self.proxy)
        self.transaction_service = lib.BitcoinTransactionService(self.proxy, self.chain_query_service)
        self.integer_converter_service = lib.BitcoinIntegerConverterService(config.coin_factor, config.coin_precision)
        self.address_validation_service = lib.BitcoinAddressValidationService(self.proxy)

        self.gateway = wg.Gateway(
            coin_address_factory = self.address_factory,
            coin_chain_query_service = self.chain_query_service,
            coin_transaction_service = self.transaction_service,
            gateway_waves_address_secret = config.gateway_waves_address_secret,
            gateway_coin_address_secret = config.gateway_coin_address_secret,
            mongo_database = self.mongo_client.get_database(config.mongo_database),
            managed_loggers = ["BitcoinRPC"],
            logging_handlers = self.logging_handlers,
            custom_currency_name = config.coin_name,
            coin_integer_converter_service = self.integer_converter_service,
            asset_integer_converter_service = wg.IntegerConverterService(),
            waves_chain = config.waves_chain,
            waves_asset_id = config.waves_asset_id,
            waves_node = config.waves_node,
            gateway_owner_address = config.gateway_owner_address,
            fee_service = self.fee_service,
            only_one_transaction_receiver = False,
            coin_transaction_web_link = config.transaction_explorer_link,
            coin_address_web_link = config.address_explorer_link,
            host = config.gateway_host,
            port = config.gateway_port,
            coin_address_validation_service = self.address_validation_service,
            coin_last_block_distance=5)

