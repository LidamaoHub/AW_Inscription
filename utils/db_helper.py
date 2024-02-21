"""
chain_scanner.py
Tools for scanning blockchain and persisting data to databases
"""

import json
import datetime
from web3 import Web3
import mysql.connector

# Global config
START_BLOCK = 0 
END_BLOCK = "latest"
WEB3_PROVIDER = "https://mainnet.infura.io/v3/xxxxxxx"  
MYSQL_CONFIG = {
  'user': 'blockchain',
  'password': 'block123', 
  'host': '127.0.0.1',
  'database': 'blocks'
}

def init_web3():
    """Creates web3 connection instance"""
    web3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER))
    return web3

def get_block_range(start, end): 
    """Returns iterator over specified block range""" 
    return range(start, end+1)

def process_block(block):
    """Extracts desired block data for storage"""
    block_data = {
        "number": block.number, 
        "timestamp": str(datetime.datetime.utcfromtimestamp(block.timestamp)),   
        "txn_count": len(block.transactions)
    }
    return block_data
    
def store_blocks(blocks):
    """Stores list of block data to MySQL database""" 
    db = mysql.connector.connect(**MYSQL_CONFIG) 
    cursor = db.cursor()
    
    for block in blocks:
        sql = """INSERT INTO blocks VALUES (%s, %s, %s)"""
        values = (block["number"], block["timestamp"], block["txn_count"])
        
        cursor.execute(sql, values)
        
    db.commit() 
    db.close()
    
if __name__ == "__main__":
    web3 = init_web3()  
    block_range = get_block_range(START_BLOCK, END_BLOCK)
    
    scanned_blocks = []
    
    # Scan blockchain and extract data
    for n in block_range:   
        block = web3.eth.getBlock(n)
        scanned_blocks.append(process_block(block)) 
        
    store_blocks(scanned_blocks)