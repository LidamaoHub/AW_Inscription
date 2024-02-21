# -*- coding: utf-8 -*-
from web3 import Web3
from flask import Flask,request,jsonify,redirect,Response
import pymongo
import os,time,json,datetime
from LidamaoToolkit import json_require,create_token,safe_dict,err,insert_cover
from tools import get_balance
from statics import rpc_url,scan_start_block,block_range,mine_block_count


client = pymongo.MongoClient("mongodb://127.0.0.1/", 27017)


table = client.game_test
tx_db = table.txs
bad_db = table.bads
block_db = table.blocks
tick_db = table.ticks
# user_balance_db = table.user_balance
user_balance_db = table.user_calc

user_increase_db = table.increases
valid_tx_db = table.valid_txs
valid_tx_statistics_db = table.valid_tx_statistics


w3 = Web3(Web3.HTTPProvider(rpc_url))

app = Flask(__name__)

@app.route("/v1/get_balance",methods=["GET"])
@json_require({"address":"string","tick":"string"},"GET")
def get_balance_(info):
    print(info)
    addr = info['address'].lower()
    tick = info['tick'].upper()
    balance = get_balance(addr,tick)

    
    return jsonify({"code":0,'balance':balance})

@app.route("/v1/get_address_amount",methods=["GET","POST"])
@json_require({"tick":"string"},"GET")
def get_address_amount(info):
    tick = info['tick'].upper()
    page_size = int(request.args.get("page_size",30))

    latest_block_number = w3.eth.blockNumber
    start = latest_block_number-(page_size*300)
    amount_list = list(user_increase_db.find({'tick':tick}).sort('block_height',-1).limit(page_size))
    safe_list = ['block_height','tick','count']
    amount_list = [safe_dict(x,safe_list) for x in amount_list]
    
    return jsonify({"code":0,'amount_list':amount_list})
@app.route("/v1/get_tick_list",methods=["GET","POST"])
def get_tick_list():
    ticks = list(tick_db.find({}))
    safe_list = ['deploy_number','p','start_block',"tick",'total_supply','block_supply']
    ticks = [safe_dict(x,safe_list) for x in ticks]
    latest_block_number = w3.eth.blockNumber
    for tick in ticks:
        tick_incr = user_increase_db.find_one({'tick':tick["tick"]},sort=[("block_height", -1)])
        print("tick_incr",tick_incr,tick)
        address_count = tick_incr['count'] if tick_incr else 0
        tick['address_count'] = address_count
        start = tick['start_block']

        pipeline = [
            {
                '$match': {"block_height":{"$gte":start,"$lte":start+mine_block_count}} 
            },
            {
                '$group': {
                    '_id': None,  
                    'total': {'$sum': '$amt'} 
                }
            }
        ]

        result = list(user_balance_db.aggregate(pipeline))

        # tick['minted'] = result[0]['total'] if len(result) else 0
        tick['minted'] = (latest_block_number-start)*tick['block_supply']/10
        tick['end_block'] = start+mine_block_count

    
    return jsonify({"code":0,"tick_list":ticks})

@app.route("/v1/get_tx_statisstics",methods=["GET","POST"])
def get_tx_statisstics():
    last_ten = valid_tx_statistics_db.find().sort("end_block",-1).limit(10)
    safe_list = ['end_block','start_block',"total_tx","total_valid"]
    last_ten = [safe_dict(x,safe_list) for x in last_ten]
    
    return jsonify({"code":0,'tx_statisstics':last_ten})


@app.route("/v1/get_balance_list",methods=["GET","POST"])
def get_balance_list():
    page = int(request.args.get("page",1))-1
    page_size = int(request.args.get('page_size',30))
    if page_size>50:
        page_size = 50
    total = 209510578375
    users = user_balance_db.find().sort('amt',-1).skip(page*page_size).limit(page_size)
    users = [safe_dict(x,['address','amt']) for x in users]
    count = user_balance_db.count_documents({})
    return jsonify({"code":0,'user_balance_list':users,'total':total,'count':count})


@app.route("/v1/get_video_url",methods=["GET","POST"])
def get_video_url():
    url = "https://www.youtube.com/watch?v=tjhfI_c5e1A"
    
    return jsonify({"code":0,"url":url})

@app.route("/v1/ping",methods=["GET","POST"])
def ping():
    
    return jsonify({"code":0})




if __name__ == "__main__":
    app.run(port=6666)
