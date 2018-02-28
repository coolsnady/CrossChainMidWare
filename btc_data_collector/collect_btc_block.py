#!/usr/bin/env python
# encoding=utf8

__author__ = 'hasee'

######################################################################
#  数据处理逻辑：
#  1. 先从数据库中获取出上次采集已成功提交的区块号
#  2. 采集前清理掉超出此区块号的tbl_block, tbl_transaction, tbl_transaction_ex, tbl_contract_info表中相关记录
#  3. 考虑到对同一个合约的操作，可能会有并发问题导致的合约操作的先后顺序颠倒的问题，
#       对于tbl_contract_info表，采用replace into ON DUPLICATE的方式
#  4. 对于tbl_contract_abi, tbl_contract_storage, tbl_contract_event表，在遇到注册相关合约相关的交易的处理上，
#       先清理，再插入
######################################################################



import logging
import sys
import traceback

from collector_conf import BTCCollectorConfig
from wallet_api import WalletApi
import time
from block_btc import BlockInfoBtc
from datetime import datetime
from coin_tx_collector import CoinTxCollecter




class BTCCoinTxCollecter(CoinTxCollecter):
    def __init__(self, db):
        super(BTCCoinTxCollecter, self).__init__()
        self.db = db
        self.t_multisig_address = self.db.b_btc_multisig_address
        self.last_sync_block_num = 0
        self.sync_start_per_round = 0
        self.sync_end_per_round = 0
        self.sync_limit_per_step = 10
        self.config = BTCCollectorConfig()
        conf = {"host": self.config.RPC_HOST, "port": self.config.RPC_PORT}
        self.wallet_api = WalletApi(self.config.ASSET_SYMBOL, conf)

    def do_collect_app(self):
        while True:
            try:
                #程序启动，设置为同步状态
                config_db = self.db.b_config
                config_db.update({"key": self.config.SYNC_STATE_FIELD},
                                 {"key": self.config.SYNC_STATE_FIELD, "value": "true"})

                # 清理上一轮的垃圾数据，包括块数据、交易数据以及合约数据
                self.last_sync_block_num = self.clear_last_garbage_data(self.db)

                # 获取当前链上最新块号
                while True:
                    latest_block_num = self.get_latest_block_num()
                    logging.debug("latest_block_num: %d, last_sync_block_num: %d" % (latest_block_num, self.last_sync_block_num))
                    if self.last_sync_block_num >= latest_block_num:
                        self.sync_start_per_round = latest_block_num
                        self.sync_end_per_round = latest_block_num
                    else:
                        self.sync_start_per_round = self.last_sync_block_num
                        self.sync_end_per_round = ((
                                self.last_sync_block_num + self.config.SYNC_BLOCK_PER_ROUND) >= latest_block_num) \
                                and latest_block_num or (self.last_sync_block_num + self.config.SYNC_BLOCK_PER_ROUND)
                    logging.debug("This round start: %d, this round end: %d" % (self.sync_start_per_round, self.sync_end_per_round))

                    sync_rate = float(self.sync_start_per_round) / latest_block_num
                    sync_process = '#' * int(40 * sync_rate) + ' ' * (40 - int(40 * sync_rate))
                    sys.stdout.write(
                        "\rsync block [%s][%d/%d], %.3f%%\n" % (sync_process, self.sync_start_per_round,
                                                              latest_block_num, sync_rate * 100))
                    while self.sync_start_per_round <= self.sync_end_per_round:
                        logging.debug("Start collect step from %d" % self.sync_start_per_round)
                        self.collect_data_cb(self.db)
                        self.last_sync_block_num = self.sync_start_per_round
                        config_db.update({"key": self.config.SYNC_BLOCK_NUM}, {"$set":{"key": self.config.SYNC_BLOCK_NUM, "value": str(self.last_sync_block_num)}})

                    if self.sync_start_per_round == latest_block_num + 1:
                        break

                time.sleep(10)

            except Exception, ex:
                logging.info(traceback.format_exc())
                print ex
                # 异常情况，60秒后重试
                time.sleep(60)
                self.do_collect_app()


    def get_latest_block_num(self):
        ret = self.wallet_api.http_request("getblockcount", [])
        real_block_num = ret['result']
        safe_block = 6
        safe_block_ret = self.db.b_config.find_one({"key": self.config.SAFE_BLOCK_FIELD})
        if safe_block_ret is not None:
            safe_block = int(safe_block_ret["value"])

        return int(real_block_num) - safe_block


    def clear_last_garbage_data(self, db_pool):
        ret = db_pool.b_config.find_one({"key": self.config.SYNC_BLOCK_NUM})
        if ret is None:
            return 0
        last_sync_block_num = int(ret["value"])
        try:
            db_pool.b_raw_transaction.remove({"blockNum":{"$gte": last_sync_block_num},"chainId": self.config.ASSET_SYMBOL.lower()})
            db_pool.b_block.remove({"blockNumber":{"$gte": last_sync_block_num},"chainId": self.config.ASSET_SYMBOL.lower()})
            db_pool.b_raw_transaction_input.remove({"blockNum": {"$gte": last_sync_block_num},"chainId": self.config.ASSET_SYMBOL.lower()})
            db_pool.b_raw_transaction_output.remove({"blockNum": {"$gte": last_sync_block_num},"chainId": self.config.ASSET_SYMBOL.lower()})
            db_pool.b_deposit_transaction.remove({"blockNum": {"$gte": last_sync_block_num},"chainId": self.config.ASSET_SYMBOL.lower()})
            db_pool.b_withdraw_transaction.remove({"blockNum": {"$gte": last_sync_block_num},"chainId": self.config.ASSET_SYMBOL.lower()})
        except Exception,ex:
            print ex
        return int(last_sync_block_num)


    #采集块数据
    def collect_block(self, db_pool, block_num_fetch):
        ret1 = self.wallet_api.http_request("getblockhash", [block_num_fetch])
        if ret1['result'] == None:
            raise Exception("blockchain_get_block error")
        block_hash = ret1['result']
        ret2 = self.wallet_api.http_request("getblock", [str(block_hash)])
        if ret2['result'] == None:
            raise Exception("blockchain_get_block error")
        json_data = ret2['result']
        block_info = BlockInfoBtc()
        block_info.from_block_resp(json_data)
        block = db_pool.b_block
        mongo_data = block.find_one({"blockHash":block_info.block_id})

        if mongo_data == None:
            block.insert(block_info.get_json_data())
        else:
            block.update({"blockHash":block_info.block_id},{"$set":block_info.get_json_data()})

        logging.debug("Collect block [num:%d], [block_hash:%s], [tx_num:%d]" % (block_num_fetch, block_hash, len(json_data["tx"])))

        return block_info


    def get_transaction_data(self, trx_id):

        ret = self.wallet_api.http_request("getrawtransaction", [trx_id, True])
        if ret["result"] is None:
            resp_data = None
        else:
            resp_data = ret["result"]
        return resp_data


    def collect_pretty_transaction(self, db_pool, base_trx_data, block_num):
        raw_transaction_db = db_pool.b_raw_transaction
        trx_data = {}
        trx_data["chainId"] = self.config.ASSET_SYMBOL.lower()
        trx_data["trxid"] = base_trx_data["txid"]
        trx_data["blockNum"] = block_num
        vin = base_trx_data["vin"]
        vout = base_trx_data["vout"]
        trx_data["vout"] = []
        trx_data["vin"] = []

        out_set = {}
        in_set = {}
        multisig_in_addr = ""
        multisig_out_addr = ""
        is_valid_tx = True
        logging.debug(base_trx_data)


        """
        Only 3 types of transactions will be filtered out and be record in database.
        1. deposit transaction (vin contains only one no LINK address and vout contains only one LINK address)
        2. withdraw transaction (vin contains only one LINK address and vout contains no other LINK address)
        3. transaction between hot-wallet and cold-wallet (vin contains only one LINK address and vout contains only one other LINK address)

        Check logic:
        1. check all tx in vin and store addresses & values (if more than one LINK address set invalid)
        2. check all tx in vout and store all non-change addresses & values (if more than one LINK address set invalid)
        3. above logic filter out the situation - more than one LINK address in vin or vout but there is one condition
           should be filter out - more than one normal address in vin for deposit transaction
        4. then we can record the transaction according to transaction type
           only one other addres in vin and only one LINK address in vout - deposit
           only one LINK addres in vin and only other addresses in vout - withdraw
           only one LINK addres in vin and only one other LINK address in vout - transaction between hot-wallet and cold-wallet
           no LINK address in vin and no LINK address in vout - transaction that we don't care about, record nothing
        5. record original transaction in raw table if we care about it.
        """
        for trx_in in vin:
            if not trx_in.has_key("txid"):
                continue
            in_trx = self.get_transaction_data(trx_in["txid"])
            if in_trx is None:
                logging.error("Fail to get vin transaction [%s] of [%s]" % (trx_in["txid"], trx_data["trxid"]))
            else:
                logging.debug(in_trx)
                for t in in_trx["vout"]:
                    if t["n"] == trx_in["vout"] and t["scriptPubKey"].has_key("addresses"):
                        in_address = t["scriptPubKey"]["addresses"][0]
                        if (in_set.has_key(in_address)):
                            in_set[in_address] += t["value"]
                        else:
                            in_set[in_address] = t["value"]
                        trx_data["vin"].append({"txid": trx_in["txid"], "vout": trx_in["vout"], "value": t["value"], "address": in_address})
                        if self.t_multisig_address.find_one({"address": in_address, "addr_type": 0}) is not None:
                            if multisig_in_addr == "":
                                multisig_in_addr = in_address
                            else:
                                is_valid_tx = False
                        break

        for trx_out in vout:
            if trx_out["scriptPubKey"].has_key("addresses"):
                out_address = trx_out["scriptPubKey"]["addresses"][0]
                trx_data["vout"].append({"value": trx_out["value"], "n": trx_out["n"], "scriptPubKey": trx_out["scriptPubKey"]["hex"], "address": out_address})
                if in_set.has_key(out_address): # remove change
                    continue
                if (out_set.has_key(out_address)):
                    out_set[out_address] += trx_out["value"]
                else:
                    out_set[out_address] = trx_out["value"]
                if self.t_multisig_address.find_one({"address": out_address, "addr_type": 0}) is not None:
                    if multisig_out_addr == "":
                        multisig_out_addr = out_address
                    else:
                        is_valid_tx = False

        if not multisig_in_addr == "" and not multisig_out_addr == "": # maybe transfer between hot-wallet and cold-wallet
            if not is_valid_tx:
                logging.error("Invalid transaction between hot-wallet and cold-wallet")
                trx_data['type'] = -3
            else:
                trx_data['type'] = 0
        elif not multisig_in_addr == "": # maybe withdraw
            if not is_valid_tx:
                logging.error("Invalid withdraw transaction")
                trx_data['type'] = -1
            else:
                trx_data['type'] = 1
        elif not multisig_out_addr == "": # maybe deposit
            if not is_valid_tx or not len(in_set) == 1:
                logging.error("Invalid deposit transaction")
                trx_data['type'] = -2
            else:
                trx_data['type'] = 2
        else:
            logging.info("Nothing to record")
            return
        trx_data["trxTime"] = datetime.utcfromtimestamp(base_trx_data['time']).strftime("%Y-%m-%d %H:%M:%S")
        trx_data["createtime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if trx_data['type'] == 2 or trx_data['type'] == 0:
            deposit_data = {
                "txid": base_trx_data["txid"],
                "from_account": in_set.keys()[0],
                "to_account": multisig_out_addr,
                "amount": str(out_set.values()[0]),
                "asset_symbol": self.config.ASSET_SYMBOL,
                "blockNum": block_num,
                "chainId": self.config.ASSET_SYMBOL.lower()
            }
            mongo_data = db_pool.b_deposit_transaction.find_one({"txid": base_trx_data["txid"]})
            if mongo_data == None:
                db_pool.b_deposit_transaction.insert(deposit_data)
            else:
                db_pool.b_deposit_transaction.update({"trxid": base_trx_data["txid"]}, {"$set": deposit_data})
        elif trx_data['type'] == 1:
            for k, v in out_set.items():
                withdraw_data = {
                    "txid": base_trx_data["txid"],
                    "from_account": multisig_in_addr,
                    "to_account": k,
                    "amount": str(v),
                    "asset_symbol": self.config.ASSET_SYMBOL,
                    "blockNum": block_num,
                    "chainId": self.config.ASSET_SYMBOL.lower()
                }
                mongo_data = db_pool.b_withdraw_transaction.find_one({"txid": base_trx_data["txid"], "from_account": multisig_in_addr, "to_account": k, "blockNum": block_num})
                if mongo_data == None:
                    db_pool.b_withdraw_transaction.insert(withdraw_data)
                else:
                    db_pool.b_withdraw_transaction.update({"trxid": base_trx_data["txid"], "from_account": multisig_in_addr, "to_account": k, "blockNum": block_num}, {"$set": withdraw_data})

        mongo_data = raw_transaction_db.find_one({"trxid": base_trx_data["txid"]})
        if mongo_data == None:
            raw_transaction_db.insert(trx_data)
        else:
            raw_transaction_db.update({"trxid": base_trx_data["txid"]}, {"$set": trx_data})

        return trx_data


    def update_block_trx_amount(self, db_pool, block_info):
        block = db_pool.b_block
        block.update({"blockHash":block_info.block_id},{"$set" : {"trxamount:":str(block_info.trx_amount),"trxfee":block_info.trx_fee}})


    #采集数据
    def collect_data_cb(self, db_pool):
        try:
            count = 0
            while self.sync_start_per_round <= self.sync_end_per_round and count < self.sync_limit_per_step:
                block_num_fetch = self.sync_start_per_round

                # 采集块
                block_info = self.collect_block(db_pool, block_num_fetch)
                for trx_id in block_info.transactions:
                    # 采集交易
                    base_trx_data = self.get_transaction_data(trx_id)
                    if base_trx_data is None:
                        continue
                    logging.debug("Transaction: %s" % base_trx_data)
                    pretty_trx_info = self.collect_pretty_transaction(db_pool, base_trx_data, block_info.block_num)
                self.sync_start_per_round += 1
                count += 1

            # 连接使用完毕，需要释放连接

        except Exception, ex:
            raise ex
