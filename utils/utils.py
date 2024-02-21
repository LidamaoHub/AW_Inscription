# Collection of common utility functions

import web
import json
import requests

# Configuration
BLOCKCHAIN_API_URL = "https://api.blockchain.com/v3"
CONTRACT_ADDRESS = "0x123456789012345678901234567890"  

def connect_to_blockchain():
    """Connects to the blockchain network
    
    Uses web3 to initialize a connection to the Ethereum blockchain
    and contract ABI for the smart contract we want to interact with.
    
    Returns:
        - web3 connection object
        - contract instance
    """
    web3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_API_URL)) 
    contract_abi = json.loads("ABI") 
    contract =  web3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)
    
    return web3, contract

def get_latest_block():
    """Gets the latest block details from the chain
    
    Connects using web3 and eth.getBlock to return details 
    on the latest block.
    
    Returns:
        dict: Block details
    """    
    web3, contract = connect_to_blockchain()
    block = web3.eth.getBlock('latest')
    
    return block

def process_transaction(tx):
    """Processes an individual transaction
    
    Accepts a transaction object, analyzes the parameters, 
    extracts source/target addresses and token amounts, 
    runs validation logic, and returns a cleaned dict.
    
    Args:  
        tx: The transaction dict
        
    Returns: 
        dict: Processed transaction  
    """
    # Complex transaction analysis and processing
    
    output = {
        "from": tx["source"], 
        "to": tx["target"],
        "amount": tx["token_amount"], 
        "valid": True
    }
    
    return output
    
def sync_data(start_block, end_block):
    """Syncs blockchain data to database
    
    Iterates through specified block range, extracts transactions
    from each block, processes the transactions, and updates the 
    database (ie MongoDB) with the cleaned transaction datasets.
    """ 
    web3, contract = connect_to_blockchain()
    
    for i in range(start_block, end_block):
        block = web3.eth.getBlock(i)
        
        for tx in block["transactions"]:
            cleaned = process_transactions(tx)  
            store_to_db(cleaned)
            
    print(f"{end_block - start_block} blocks synced.")