"""GatewayConfigParser"""

from configparser import ConfigParser
from decimal import Decimal
from typing import Union, Optional
from waves_gateway.common import Injectable, KeyPair, InvalidConfigError
from waves_gateway.model import GatewayConfigFile


@Injectable()
class GatewayConfigParser(object):
    """
    May be used to parse a gateway configuration file.
    """

    def _parse_node_section(self, config_parser: ConfigParser, parsed_config: GatewayConfigFile) -> None:
        parsed_config.waves_node = config_parser.get('node', 'waves')
        parsed_config.coin_node = config_parser.get('node', 'coin')

    def _parse_number(self, config: ConfigParser, section: str, option: str) -> Union[int, Decimal]:
        """Parses a number field to an int or Decimal."""
        value = config.get(section, option)  # type: str
        if '.' in value:
            return Decimal(value)
        else:
            return int(value)

    def _parse_fee_section(self, config_parser: ConfigParser, parsed_config: GatewayConfigFile) -> None:
        parsed_config.coin_fee = self._parse_number(config_parser, 'fee', 'coin')
        parsed_config.gateway_fee = self._parse_number(config_parser, 'fee', 'gateway')

    def _parse_gateway_address_section(self, config_parser: ConfigParser, parsed_config: GatewayConfigFile):
        parsed_config.gateway_owner_address = config_parser.get('gateway_address', 'owner')

        gateway_waves_address_public_key = config_parser.get('gateway_address', 'waves_public_key')
        gateway_waves_address_private_key = config_parser.get('gateway_address', 'waves_private_key')
        gateway_coin_address_public_key = config_parser.get('gateway_address', 'coin_public_key')
        gateway_coin_address_private_key = config_parser.get(
            'gateway_address', 'coin_private_key', fallback=None)  # type: Optional[str]

        parsed_config.gateway_waves_address_secret = KeyPair(
            public=gateway_waves_address_public_key, secret=gateway_waves_address_private_key)
        parsed_config.gateway_coin_address_secret = KeyPair(
            public=gateway_coin_address_public_key, secret=gateway_coin_address_private_key)

    def _parse_mongodb_section(self, config_parser: ConfigParser, parsed_config: GatewayConfigFile) -> None:
        parsed_config.mongo_host = config_parser.get('mongodb', 'host')
        parsed_config.mongo_port = config_parser.getint('mongodb', 'port')
        parsed_config.mongo_database = config_parser.get('mongodb', 'database')

    def _parse_other_section(self, config_parser: ConfigParser, parsed_config: GatewayConfigFile) -> None:
        parsed_config.waves_chain = config_parser.get('other', 'waves_chain', fallback="mainnet")
        parsed_config.waves_chain_id = config_parser.get('other', 'waves_chain_id', fallback=None)
        parsed_config.waves_asset_id = config_parser.get('other', 'waves_asset_id', fallback=None)
        parsed_config.environment = config_parser.get('other', 'environment', fallback="prod")

    def _parse_server_section(self, config_parser: ConfigParser, parsed_config: GatewayConfigFile):
        parsed_config.gateway_host = config_parser.get('server', 'host', fallback='localhost')
        parsed_config.gateway_port = config_parser.getint('server', 'port', fallback=5000)

    def _parse_coin_section(self, config_parser: ConfigParser, parsed_config: GatewayConfigFile):
        parsed_config.coin_name = config_parser.get('coin', 'name')
        parsed_config.coin_factor = config_parser.get('coin', 'factor')
        parsed_config.coin_precision = config_parser.get('coin', 'precision')

    def _parse_explorer_section(self, config_parser: ConfigParser, parsed_config: GatewayConfigFile):
        parsed_config.transaction_explorer_link = config_parser.get('explorer', 'transaction_link')
        parsed_config.address_explorer_link = config_parser.get('explorer', 'address_link')

    def parse_config_file_content(self, file_content: str) -> GatewayConfigFile:
        """Parses the given config file."""
        config_parser = ConfigParser()
        config_parser.read_string(file_content)
        parsed_config = GatewayConfigFile()

        self._parse_node_section(config_parser, parsed_config)
        self._parse_fee_section(config_parser, parsed_config)
        self._parse_gateway_address_section(config_parser, parsed_config)
        self._parse_mongodb_section(config_parser, parsed_config)
        self._parse_other_section(config_parser, parsed_config)
        self._parse_server_section(config_parser, parsed_config)
        self._parse_coin_section(config_parser, parsed_config)
        self._parse_explorer_section(config_parser, parsed_config)
        return parsed_config

    @staticmethod
    def parse_config_file(file):
        """First reads the config file and then calls parse_config_file_content with the content."""
        config = GatewayConfigParser()
        return config.parse_config_file_content(file.read())
