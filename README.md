

# AW Inscription

This project is a backend service for AW Inscription based on the Flask framework.


## Inscription operating method

**Deploy**
```json
{
    "p": "game-20",
    "op": "deploy",
    "tick": "game",
    "amt": 8000000
}
```

**Mint**
```json
{
      "p": "game-20",  
      "op": "mint", 
      "tick": "game",
}
```
**Transfer**
```json
{
    "p": "game-20",
    "op": "transfer",
    "tick": "game",
    "amt": 8000000
}
```
The recipient's address is the transfer address

**Market**
```json
{
    "p": "game-20",
    "op": "market",
    "tick": "game",
    "amt": 8000000,
    "func":"sell"
}
```
**Play**
```json
{
    "p": "game-20", 
     "op": "play",
     "tick": "game", 
     "amt": 10, 
     "key":"up"
 }
```


## Project Overview

The project provides a series of APIs for querying blockchain-related information, including address balances, address increment amounts, Tick lists, transaction statistics, and more.

## Project Structure

- `app.py`: The main file of the Flask application, containing all the API definitions and service startup code.
- `tools.py`: Tool module containing some utility functions, such as balance retrieval.
- `statics.py`: Static configuration file containing static configuration information such as RPC address and starting block number for block scanning.

## API Documentation

### 1. Get Address Balance

- **Endpoint**: `/v1/get_balance`
- **Request Method**: GET
- **Request Parameters**:
  - `address`: string, the address
  - `tick`: string, the token type
- **Response**: JSON format containing balance information

### 2. Get Address Increment Amount

- **Endpoint**: `/v1/get_address_amount`
- **Request Method**: GET
- **Request Parameters**:
  - `tick`: string, the token type
- **Response**: JSON format containing address increment amount information

### 3. Get Tick List

- **Endpoint**: `/v1/get_tick_list`
- **Request Method**: GET
- **Response**: JSON format containing Tick list information

### 4. Get Transaction Statistics

- **Endpoint**: `/v1/get_tx_statisstics`
- **Request Method**: GET
- **Response**: JSON format containing transaction statistics information

### 5. Get Address Balance List

- **Endpoint**: `/v1/get_balance_list`
- **Request Method**: GET
- **Response**: JSON format containing address balance list information

### 6. Get Video URL

- **Endpoint**: `/v1/get_video_url`
- **Request Method**: GET
- **Response**: JSON format containing video URL information

### 7. Health Check

- **Endpoint**: `/v1/ping`
- **Request Method**: GET
- **Response**: JSON format containing health check result

## Dependency Installation

```bash
pip install Flask web3 pymongo
```

## Startup

```bash
python app.py
```

## Notes

- This project depends on the MongoDB database. Please ensure that MongoDB is installed and running.
- Please modify the RPC address and other configuration information in `statics.py` according to the actual situation.

## Other

If you have any questions, please contact the developer for assistance.
