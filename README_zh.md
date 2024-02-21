# AW Inscription

该项目是一个基于 Flask 框架的区块链应用后端服务。

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

## 项目简介

该项目提供了一系列接口，用于查询AW Inscription相关信息，包括地址余额、地址增加数量、Tick 列表、交易统计信息等。

## 项目结构

- `app.py`：Flask 应用主文件，包含了所有的接口定义和服务启动代码。
- `tools.py`：工具模块，包含了一些辅助函数，如获取余额等。
- `statics.py`：静态配置文件，包含了一些静态配置信息，如 RPC 地址、区块扫描起始块号等。

## 接口文档

### 1. 获取地址余额

- **接口路径**：`/v1/get_balance`
- **请求方法**：GET
- **请求参数**：
  - `address`：string，地址
  - `tick`：string，代币类型
- **返回结果**：JSON 格式，包含余额信息

### 2. 获取地址增加数量

- **接口路径**：`/v1/get_address_amount`
- **请求方法**：GET
- **请求参数**：
  - `tick`：string，代币类型
- **返回结果**：JSON 格式，包含地址增加数量信息

### 3. 获取 Tick 列表

- **接口路径**：`/v1/get_tick_list`
- **请求方法**：GET
- **返回结果**：JSON 格式，包含 Tick 列表信息

### 4. 获取交易统计信息

- **接口路径**：`/v1/get_tx_statisstics`
- **请求方法**：GET
- **返回结果**：JSON 格式，包含交易统计信息

### 5. 获取地址余额列表

- **接口路径**：`/v1/get_balance_list`
- **请求方法**：GET
- **返回结果**：JSON 格式，包含地址余额列表信息

### 6. 获取视频链接

- **接口路径**：`/v1/get_video_url`
- **请求方法**：GET
- **返回结果**：JSON 格式，包含视频链接信息

### 7. 健康检查

- **接口路径**：`/v1/ping`
- **请求方法**：GET
- **返回结果**：JSON 格式，包含健康检查结果

## 依赖安装

```bash
pip install Flask web3 pymongo
```

## 启动方式

```bash
python app.py
```

## 注意事项

- 该项目依赖于 MongoDB 数据库，请确保已安装并运行 MongoDB 服务。
- 请根据实际情况修改 `statics.py` 中的 RPC 地址等配置信息。

## 其他

如有任何问题，请联系开发者进行咨询。
