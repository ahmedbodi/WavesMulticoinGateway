"""
BaseGateway
"""

import logging
from logging.handlers import RotatingFileHandler
from typing import List

import bitcoinrpc.authproxy as authproxy
import pymongo
import waves_gateway as wg
import waves_multicoin_gateway.lib as lib

class BaseGateway(object):

    def __init__(self, config: wg.GatewayConfigFile) -> None:
        # Setup What we can here
        self.mongo_client = pymongo.MongoClient(host=config.mongo_host, port=config.mongo_port)
        self.fee_service = wg.ConstantFeeServiceImpl(config.gateway_fee, config.coin_fee)
        self.config = config

        # These should be done in the child classes
        self.proxy = None
        self.address_factory = None
        self.chain_query_service = None
        self.transaction_service = None
        self.integer_converter_service = None
        self.address_validation_service = None
        self.logging_handlers = None
        self.gateway = None


    def _init_logging_handlers(self, environment: str) -> List[logging.Handler]:
        formatter = logging.Formatter("[%(asctime)s] %(levelname)s {%(name)s} - %(message)s")
        logging_handlers = []  # type: List[logging.Handler]

        if environment == "prod":
            file_handler = RotatingFileHandler(config.logfile_name, maxBytes=10485760, backupCount=20, encoding='utf8')
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)
            logging_handlers.append(file_handler)

            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.WARN)
            stream_handler.setFormatter(formatter)
            logging_handlers.append(stream_handler)
        elif environment == "debug":
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            stream_handler.setFormatter(formatter)
            logging_handlers.append(stream_handler)
        elif environment == "test":
            pass
        else:
            raise Exception('Unknown environment ' + environment + '. Use prod or debug')

        return logging_handlers

    def run(self):
        self.gateway.run()

    def set_log_level(self, level):
        self.gateway.set_log_level(level)
