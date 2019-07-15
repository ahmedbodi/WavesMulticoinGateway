"""
Quebecoin Gateway
"""
import gevent.monkey
gevent.monkey.patch_all()

from waves_multicoin_gateway import BitcoinGateway, GatewayConfigParser
import waves_gateway as wg

file = open("config.cfg", "r")

config = GatewayConfigParser.parse_config_file(file)
gateway = BitcoinGateway(config=config)
gateway.run()
