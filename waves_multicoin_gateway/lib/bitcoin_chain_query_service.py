"""
BitcoinChainQueryService
"""

import waves_gateway as gw
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from typing import List, Optional
import gevent.pool as pool

from decimal import Decimal

from waves_gateway import Transaction

from .util import sum_unspents


class BitcoinChainQueryService(gw.ChainQueryService):
    """
    Implementation of an ChainQueryService on the Bitcoin Blockchain.
    """

    def __init__(self, proxy: AuthServiceProxy) -> None:
        self.proxy = proxy

    def get_transaction_by_tx(self, tx: str) -> Optional[Transaction]:
        try:
            return self.get_transaction(tx)
        except JSONRPCException:
            raise gw.InvalidTransactionIdentifier()

    def _extract_receivers(self, transaction: dict) -> List[gw.TransactionReceiver]:
        """Extracts the receivers of an unparsed transaction."""
        results = list()  # type: List[gw.TransactionReceiver]

        for vout in transaction['vout']:
            if 'addresses' not in vout['scriptPubKey']:
                continue

            for address in vout['scriptPubKey']['addresses']:
                transaction_receiver = gw.TransactionReceiver(address=address, amount=vout['value'])
                results.append(transaction_receiver)

        return results

    def _filter_sender_duplicates(self, senders: List[gw.TransactionSender]) -> List[gw.TransactionSender]:
        results = list()  # type: List[gw.TransactionSender]

        for sender in senders:
            if sender not in results:
                results.append(sender)

        return results

    def _resolve_senders(self, transaction: dict) -> List[gw.TransactionSender]:
        """Extracts the senders of an unparsed transaction"""

        if 'vin' not in transaction:
            return list()

        results = list()  # type: List[gw.TransactionSender]

        for vin in transaction['vin']:

            if ('txid' not in vin) or ('vout' not in vin):
                continue

            vin_transaction_raw = self.proxy.getrawtransaction(vin['txid'])
            vin_transaction = self.proxy.decoderawtransaction(vin_transaction_raw)

            if 'addresses' not in vin_transaction['vout'][vin['vout']]['scriptPubKey']:
                continue

            for address in vin_transaction['vout'][vin['vout']]['scriptPubKey']['addresses']:
                transaction_sender = gw.TransactionSender(address=address)
                results.append(transaction_sender)

        return self._filter_sender_duplicates(results)

    def get_transaction(self, tx: str) -> gw.Transaction:
        raw_transaction = self.proxy.getrawtransaction(tx)
        transaction = self.proxy.decoderawtransaction(raw_transaction)

        transaction_receivers = self._extract_receivers(transaction)
        transaction_sender = self._resolve_senders(transaction)

        return gw.Transaction(tx, transaction_receivers, transaction_sender)

    def get_transactions_of_block_at_height(self, height: gw.CoinBlockHeight) -> List[gw.Transaction]:
        block_hash = self.proxy.getblockhash(height)
        block = self.proxy.getblock(block_hash)

        get_transaction_tasks = pool.Pool()  # bitcoin based server's does not accept more than one parallel connection

        return [a for a in get_transaction_tasks.map(self.get_transaction, block['tx'])]

    def get_amount_of_transaction(self, transaction: str) -> Decimal:
        transaction = self.proxy.gettransaction(transaction)
        return transaction['amount']  # type: ignore

    def get_height_of_highest_block(self) -> gw.CoinBlockHeight:
        blocks = self.proxy.getblockcount()
        return blocks
