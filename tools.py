import redis,json,pymongo,time

from statics import rpc_url,scan_start_block,block_range,mine_block_count


client = pymongo.MongoClient("mongodb://localhost/", 27017)

table = client.game_test
bad_db = table.bads
# user_balance_db = table.user_balance
user_balance_db = table.user_calc
tick_db = table.ticks
valid_tx_db = table.valid_txs
valid_tx_statistics_db = table.valid_tx_statistics
block_db = table.blocks

protocol_name = "game-20"
safe_method_list = ["deploy",'mint','transfer','play']



class RedisListManager:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_client = redis.StrictRedis(host=host, port=port, db=db)

    def add_json_to_list(self, list_key, json_data):
        serialized_json = json.dumps(json_data)
        self.redis_client.rpush(list_key, serialized_json)

    def get_json_list(self, list_key):
        serialized_list = self.redis_client.lrange(list_key, 0, -1)
        json_list = [json.loads(item) for item in serialized_list]
        return json_list
    def clear_list(self, list_key):
        list_key = str(list_key)

    


rmanager = RedisListManager()

def get_balance(addr,tick):
    addr = addr.lower()
    tick = tick.upper()
    user_txs = user_balance_db.find({'address':addr,'tick':tick,"state":"success"})
    balance_list = [x['amt'] for x in user_txs]
    user_balance = sum(balance_list)
    return user_balance

def is_valid_tx(tx):
    try:
        tx_data = tx.input
        hash_ = tx["hash"].hex()
        block_height = tx.blockNumber
        json_str = bytes.fromhex(tx_data[2:]).decode('utf-8')
        json_data = json.loads(json_str)
        return is_valid_memo(json_data,hash_,block_height)
    except Exception as e:
        return False 

def is_valid_memo(j,hash_,block_height):
    try:
        p = j['p']
        op = j['op']
        tick = j['tick']
        if op=="transfer":
            amt = j['amt']
            if amt<=0 or amt>=210000000000:
                print("错误的转账参数")
                return False
        if op=="play":
            amt = j['amt']
            key = j['key']
            
        return p == protocol_name and op in safe_method_list
    except Exception as e:
        print(f"解析memo失败{e}")
        bad_db.insert_one({"json":j,'hash':hash_,"block_height":block_height})




def mint(tick_info,memo,tx_info):
    to_address = tx_info['to_address']
    block_height = tx_info['block_height']
    tick_end_time = tick_info['end_block']
    if block_height<=tick_end_time and block_height>tick_info['start_block']:
        rmanager.add_json_to_list(str(block_height),{'tick':tick_info['tick'],'target':to_address})
    

def transfer(tick_info,memo,tx_info):
    print(tx_info)
    from_address = tx_info['from_address']
    to_address = tx_info['to_address']
    block_height = tx_info['block_height']
    amt = int(memo["amt"])
    tick_name = tick_info['tick']
    end_block = tick_info['end_block']
    if block_height>end_block:
        user_balance = get_balance(from_address,tick_name)
        print(user_balance,amt)
        if user_balance>=amt:
            print(f'用户{from_address}向{to_address}转账{amt}')
            user_balance_db.insert_one({
                "tick":tick_name,
                'address':from_address,
                'block_height':block_height,
                'amt':(-1*amt),
                "type":"transfer",
                "from":from_address,
                'to':to_address,
                "hash":tx_info["hash"],
                "state":"pending"})
            user_balance_db.insert_one({
                "tick":tick_name,
                'address':to_address,
                'block_height':block_height,
                'amt':amt,
                "type":"transfer",
                "from":from_address,
                'to':to_address,
                "hash":tx_info["hash"],
                "state":"pending"})
  


def deploy(memo,tx_info):
    tick_name = memo['tick'].strip().upper()
    block_height = tx_info['block_height']
    t = int(time.time())
    amt = memo['amt']
    start = block_height-block_height%block_range+block_range
    tick_db.insert_one({
        'tick':tick_name,
        'block_supply':memo['amt'],
        'p':memo['p'],
        'op':memo['op'],
        "deployer":tx_info["from_address"],
        "deploy_number":block_height,
        "total_supply":(mine_block_count/block_range)*memo['amt'],
        'start_block':start,
        "end_block":start+mine_block_count,
        "update_time":t
    })
    print(f"deploy success:{tick_name},deployer :{tx_info['from_address']}")

def get_balance(addr,tick):
    user_txs = user_balance_db.find({'address':addr,'tick':tick,"state":"success"})
    balance_list = [x['amt'] for x in user_txs]
    user_balance = sum(balance_list)
    return user_balance


def share_mining_reward(block_height):
    mints = {}
    start_block = block_height-block_range

    for height in range(start_block+1,block_height+1):
        mint_txs = rmanager.get_json_list(str(height))
        for tx in mint_txs:
            tick_name = tx['tick']
            target = tx['target']
            if  mints.get(tick_name):
                mints[tick_name].append(target)
            else:
                mints[tick_name] = [target]
    # The logic here is to take all the addresses in the 10 blocks that have the same tick of mint and filter them underneath.
    for tick in mints:
        address_list = [addr.lower() for addr in list(set(mints[tick])) if addr]
        tick_info = tick_db.find_one({'tick':tick})
        supply = tick_info['block_supply']
        addon = int(supply/len(address_list))
        user_balance_db.delete_many({'block_height':block_height})
        user_to_insert = [{"tick":tick,'address':user_address,'block_height':block_height,'amt':addon,'state':"success","type":"mint"} for user_address in address_list]
        user_balance_db.insert_many(user_to_insert)

    total_info = list(valid_tx_db.find({"block_height":{"$gt":start_block,"$lte":block_height}}))
    total_tx = sum([x['tx_amount'] for x in total_info])
    total_valid = sum([x['valid_tx_amount'] for x in total_info])
    valid_tx_statistics_db.update_one({"start_block":start_block,"end_block":block_height},{"$set":{"total_tx":total_tx,"total_valid":total_valid}},upsert=True)
    block_db.update_one({'state':True},{"$set":{"reward_block_height":int(block_height)}})
    print("-----"*10)













