from web3 import Web3
import json,time
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



# connect ethereum rpc

w3 = Web3(Web3.HTTPProvider(rpc_url))



def main():
    latest_block_number = w3.eth.blockNumber-30
    print("Latest block:",latest_block_number)
    block = block_db.find_one({"state":True,'tick':"GAME"})

    if block:
        s = scan_start_block if block['block_height']<scan_start_block else (block['block_height']+1)
        range_ = range(s,latest_block_number)
    else:
        range_ = range(scan_start_block,latest_block_number)
        block_db.update_one({'state':True,'tick':"GAME"},{"$set":{"block_height":scan_start_block,"reward_block_height":scan_start_block}},upsert=True)
    for block_height in range_:
        t1 = time.time()
        get_block_info(block_height,latest_block_number)
        t2 = time.time()
        d = t2-t1
        if d>1:
            print(f"finishe the tx {block_height} need:{t2-t1}")
    time.sleep(10)


def get_block_info(block_height,latest_block_number):
    rmanager.clear_list(str(block_height))
    block = w3.eth.getBlock(block_height, full_transactions=True)
    txs = [tx for tx in block.transactions if is_valid_tx(tx)]
    valid_tx_db.update_one(
        {"block_height":block_height},
        {"$set":{"tx_amount":len(block.transactions),"valid_tx_amount":len(txs)}},
        upsert=True
    )
    for tx in txs:
        json_str = bytes.fromhex(tx.input[2:]).decode('utf-8')
        json_data = json.loads(json_str)

        from_address = tx['from']
        to_address = tx['to']
        block_height = tx['blockNumber']
        block_hash = tx ['hash'].hex()
        manage_memo(json_data,from_address,to_address,block_height,block_hash)

    if block_height%block_range==0:
        share_mining_reward(block_height)
    if block_height%increase_count==0:
        tick_name = "GAME"
        count = len(user_balance_db.distinct("address",
            {"block_height":{"$lt":block_height}}))
        user_increase_db.update_one({"block_height":block_height,"tick":tick_name},{"$set":{"count":count}},upsert=True)


    block_db.update_one({'state':True},{"$set":{"block_height":int(block_height)}})

        

def manage_memo(memo,from_address,to_address,block_height,block_hash):
    from_address = from_address.lower()
    to_address = to_address.lower()
    tx_info = {"from_address":from_address,"to_address":to_address,'block_height':block_height,"hash":block_hash}
    tick_name = memo['tick'].strip().upper()
    op = memo['op']
    t = int(time.time())
    tick_info = tick_db.find_one({"tick":tick_name})
    if tick_info:
        if op == 'mint':
            mint(tick_info,memo,tx_info)
        elif op == 'transfer':
            transfer(tick_info,memo,tx_info)
        else:
            print(f"bad op:{memo}")
    else:
        if op == 'deploy' and tick_name=="GAME":
            deploy(memo,tx_info)
        else:
            print(f"{tick_name} didn't deployed")



  
while True:
    main()

