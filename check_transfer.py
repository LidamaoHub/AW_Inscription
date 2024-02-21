from web3 import Web3
import json,time,sys
import pymongo
from tools import rmanager,is_valid_tx,is_valid_memo,mint,deploy,transfer,share_mining_reward
from statics import rpc_url,scan_start_block,block_range,mine_block_count,increase_count

client = pymongo.MongoClient("mongodb://localhost/", 27017)

table = client.game_test
tx_db = table.txs
user_balance_db = table.user_calc
bad_db = table.bads
block_db = table.blocks
tick_db = table.ticks
valid_tx_db = table.valid_txs
user_increase_db = table.increases

waiting_blocks = 120

w3 = Web3(Web3.HTTPProvider(rpc_url))

def main():
    latest_block_number = w3.eth.blockNumber-waiting_blocks
    l = {}
    l2 = []
    un_deal_txs = list(user_balance_db.find({"state":"pending","block_height":{"$lt":latest_block_number}}))
    len_a = len(un_deal_txs)
    un_deal_amts = [x['amt'] for x in un_deal_txs]
    


    un_deal_hashs = [x for x in un_deal_txs if x['amt']>0]
    if len_a != 2*len(un_deal_hashs):
        sys.exit()
    total = sum(un_deal_amts)
    if total != 0:
        sys.exit()
    for tx in un_deal_hashs:
        transaction_hash = tx['hash']
        if check(transaction_hash,latest_block_number):
            user_balance_db.update_many({"hash":transaction_hash},{"$set":{"state":"success"}})
        else:
            sys.exit()

def check(transaction_hash,now_heigh):
    tx_receipt = w3.eth.getTransactionReceipt(transaction_hash)
    if tx_receipt is not None and tx_receipt.blockNumber is not None:
        return True
    else:
        return False



while True:
    main()
    time.sleep(10)