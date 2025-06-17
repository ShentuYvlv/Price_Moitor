
bybit

Kind: global class
Extends: Exchange

    enableDemoTrading
    isUnifiedEnabled
    upgradeUnifiedTradeAccount
    fetchTime
    fetchCurrencies
    fetchMarkets
    fetchTicker
    fetchTickers
    fetchBidsAsks
    fetchOHLCV
    fetchFundingRates
    fetchFundingRateHistory
    fetchTrades
    fetchOrderBook
    fetchBalance
    createMarketBuyOrderWithCost
    createMarkeSellOrderWithCost
    createOrder
    createOrders
    editOrder
    editOrders
    cancelOrder
    cancelOrders
    cancelAllOrdersAfter
    cancelOrdersForSymbols
    cancelAllOrders
    fetchOrderClassic
    fetchOrder
    fetchOrders
    fetchOrdersClassic
    fetchClosedOrder
    fetchOpenOrder
    fetchCanceledAndClosedOrders
    fetchClosedOrders
    fetchCanceledOrders
    fetchOpenOrders
    fetchOrderTrades
    fetchMyTrades
    fetchDepositAddressesByNetwork
    fetchDepositAddress
    fetchDeposits
    fetchWithdrawals
    fetchLedger
    withdraw
    fetchPosition
    fetchPositions
    fetchLeverage
    setMarginMode
    setLeverage
    setPositionMode
    fetchOpenInterest
    fetchOpenInterestHistory
    fetchCrossBorrowRate
    fetchBorrowInterest
    fetchBorrowRateHistory
    transfer
    fetchTransfers
    borrowCrossMargin
    repayCrossMargin
    fetchMarketLeverageTiers
    fetchTradingFee
    fetchTradingFees
    fetchDepositWithdrawFees
    fetchSettlementHistory
    fetchMySettlementHistory
    fetchVolatilityHistory
    fetchGreeks
    fetchMyLiquidations
    fetchLeverageTiers
    fetchFundingHistory
    fetchOption
    fetchOptionChain
    fetchPositionsHistory
    fetchConvertCurrencies
    fetchConvertQuote
    createConvertTrade
    fetchConvertTrade
    fetchConvertTradeHistory
    fetchLongShortRatioHistory
    createOrderWs
    editOrderWs
    cancelOrderWs
    watchTicker
    watchTickers
    unWatchTickers
    unWatchTicker
    watchBidsAsks
    watchOHLCV
    watchOHLCVForSymbols
    unWatchOHLCVForSymbols
    unWatchOHLCV
    watchOrderBook
    watchOrderBookForSymbols
    unWatchOrderBookForSymbols
    unWatchOrderBook
    watchTrades
    watchTradesForSymbols
    unWatchTradesForSymbols
    unWatchTrades
    watchMyTrades
    unWatchMyTrades
    watchPositions
    watchLiquidations
    watchOrders
    unWatchOrders
    watchBalance

enableDemoTrading

enables or disables demo trading mode

Kind: instance method of bybit

See: https://bybit-exchange.github.io/docs/v5/demo
Param 	Type 	Required 	Description
enable 	boolean 	No 	true if demo trading should be enabled, false otherwise

bybit.enableDemoTrading ([enable])

isUnifiedEnabled

returns [enableUnifiedMargin, enableUnifiedAccount] so the user can check if unified account is enabled

Kind: instance method of bybit
Returns: any - [enableUnifiedMargin, enableUnifiedAccount]

See

    https://bybit-exchange.github.io/docs/v5/user/apikey-info#http-request
    https://bybit-exchange.github.io/docs/v5/account/account-info

Param 	Type 	Required 	Description
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.isUnifiedEnabled ([params])

upgradeUnifiedTradeAccount

upgrades the account to unified trade account warning this is irreversible

Kind: instance method of bybit
Returns: any - nothing

See: https://bybit-exchange.github.io/docs/v5/account/upgrade-unified-account
Param 	Type 	Required 	Description
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.upgradeUnifiedTradeAccount ([params])

fetchTime

fetches the current integer timestamp in milliseconds from the exchange server

Kind: instance method of bybit
Returns: int - the current integer timestamp in milliseconds from the exchange server

See: https://bybit-exchange.github.io/docs/v5/market/time
Param 	Type 	Required 	Description
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.fetchTime ([params])

fetchCurrencies

fetches all available currencies on an exchange

Kind: instance method of bybit
Returns: object - an associative dictionary of currencies

See: https://bybit-exchange.github.io/docs/v5/asset/coin-info
Param 	Type 	Required 	Description
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.fetchCurrencies ([params])

fetchMarkets

retrieves data on all markets for bybit

Kind: instance method of bybit
Returns: Array<object> - an array of objects representing market data

See: https://bybit-exchange.github.io/docs/v5/market/instrument
Param 	Type 	Required 	Description
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.fetchMarkets ([params])

fetchTicker

fetches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market

Kind: instance method of bybit
Returns: object - a ticker structure

See: https://bybit-exchange.github.io/docs/v5/market/tickers
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to fetch the ticker for
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.fetchTicker (symbol[, params])

fetchTickers

fetches price tickers for multiple markets, statistical information calculated over the past 24 hours for each market

Kind: instance method of bybit
Returns: object - an array of ticker structures

See: https://bybit-exchange.github.io/docs/v5/market/tickers
Param 	Type 	Required 	Description
symbols 	Array<string> 	Yes 	unified symbols of the markets to fetch the ticker for, all market tickers are returned if not assigned
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.subType 	string 	No 	contract only 'linear', 'inverse'
params.baseCoin 	string 	No 	option only base coin, default is 'BTC'

bybit.fetchTickers (symbols[, params])

fetchBidsAsks

fetches the bid and ask price and volume for multiple markets

Kind: instance method of bybit
Returns: object - a dictionary of ticker structures

See: https://bybit-exchange.github.io/docs/v5/market/tickers
Param 	Type 	Required 	Description
symbols 	Array<string>, undefined 	Yes 	unified symbols of the markets to fetch the bids and asks for, all markets are returned if not assigned
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.subType 	string 	No 	contract only 'linear', 'inverse'
params.baseCoin 	string 	No 	option only base coin, default is 'BTC'

bybit.fetchBidsAsks (symbols[, params])

fetchOHLCV

fetches historical candlestick data containing the open, high, low, and close price, and the volume of a market

Kind: instance method of bybit
Returns: Array<Array<int>> - A list of candles ordered as timestamp, open, high, low, close, volume

See

    https://bybit-exchange.github.io/docs/v5/market/kline
    https://bybit-exchange.github.io/docs/v5/market/mark-kline
    https://bybit-exchange.github.io/docs/v5/market/index-kline
    https://bybit-exchange.github.io/docs/v5/market/preimum-index-kline

Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to fetch OHLCV data for
timeframe 	string 	Yes 	the length of time each candle represents
since 	int 	No 	timestamp in ms of the earliest candle to fetch
limit 	int 	No 	the maximum amount of candles to fetch
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.until 	int 	No 	the latest time in ms to fetch orders for
params.paginate 	boolean 	No 	default false, when true will automatically paginate by calling this endpoint multiple times. See in the docs all the availble parameters

bybit.fetchOHLCV (symbol, timeframe[, since, limit, params])

fetchFundingRates

fetches funding rates for multiple markets

Kind: instance method of bybit
Returns: Array<object> - a list of funding rate structures

See: https://bybit-exchange.github.io/docs/v5/market/tickers
Param 	Type 	Required 	Description
symbols 	Array<string> 	Yes 	unified symbols of the markets to fetch the funding rates for, all market funding rates are returned if not assigned
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.fetchFundingRates (symbols[, params])

fetchFundingRateHistory

fetches historical funding rate prices

Kind: instance method of bybit
Returns: Array<object> - a list of funding rate structures

See: https://bybit-exchange.github.io/docs/v5/market/history-fund-rate
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to fetch the funding rate history for
since 	int 	No 	timestamp in ms of the earliest funding rate to fetch
limit 	int 	No 	the maximum amount of funding rate structures to fetch
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.until 	int 	No 	timestamp in ms of the latest funding rate
params.paginate 	boolean 	No 	default false, when true will automatically paginate by calling this endpoint multiple times. See in the docs all the availble parameters

bybit.fetchFundingRateHistory (symbol[, since, limit, params])

fetchTrades

get the list of most recent trades for a particular symbol

Kind: instance method of bybit
Returns: Array<Trade> - a list of trade structures

See: https://bybit-exchange.github.io/docs/v5/market/recent-trade
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to fetch trades for
since 	int 	No 	timestamp in ms of the earliest trade to fetch
limit 	int 	No 	the maximum amount of trades to fetch
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.type 	string 	No 	market type, ['swap', 'option', 'spot']
params.subType 	string 	No 	market subType, ['linear', 'inverse']

bybit.fetchTrades (symbol[, since, limit, params])

fetchOrderBook

fetches information on open orders with bid (buy) and ask (sell) prices, volumes and other data

Kind: instance method of bybit
Returns: object - A dictionary of order book structures indexed by market symbols

See: https://bybit-exchange.github.io/docs/v5/market/orderbook
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to fetch the order book for
limit 	int 	No 	the maximum amount of order book entries to return
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.fetchOrderBook (symbol[, limit, params])

fetchBalance

query for balance and get the amount of funds available for trading or funds locked in orders

Kind: instance method of bybit
Returns: object - a balance structure

See

    https://bybit-exchange.github.io/docs/v5/spot-margin-normal/account-info
    https://bybit-exchange.github.io/docs/v5/asset/all-balance
    https://bybit-exchange.github.io/docs/v5/account/wallet-balance

Param 	Type 	Required 	Description
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.type 	string 	No 	wallet type, ['spot', 'swap', 'funding']

bybit.fetchBalance ([params])

createMarketBuyOrderWithCost

create a market buy order by providing the symbol and cost

Kind: instance method of bybit
Returns: object - an order structure

See: https://bybit-exchange.github.io/docs/v5/order/create-order
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to create an order in
cost 	float 	Yes 	how much you want to trade in units of the quote currency
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.createMarketBuyOrderWithCost (symbol, cost[, params])

createMarkeSellOrderWithCost

create a market sell order by providing the symbol and cost

Kind: instance method of bybit
Returns: object - an order structure

See: https://bybit-exchange.github.io/docs/v5/order/create-order
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to create an order in
cost 	float 	Yes 	how much you want to trade in units of the quote currency
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.createMarkeSellOrderWithCost (symbol, cost[, params])

createOrder

create a trade order

Kind: instance method of bybit
Returns: object - an order structure

See

    https://bybit-exchange.github.io/docs/v5/order/create-order
    https://bybit-exchange.github.io/docs/v5/position/trading-stop

Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to create an order in
type 	string 	Yes 	'market' or 'limit'
side 	string 	Yes 	'buy' or 'sell'
amount 	float 	Yes 	how much of currency you want to trade in units of base currency
price 	float 	No 	the price at which the order is to be fulfilled, in units of the quote currency, ignored in market orders
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.timeInForce 	string 	No 	"GTC", "IOC", "FOK"
params.postOnly 	bool 	No 	true or false whether the order is post-only
params.reduceOnly 	bool 	No 	true or false whether the order is reduce-only
params.positionIdx 	string 	No 	contracts only 0 for one-way mode, 1 buy side of hedged mode, 2 sell side of hedged mode
params.hedged 	bool 	No 	contracts only true for hedged mode, false for one way mode, default is false
params.isLeverage 	int 	No 	unified spot only false then spot trading true then margin trading
params.tpslMode 	string 	No 	contract only 'full' or 'partial'
params.mmp 	string 	No 	option only market maker protection
params.triggerDirection 	string 	No 	contract only the direction for trigger orders, 'above' or 'below'
params.triggerPrice 	float 	No 	The price at which a trigger order is triggered at
params.stopLossPrice 	float 	No 	The price at which a stop loss order is triggered at
params.takeProfitPrice 	float 	No 	The price at which a take profit order is triggered at
params.takeProfit 	object 	No 	takeProfit object in params containing the triggerPrice at which the attached take profit order will be triggered
params.takeProfit.triggerPrice 	float 	No 	take profit trigger price
params.stopLoss 	object 	No 	stopLoss object in params containing the triggerPrice at which the attached stop loss order will be triggered
params.stopLoss.triggerPrice 	float 	No 	stop loss trigger price
params.trailingAmount 	string 	No 	the quote amount to trail away from the current market price
params.trailingTriggerPrice 	string 	No 	the price to trigger a trailing order, default uses the price argument

bybit.createOrder (symbol, type, side, amount[, price, params])

createOrders

create a list of trade orders

Kind: instance method of bybit
Returns: object - an order structure

See: https://bybit-exchange.github.io/docs/v5/order/batch-place
Param 	Type 	Required 	Description
orders 	Array 	Yes 	list of orders to create, each object should contain the parameters required by createOrder, namely symbol, type, side, amount, price and params
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.createOrders (orders[, params])

editOrder

edit a trade order

Kind: instance method of bybit
Returns: object - an order structure

See

    https://bybit-exchange.github.io/docs/v5/order/amend-order
    https://bybit-exchange.github.io/docs/derivatives/unified/replace-order
    https://bybit-exchange.github.io/docs/api-explorer/derivatives/trade/contract/replace-order

Param 	Type 	Required 	Description
id 	string 	Yes 	cancel order id
symbol 	string 	Yes 	unified symbol of the market to create an order in
type 	string 	Yes 	'market' or 'limit'
side 	string 	Yes 	'buy' or 'sell'
amount 	float 	Yes 	how much of currency you want to trade in units of base currency
price 	float 	Yes 	the price at which the order is to be fulfilled, in units of the quote currency, ignored in market orders
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.triggerPrice 	float 	No 	The price that a trigger order is triggered at
params.stopLossPrice 	float 	No 	The price that a stop loss order is triggered at
params.takeProfitPrice 	float 	No 	The price that a take profit order is triggered at
params.takeProfit 	object 	No 	takeProfit object in params containing the triggerPrice that the attached take profit order will be triggered
params.takeProfit.triggerPrice 	float 	No 	take profit trigger price
params.stopLoss 	object 	No 	stopLoss object in params containing the triggerPrice that the attached stop loss order will be triggered
params.stopLoss.triggerPrice 	float 	No 	stop loss trigger price
params.triggerBy 	string 	No 	'IndexPrice', 'MarkPrice' or 'LastPrice', default is 'LastPrice', required if no initial value for triggerPrice
params.slTriggerBy 	string 	No 	'IndexPrice', 'MarkPrice' or 'LastPrice', default is 'LastPrice', required if no initial value for stopLoss
params.tpTriggerby 	string 	No 	'IndexPrice', 'MarkPrice' or 'LastPrice', default is 'LastPrice', required if no initial value for takeProfit

bybit.editOrder (id, symbol, type, side, amount, price[, params])

editOrders

edit a list of trade orders

Kind: instance method of bybit
Returns: object - an order structure

See: https://bybit-exchange.github.io/docs/v5/order/batch-amend
Param 	Type 	Required 	Description
orders 	Array 	Yes 	list of orders to create, each object should contain the parameters required by createOrder, namely symbol, type, side, amount, price and params
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.editOrders (orders[, params])

cancelOrder

cancels an open order

Kind: instance method of bybit
Returns: object - An order structure

See: https://bybit-exchange.github.io/docs/v5/order/cancel-order
Param 	Type 	Required 	Description
id 	string 	Yes 	order id
symbol 	string 	Yes 	unified symbol of the market the order was made in
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.trigger 	boolean 	No 	spot only whether the order is a trigger order
params.stop 	boolean 	No 	alias for trigger
params.orderFilter 	string 	No 	spot only 'Order' or 'StopOrder' or 'tpslOrder'

bybit.cancelOrder (id, symbol[, params])

cancelOrders

cancel multiple orders

Kind: instance method of bybit
Returns: object - an list of order structures

See: https://bybit-exchange.github.io/docs/v5/order/batch-cancel
Param 	Type 	Required 	Description
ids 	Array<string> 	Yes 	order ids
symbol 	string 	Yes 	unified symbol of the market the order was made in
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.clientOrderIds 	Array<string> 	No 	client order ids

bybit.cancelOrders (ids, symbol[, params])

cancelAllOrdersAfter

dead man's switch, cancel all orders after the given timeout

Kind: instance method of bybit
Returns: object - the api result

See: https://bybit-exchange.github.io/docs/v5/order/dcp
Param 	Type 	Required 	Description
timeout 	number 	Yes 	time in milliseconds
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.product 	string 	No 	OPTIONS, DERIVATIVES, SPOT, default is 'DERIVATIVES'

bybit.cancelAllOrdersAfter (timeout[, params])

cancelOrdersForSymbols

cancel multiple orders for multiple symbols

Kind: instance method of bybit
Returns: object - an list of order structures

See: https://bybit-exchange.github.io/docs/v5/order/batch-cancel
Param 	Type 	Required 	Description
orders 	Array<CancellationRequest> 	Yes 	list of order ids with symbol, example [{"id": "a", "symbol": "BTC/USDT"}, {"id": "b", "symbol": "ETH/USDT"}]
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.cancelOrdersForSymbols (orders[, params])

cancelAllOrders

cancel all open orders

Kind: instance method of bybit
Returns: Array<object> - a list of order structures

See: https://bybit-exchange.github.io/docs/v5/order/cancel-all
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol, only orders in the market of this symbol are cancelled when symbol is not undefined
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.trigger 	boolean 	No 	true if trigger order
params.stop 	boolean 	No 	alias for trigger
params.type 	string 	No 	market type, ['swap', 'option', 'spot']
params.subType 	string 	No 	market subType, ['linear', 'inverse']
params.baseCoin 	string 	No 	Base coin. Supports linear, inverse & option
params.settleCoin 	string 	No 	Settle coin. Supports linear, inverse & option

bybit.cancelAllOrders (symbol[, params])

fetchOrderClassic

fetches information on an order made by the user classic accounts only

Kind: instance method of bybit
Returns: object - An order structure

See: https://bybit-exchange.github.io/docs/v5/order/order-list
Param 	Type 	Required 	Description
id 	string 	Yes 	the order id
symbol 	string 	Yes 	unified symbol of the market the order was made in
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.fetchOrderClassic (id, symbol[, params])

fetchOrder

classic accounts only/ spot not supported fetches information on an order made by the user classic accounts only

Kind: instance method of bybit
Returns: object - An order structure

See: https://bybit-exchange.github.io/docs/v5/order/order-list
Param 	Type 	Required 	Description
id 	string 	Yes 	the order id
symbol 	string 	Yes 	unified symbol of the market the order was made in
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.acknowledged 	object 	No 	to suppress the warning, set to true

bybit.fetchOrder (id, symbol[, params])

fetchOrders

classic accounts only/ spot not supported fetches information on multiple orders made by the user classic accounts only/ spot not supported

Kind: instance method of bybit
Returns: Array<Order> - a list of order structures

See: https://bybit-exchange.github.io/docs/v5/order/order-list
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol of the market orders were made in
since 	int 	No 	the earliest time in ms to fetch orders for
limit 	int 	No 	the maximum number of order structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.trigger 	boolean 	No 	true if trigger order
params.stop 	boolean 	No 	alias for trigger
params.type 	string 	No 	market type, ['swap', 'option']
params.subType 	string 	No 	market subType, ['linear', 'inverse']
params.orderFilter 	string 	No 	'Order' or 'StopOrder' or 'tpslOrder'
params.until 	int 	No 	the latest time in ms to fetch entries for
params.paginate 	boolean 	No 	default false, when true will automatically paginate by calling this endpoint multiple times. See in the docs all the availble parameters

bybit.fetchOrders (symbol[, since, limit, params])

fetchOrdersClassic

fetches information on multiple orders made by the user classic accounts only

Kind: instance method of bybit
Returns: Array<Order> - a list of order structures

See: https://bybit-exchange.github.io/docs/v5/order/order-list
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol of the market orders were made in
since 	int 	No 	the earliest time in ms to fetch orders for
limit 	int 	No 	the maximum number of order structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.trigger 	boolean 	No 	true if trigger order
params.stop 	boolean 	No 	alias for trigger
params.type 	string 	No 	market type, ['swap', 'option', 'spot']
params.subType 	string 	No 	market subType, ['linear', 'inverse']
params.orderFilter 	string 	No 	'Order' or 'StopOrder' or 'tpslOrder'
params.until 	int 	No 	the latest time in ms to fetch entries for
params.paginate 	boolean 	No 	default false, when true will automatically paginate by calling this endpoint multiple times. See in the docs all the availble parameters

bybit.fetchOrdersClassic (symbol[, since, limit, params])

fetchClosedOrder

fetches information on a closed order made by the user

Kind: instance method of bybit
Returns: object - an order structure

See: https://bybit-exchange.github.io/docs/v5/order/order-list
Param 	Type 	Required 	Description
id 	string 	Yes 	order id
symbol 	string 	No 	unified symbol of the market the order was made in
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.trigger 	boolean 	No 	set to true for fetching a closed trigger order
params.stop 	boolean 	No 	alias for trigger
params.type 	string 	No 	market type, ['swap', 'option', 'spot']
params.subType 	string 	No 	market subType, ['linear', 'inverse']
params.orderFilter 	string 	No 	'Order' or 'StopOrder' or 'tpslOrder'

bybit.fetchClosedOrder (id[, symbol, params])

fetchOpenOrder

fetches information on an open order made by the user

Kind: instance method of bybit
Returns: object - an order structure

See: https://bybit-exchange.github.io/docs/v5/order/open-order
Param 	Type 	Required 	Description
id 	string 	Yes 	order id
symbol 	string 	No 	unified symbol of the market the order was made in
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.trigger 	boolean 	No 	set to true for fetching an open trigger order
params.stop 	boolean 	No 	alias for trigger
params.type 	string 	No 	market type, ['swap', 'option', 'spot']
params.subType 	string 	No 	market subType, ['linear', 'inverse']
params.baseCoin 	string 	No 	Base coin. Supports linear, inverse & option
params.settleCoin 	string 	No 	Settle coin. Supports linear, inverse & option
params.orderFilter 	string 	No 	'Order' or 'StopOrder' or 'tpslOrder'

bybit.fetchOpenOrder (id[, symbol, params])

fetchCanceledAndClosedOrders

fetches information on multiple canceled and closed orders made by the user

Kind: instance method of bybit
Returns: Array<Order> - a list of order structures

See: https://bybit-exchange.github.io/docs/v5/order/order-list
Param 	Type 	Required 	Description
symbol 	string 	No 	unified market symbol of the market orders were made in
since 	int 	No 	the earliest time in ms to fetch orders for
limit 	int 	No 	the maximum number of order structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.trigger 	boolean 	No 	set to true for fetching trigger orders
params.stop 	boolean 	No 	alias for trigger
params.type 	string 	No 	market type, ['swap', 'option', 'spot']
params.subType 	string 	No 	market subType, ['linear', 'inverse']
params.orderFilter 	string 	No 	'Order' or 'StopOrder' or 'tpslOrder'
params.until 	int 	No 	the latest time in ms to fetch entries for
params.paginate 	boolean 	No 	default false, when true will automatically paginate by calling this endpoint multiple times. See in the docs all the available parameters

bybit.fetchCanceledAndClosedOrders ([symbol, since, limit, params])

fetchClosedOrders

fetches information on multiple closed orders made by the user

Kind: instance method of bybit
Returns: Array<Order> - a list of order structures

See: https://bybit-exchange.github.io/docs/v5/order/order-list
Param 	Type 	Required 	Description
symbol 	string 	No 	unified market symbol of the market orders were made in
since 	int 	No 	the earliest time in ms to fetch orders for
limit 	int 	No 	the maximum number of order structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.trigger 	boolean 	No 	set to true for fetching closed trigger orders
params.stop 	boolean 	No 	alias for trigger
params.type 	string 	No 	market type, ['swap', 'option', 'spot']
params.subType 	string 	No 	market subType, ['linear', 'inverse']
params.orderFilter 	string 	No 	'Order' or 'StopOrder' or 'tpslOrder'
params.until 	int 	No 	the latest time in ms to fetch entries for
params.paginate 	boolean 	No 	default false, when true will automatically paginate by calling this endpoint multiple times. See in the docs all the available parameters

bybit.fetchClosedOrders ([symbol, since, limit, params])

fetchCanceledOrders

fetches information on multiple canceled orders made by the user

Kind: instance method of bybit
Returns: object - a list of order structures

See: https://bybit-exchange.github.io/docs/v5/order/order-list
Param 	Type 	Required 	Description
symbol 	string 	No 	unified market symbol of the market orders were made in
since 	int 	No 	timestamp in ms of the earliest order, default is undefined
limit 	int 	No 	max number of orders to return, default is undefined
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.trigger 	boolean 	No 	true if trigger order
params.stop 	boolean 	No 	alias for trigger
params.type 	string 	No 	market type, ['swap', 'option', 'spot']
params.subType 	string 	No 	market subType, ['linear', 'inverse']
params.orderFilter 	string 	No 	'Order' or 'StopOrder' or 'tpslOrder'
params.until 	int 	No 	the latest time in ms to fetch entries for
params.paginate 	boolean 	No 	default false, when true will automatically paginate by calling this endpoint multiple times. See in the docs all the available parameters

bybit.fetchCanceledOrders ([symbol, since, limit, params])

fetchOpenOrders

fetch all unfilled currently open orders

Kind: instance method of bybit
Returns: Array<Order> - a list of order structures

See: https://bybit-exchange.github.io/docs/v5/order/open-order
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol
since 	int 	No 	the earliest time in ms to fetch open orders for
limit 	int 	No 	the maximum number of open orders structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.trigger 	boolean 	No 	set to true for fetching open trigger orders
params.stop 	boolean 	No 	alias for trigger
params.type 	string 	No 	market type, ['swap', 'option', 'spot']
params.subType 	string 	No 	market subType, ['linear', 'inverse']
params.baseCoin 	string 	No 	Base coin. Supports linear, inverse & option
params.settleCoin 	string 	No 	Settle coin. Supports linear, inverse & option
params.orderFilter 	string 	No 	'Order' or 'StopOrder' or 'tpslOrder'
params.paginate 	boolean 	No 	default false, when true will automatically paginate by calling this endpoint multiple times. See in the docs all the availble parameters

bybit.fetchOpenOrders (symbol[, since, limit, params])

fetchOrderTrades

fetch all the trades made from a single order

Kind: instance method of bybit
Returns: Array<object> - a list of trade structures

See: https://bybit-exchange.github.io/docs/v5/position/execution
Param 	Type 	Required 	Description
id 	string 	Yes 	order id
symbol 	string 	Yes 	unified market symbol
since 	int 	No 	the earliest time in ms to fetch trades for
limit 	int 	No 	the maximum number of trades to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.fetchOrderTrades (id, symbol[, since, limit, params])

fetchMyTrades

fetch all trades made by the user

Kind: instance method of bybit
Returns: Array<Trade> - a list of trade structures

See: https://bybit-exchange.github.io/docs/api-explorer/v5/position/execution
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol
since 	int 	No 	the earliest time in ms to fetch trades for
limit 	int 	No 	the maximum number of trades structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.type 	string 	No 	market type, ['swap', 'option', 'spot']
params.subType 	string 	No 	market subType, ['linear', 'inverse']
params.paginate 	boolean 	No 	default false, when true will automatically paginate by calling this endpoint multiple times. See in the docs all the availble parameters

bybit.fetchMyTrades (symbol[, since, limit, params])

fetchDepositAddressesByNetwork

fetch a dictionary of addresses for a currency, indexed by network

Kind: instance method of bybit
Returns: object - a dictionary of address structures indexed by the network

See: https://bybit-exchange.github.io/docs/v5/asset/master-deposit-addr
Param 	Type 	Required 	Description
code 	string 	Yes 	unified currency code of the currency for the deposit address
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.fetchDepositAddressesByNetwork (code[, params])

fetchDepositAddress

fetch the deposit address for a currency associated with this account

Kind: instance method of bybit
Returns: object - an address structure

See: https://bybit-exchange.github.io/docs/v5/asset/master-deposit-addr
Param 	Type 	Required 	Description
code 	string 	Yes 	unified currency code
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.fetchDepositAddress (code[, params])

fetchDeposits

fetch all deposits made to an account

Kind: instance method of bybit
Returns: Array<object> - a list of transaction structures

See: https://bybit-exchange.github.io/docs/v5/asset/deposit-record
Param 	Type 	Required 	Description
code 	string 	Yes 	unified currency code
since 	int 	No 	the earliest time in ms to fetch deposits for, default = 30 days before the current time
limit 	int 	No 	the maximum number of deposits structures to retrieve, default = 50, max = 50
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.until 	int 	No 	the latest time in ms to fetch deposits for, default = 30 days after since EXCHANGE SPECIFIC PARAMETERS
params.paginate 	boolean 	No 	default false, when true will automatically paginate by calling this endpoint multiple times. See in the docs all the availble parameters
params.cursor 	string 	No 	used for pagination

bybit.fetchDeposits (code[, since, limit, params])

fetchWithdrawals

fetch all withdrawals made from an account

Kind: instance method of bybit
Returns: Array<object> - a list of transaction structures

See: https://bybit-exchange.github.io/docs/v5/asset/withdraw-record
Param 	Type 	Required 	Description
code 	string 	Yes 	unified currency code
since 	int 	No 	the earliest time in ms to fetch withdrawals for
limit 	int 	No 	the maximum number of withdrawals structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.until 	int 	No 	the latest time in ms to fetch entries for
params.paginate 	boolean 	No 	default false, when true will automatically paginate by calling this endpoint multiple times. See in the docs all the availble parameters

bybit.fetchWithdrawals (code[, since, limit, params])

fetchLedger

fetch the history of changes, actions done by the user or operations that altered the balance of the user

Kind: instance method of bybit
Returns: object - a ledger structure

See

    https://bybit-exchange.github.io/docs/v5/account/transaction-log
    https://bybit-exchange.github.io/docs/v5/account/contract-transaction-log

Param 	Type 	Required 	Description
code 	string 	No 	unified currency code, default is undefined
since 	int 	No 	timestamp in ms of the earliest ledger entry, default is undefined
limit 	int 	No 	max number of ledger entries to return, default is undefined
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.paginate 	boolean 	No 	default false, when true will automatically paginate by calling this endpoint multiple times. See in the docs all the available parameters
params.subType 	string 	No 	if inverse will use v5/account/contract-transaction-log

bybit.fetchLedger ([code, since, limit, params])

withdraw

make a withdrawal

Kind: instance method of bybit
Returns: object - a transaction structure

See: https://bybit-exchange.github.io/docs/v5/asset/withdraw
Param 	Type 	Required 	Description
code 	string 	Yes 	unified currency code
amount 	float 	Yes 	the amount to withdraw
address 	string 	Yes 	the address to withdraw to
tag 	string 	Yes 	
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.withdraw (code, amount, address, tag[, params])

fetchPosition

fetch data on a single open contract trade position

Kind: instance method of bybit
Returns: object - a position structure

See: https://bybit-exchange.github.io/docs/v5/position
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol of the market the position is held in, default is undefined
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.fetchPosition (symbol[, params])

fetchPositions

fetch all open positions

Kind: instance method of bybit
Returns: Array<object> - a list of position structure

See: https://bybit-exchange.github.io/docs/v5/position
Param 	Type 	Required 	Description
symbols 	Array<string> 	Yes 	list of unified market symbols
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.type 	string 	No 	market type, ['swap', 'option', 'spot']
params.subType 	string 	No 	market subType, ['linear', 'inverse']
params.baseCoin 	string 	No 	Base coin. Supports linear, inverse & option
params.settleCoin 	string 	No 	Settle coin. Supports linear, inverse & option
params.paginate 	boolean 	No 	default false, when true will automatically paginate by calling this endpoint multiple times

bybit.fetchPositions (symbols[, params])

fetchLeverage

fetch the set leverage for a market

Kind: instance method of bybit
Returns: object - a leverage structure

See: https://bybit-exchange.github.io/docs/v5/position
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.fetchLeverage (symbol[, params])

setMarginMode

set margin mode (account) or trade mode (symbol)

Kind: instance method of bybit
Returns: object - response from the exchange

See

    https://bybit-exchange.github.io/docs/v5/account/set-margin-mode
    https://bybit-exchange.github.io/docs/v5/position/cross-isolate

Param 	Type 	Required 	Description
marginMode 	string 	Yes 	account mode must be either [isolated, cross, portfolio], trade mode must be either [isolated, cross]
symbol 	string 	Yes 	unified market symbol of the market the position is held in, default is undefined
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.leverage 	string 	No 	the rate of leverage, is required if setting trade mode (symbol)

bybit.setMarginMode (marginMode, symbol[, params])

setLeverage

set the level of leverage for a market

Kind: instance method of bybit
Returns: object - response from the exchange

See: https://bybit-exchange.github.io/docs/v5/position/leverage
Param 	Type 	Required 	Description
leverage 	float 	Yes 	the rate of leverage
symbol 	string 	Yes 	unified market symbol
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.buyLeverage 	string 	No 	leverage for buy side
params.sellLeverage 	string 	No 	leverage for sell side

bybit.setLeverage (leverage, symbol[, params])

setPositionMode

set hedged to true or false for a market

Kind: instance method of bybit
Returns: object - response from the exchange

See: https://bybit-exchange.github.io/docs/v5/position/position-mode
Param 	Type 	Required 	Description
hedged 	bool 	Yes 	
symbol 	string 	Yes 	used for unified account with inverse market
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.setPositionMode (hedged, symbol[, params])

fetchOpenInterest

Retrieves the open interest of a derivative trading pair

Kind: instance method of bybit
Returns: object - an open interest structurehttps://docs.ccxt.com/#/?id=open-interest-structure

See: https://bybit-exchange.github.io/docs/v5/market/open-interest
Param 	Type 	Required 	Description
symbol 	string 	Yes 	Unified CCXT market symbol
params 	object 	No 	exchange specific parameters
params.interval 	string 	No 	5m, 15m, 30m, 1h, 4h, 1d
params.category 	string 	No 	"linear" or "inverse"

bybit.fetchOpenInterest (symbol[, params])

fetchOpenInterestHistory

Gets the total amount of unsettled contracts. In other words, the total number of contracts held in open positions

Kind: instance method of bybit
Returns: An array of open interest structures

See: https://bybit-exchange.github.io/docs/v5/market/open-interest
Param 	Type 	Required 	Description
symbol 	string 	Yes 	Unified market symbol
timeframe 	string 	Yes 	"5m", 15m, 30m, 1h, 4h, 1d
since 	int 	No 	Not used by Bybit
limit 	int 	No 	The number of open interest structures to return. Max 200, default 50
params 	object 	No 	Exchange specific parameters
params.paginate 	boolean 	No 	default false, when true will automatically paginate by calling this endpoint multiple times. See in the docs all the availble parameters

bybit.fetchOpenInterestHistory (symbol, timeframe[, since, limit, params])

fetchCrossBorrowRate

fetch the rate of interest to borrow a currency for margin trading

Kind: instance method of bybit
Returns: object - a borrow rate structure

See: https://bybit-exchange.github.io/docs/zh-TW/v5/spot-margin-normal/interest-quota
Param 	Type 	Required 	Description
code 	string 	Yes 	unified currency code
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.fetchCrossBorrowRate (code[, params])

fetchBorrowInterest

fetch the interest owed by the user for borrowing currency for margin trading

Kind: instance method of bybit
Returns: Array<object> - a list of borrow interest structures

See: https://bybit-exchange.github.io/docs/zh-TW/v5/spot-margin-normal/account-info
Param 	Type 	Required 	Description
code 	string 	Yes 	unified currency code
symbol 	string 	Yes 	unified market symbol when fetch interest in isolated markets
since 	number 	No 	the earliest time in ms to fetch borrrow interest for
limit 	number 	No 	the maximum number of structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.fetchBorrowInterest (code, symbol[, since, limit, params])

fetchBorrowRateHistory

retrieves a history of a currencies borrow interest rate at specific time slots

Kind: instance method of bybit
Returns: Array<object> - an array of borrow rate structures

See: https://bybit-exchange.github.io/docs/v5/spot-margin-uta/historical-interest
Param 	Type 	Required 	Description
code 	string 	Yes 	unified currency code
since 	int 	No 	timestamp for the earliest borrow rate
limit 	int 	No 	the maximum number of borrow rate structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.until 	int 	No 	the latest time in ms to fetch entries for

bybit.fetchBorrowRateHistory (code[, since, limit, params])

transfer

transfer currency internally between wallets on the same account

Kind: instance method of bybit
Returns: object - a transfer structure

See: https://bybit-exchange.github.io/docs/v5/asset/create-inter-transfer
Param 	Type 	Required 	Description
code 	string 	Yes 	unified currency code
amount 	float 	Yes 	amount to transfer
fromAccount 	string 	Yes 	account to transfer from
toAccount 	string 	Yes 	account to transfer to
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.transferId 	string 	No 	UUID, which is unique across the platform

bybit.transfer (code, amount, fromAccount, toAccount[, params])

fetchTransfers

fetch a history of internal transfers made on an account

Kind: instance method of bybit
Returns: Array<object> - a list of transfer structures

See: https://bybit-exchange.github.io/docs/v5/asset/inter-transfer-list
Param 	Type 	Required 	Description
code 	string 	Yes 	unified currency code of the currency transferred
since 	int 	No 	the earliest time in ms to fetch transfers for
limit 	int 	No 	the maximum number of transfer structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.until 	int 	No 	the latest time in ms to fetch entries for
params.paginate 	boolean 	No 	default false, when true will automatically paginate by calling this endpoint multiple times. See in the docs all the availble parameters

bybit.fetchTransfers (code[, since, limit, params])

borrowCrossMargin

create a loan to borrow margin

Kind: instance method of bybit
Returns: object - a margin loan structure

See: https://bybit-exchange.github.io/docs/v5/spot-margin-normal/borrow
Param 	Type 	Required 	Description
code 	string 	Yes 	unified currency code of the currency to borrow
amount 	float 	Yes 	the amount to borrow
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.borrowCrossMargin (code, amount[, params])

repayCrossMargin

repay borrowed margin and interest

Kind: instance method of bybit
Returns: object - a margin loan structure

See: https://bybit-exchange.github.io/docs/v5/spot-margin-normal/repay
Param 	Type 	Required 	Description
code 	string 	Yes 	unified currency code of the currency to repay
amount 	float 	Yes 	the amount to repay
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.repayCrossMargin (code, amount[, params])

fetchMarketLeverageTiers

retrieve information on the maximum leverage, and maintenance margin for trades of varying trade sizes for a single market

Kind: instance method of bybit
Returns: object - a leverage tiers structure

See: https://bybit-exchange.github.io/docs/v5/market/risk-limit
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.fetchMarketLeverageTiers (symbol[, params])

fetchTradingFee

fetch the trading fees for a market

Kind: instance method of bybit
Returns: object - a fee structure

See: https://bybit-exchange.github.io/docs/v5/account/fee-rate
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.fetchTradingFee (symbol[, params])

fetchTradingFees

fetch the trading fees for multiple markets

Kind: instance method of bybit
Returns: object - a dictionary of fee structures indexed by market symbols

See: https://bybit-exchange.github.io/docs/v5/account/fee-rate
Param 	Type 	Required 	Description
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.type 	string 	No 	market type, ['swap', 'option', 'spot']

bybit.fetchTradingFees ([params])

fetchDepositWithdrawFees

fetch deposit and withdraw fees

Kind: instance method of bybit
Returns: object - a list of fee structures

See: https://bybit-exchange.github.io/docs/v5/asset/coin-info
Param 	Type 	Required 	Description
codes 	Array<string> 	Yes 	list of unified currency codes
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.fetchDepositWithdrawFees (codes[, params])

fetchSettlementHistory

fetches historical settlement records

Kind: instance method of bybit
Returns: Array<object> - a list of [settlement history objects]

See: https://bybit-exchange.github.io/docs/v5/market/delivery-price
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol of the settlement history
since 	int 	No 	timestamp in ms
limit 	int 	No 	number of records
params 	object 	No 	exchange specific params
params.type 	string 	No 	market type, ['swap', 'option', 'spot']
params.subType 	string 	No 	market subType, ['linear', 'inverse']

bybit.fetchSettlementHistory (symbol[, since, limit, params])

fetchMySettlementHistory

fetches historical settlement records of the user

Kind: instance method of bybit
Returns: Array<object> - a list of [settlement history objects]

See: https://bybit-exchange.github.io/docs/v5/asset/delivery
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol of the settlement history
since 	int 	No 	timestamp in ms
limit 	int 	No 	number of records
params 	object 	No 	exchange specific params
params.type 	string 	No 	market type, ['swap', 'option', 'spot']
params.subType 	string 	No 	market subType, ['linear', 'inverse']

bybit.fetchMySettlementHistory (symbol[, since, limit, params])

fetchVolatilityHistory

fetch the historical volatility of an option market based on an underlying asset

Kind: instance method of bybit
Returns: Array<object> - a list of volatility history objects

See: https://bybit-exchange.github.io/docs/v5/market/iv
Param 	Type 	Required 	Description
code 	string 	Yes 	unified currency code
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.period 	int 	No 	the period in days to fetch the volatility for: 7,14,21,30,60,90,180,270

bybit.fetchVolatilityHistory (code[, params])

fetchGreeks

fetches an option contracts greeks, financial metrics used to measure the factors that affect the price of an options contract

Kind: instance method of bybit
Returns: object - a greeks structure

See: https://bybit-exchange.github.io/docs/api-explorer/v5/market/tickers
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to fetch greeks for
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.fetchGreeks (symbol[, params])

fetchMyLiquidations

retrieves the users liquidated positions

Kind: instance method of bybit
Returns: object - an array of liquidation structures

See: https://bybit-exchange.github.io/docs/api-explorer/v5/position/execution
Param 	Type 	Required 	Description
symbol 	string 	No 	unified CCXT market symbol
since 	int 	No 	the earliest time in ms to fetch liquidations for
limit 	int 	No 	the maximum number of liquidation structures to retrieve
params 	object 	No 	exchange specific parameters for the exchange API endpoint
params.type 	string 	No 	market type, ['swap', 'option', 'spot']
params.subType 	string 	No 	market subType, ['linear', 'inverse']
params.paginate 	boolean 	No 	default false, when true will automatically paginate by calling this endpoint multiple times. See in the docs all the available parameters

bybit.fetchMyLiquidations ([symbol, since, limit, params])

fetchLeverageTiers

retrieve information on the maximum leverage, for different trade sizes

Kind: instance method of bybit
Returns: object - a dictionary of leverage tiers structures, indexed by market symbols

See: https://bybit-exchange.github.io/docs/v5/market/risk-limit
Param 	Type 	Required 	Description
symbols 	Array<string> 	No 	a list of unified market symbols
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.subType 	string 	No 	market subType, ['linear', 'inverse'], default is 'linear'
params.paginate 	boolean 	No 	default false, when true will automatically paginate by calling this endpoint multiple times. See in the docs all the available parameters

bybit.fetchLeverageTiers ([symbols, params])

fetchFundingHistory

fetch the history of funding payments paid and received on this account

Kind: instance method of bybit
Returns: object - a funding history structure

See: https://bybit-exchange.github.io/docs/api-explorer/v5/position/execution
Param 	Type 	Required 	Description
symbol 	string 	No 	unified market symbol
since 	int 	No 	the earliest time in ms to fetch funding history for
limit 	int 	No 	the maximum number of funding history structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.paginate 	boolean 	No 	default false, when true will automatically paginate by calling this endpoint multiple times. See in the docs all the available parameters

bybit.fetchFundingHistory ([symbol, since, limit, params])

fetchOption

fetches option data that is commonly found in an option chain

Kind: instance method of bybit
Returns: object - an option chain structure

See: https://bybit-exchange.github.io/docs/v5/market/tickers
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.fetchOption (symbol[, params])

fetchOptionChain

fetches data for an underlying asset that is commonly found in an option chain

Kind: instance method of bybit
Returns: object - a list of option chain structures

See: https://bybit-exchange.github.io/docs/v5/market/tickers
Param 	Type 	Required 	Description
code 	string 	Yes 	base currency to fetch an option chain for
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.fetchOptionChain (code[, params])

fetchPositionsHistory

fetches historical positions

Kind: instance method of bybit
Returns: Array<object> - a list of position structures

See: https://bybit-exchange.github.io/docs/v5/position/close-pnl
Param 	Type 	Required 	Description
symbols 	Array<string> 	Yes 	a list of unified market symbols
since 	int 	No 	timestamp in ms of the earliest position to fetch, params["until"] - since <= 7 days
limit 	int 	No 	the maximum amount of records to fetch, default=50, max=100
params 	object 	Yes 	extra parameters specific to the exchange api endpoint
params.until 	int 	No 	timestamp in ms of the latest position to fetch, params["until"] - since <= 7 days
params.subType 	string 	No 	'linear' or 'inverse'

bybit.fetchPositionsHistory (symbols[, since, limit, params])

fetchConvertCurrencies

fetches all available currencies that can be converted

Kind: instance method of bybit
Returns: object - an associative dictionary of currencies

See: https://bybit-exchange.github.io/docs/v5/asset/convert/convert-coin-list
Param 	Type 	Required 	Description
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.accountType 	string 	No 	eb_convert_uta, eb_convert_spot, eb_convert_funding, eb_convert_inverse, or eb_convert_contract

bybit.fetchConvertCurrencies ([params])

fetchConvertQuote

fetch a quote for converting from one currency to another

Kind: instance method of bybit
Returns: object - a conversion structure

See: https://bybit-exchange.github.io/docs/v5/asset/convert/apply-quote
Param 	Type 	Required 	Description
fromCode 	string 	Yes 	the currency that you want to sell and convert from
toCode 	string 	Yes 	the currency that you want to buy and convert into
amount 	float 	No 	how much you want to trade in units of the from currency
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.accountType 	string 	No 	eb_convert_uta, eb_convert_spot, eb_convert_funding, eb_convert_inverse, or eb_convert_contract

bybit.fetchConvertQuote (fromCode, toCode[, amount, params])

createConvertTrade

convert from one currency to another

Kind: instance method of bybit
Returns: object - a conversion structure

See: https://bybit-exchange.github.io/docs/v5/asset/convert/confirm-quote
Param 	Type 	Required 	Description
id 	string 	Yes 	the id of the trade that you want to make
fromCode 	string 	Yes 	the currency that you want to sell and convert from
toCode 	string 	Yes 	the currency that you want to buy and convert into
amount 	float 	Yes 	how much you want to trade in units of the from currency
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.createConvertTrade (id, fromCode, toCode, amount[, params])

fetchConvertTrade

fetch the data for a conversion trade

Kind: instance method of bybit
Returns: object - a conversion structure

See: https://bybit-exchange.github.io/docs/v5/asset/convert/get-convert-result
Param 	Type 	Required 	Description
id 	string 	Yes 	the id of the trade that you want to fetch
code 	string 	No 	the unified currency code of the conversion trade
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.accountType 	string 	No 	eb_convert_uta, eb_convert_spot, eb_convert_funding, eb_convert_inverse, or eb_convert_contract

bybit.fetchConvertTrade (id[, code, params])

fetchConvertTradeHistory

fetch the users history of conversion trades

Kind: instance method of bybit
Returns: Array<object> - a list of conversion structures

See: https://bybit-exchange.github.io/docs/v5/asset/convert/get-convert-history
Param 	Type 	Required 	Description
code 	string 	No 	the unified currency code
since 	int 	No 	the earliest time in ms to fetch conversions for
limit 	int 	No 	the maximum number of conversion structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.accountType 	string 	No 	eb_convert_uta, eb_convert_spot, eb_convert_funding, eb_convert_inverse, or eb_convert_contract

bybit.fetchConvertTradeHistory ([code, since, limit, params])

fetchLongShortRatioHistory

fetches the long short ratio history for a unified market symbol

Kind: instance method of bybit
Returns: Array<object> - an array of long short ratio structures

See: https://bybit-exchange.github.io/docs/v5/market/long-short-ratio
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to fetch the long short ratio for
timeframe 	string 	No 	the period for the ratio, default is 24 hours
since 	int 	No 	the earliest time in ms to fetch ratios for
limit 	int 	No 	the maximum number of long short ratio structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.fetchLongShortRatioHistory (symbol[, timeframe, since, limit, params])

createOrderWs

create a trade order

Kind: instance method of bybit
Returns: object - an order structure

See

    https://bybit-exchange.github.io/docs/v5/order/create-order
    https://bybit-exchange.github.io/docs/v5/websocket/trade/guideline#createamendcancel-order

Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to create an order in
type 	string 	Yes 	'market' or 'limit'
side 	string 	Yes 	'buy' or 'sell'
amount 	float 	Yes 	how much of currency you want to trade in units of base currency
price 	float 	No 	the price at which the order is to be fulfilled, in units of the quote currency, ignored in market orders
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.timeInForce 	string 	No 	"GTC", "IOC", "FOK"
params.postOnly 	bool 	No 	true or false whether the order is post-only
params.reduceOnly 	bool 	No 	true or false whether the order is reduce-only
params.positionIdx 	string 	No 	contracts only 0 for one-way mode, 1 buy side of hedged mode, 2 sell side of hedged mode
params.isLeverage 	boolean 	No 	unified spot only false then spot trading true then margin trading
params.tpslMode 	string 	No 	contract only 'full' or 'partial'
params.mmp 	string 	No 	option only market maker protection
params.triggerDirection 	string 	No 	contract only the direction for trigger orders, 'above' or 'below'
params.triggerPrice 	float 	No 	The price at which a trigger order is triggered at
params.stopLossPrice 	float 	No 	The price at which a stop loss order is triggered at
params.takeProfitPrice 	float 	No 	The price at which a take profit order is triggered at
params.takeProfit 	object 	No 	takeProfit object in params containing the triggerPrice at which the attached take profit order will be triggered
params.takeProfit.triggerPrice 	float 	No 	take profit trigger price
params.stopLoss 	object 	No 	stopLoss object in params containing the triggerPrice at which the attached stop loss order will be triggered
params.stopLoss.triggerPrice 	float 	No 	stop loss trigger price
params.trailingAmount 	string 	No 	the quote amount to trail away from the current market price
params.trailingTriggerPrice 	string 	No 	the price to trigger a trailing order, default uses the price argument

bybit.createOrderWs (symbol, type, side, amount[, price, params])

editOrderWs

edit a trade order

Kind: instance method of bybit
Returns: object - an order structure

See

    https://bybit-exchange.github.io/docs/v5/order/amend-order
    https://bybit-exchange.github.io/docs/v5/websocket/trade/guideline#createamendcancel-order

Param 	Type 	Required 	Description
id 	string 	Yes 	cancel order id
symbol 	string 	Yes 	unified symbol of the market to create an order in
type 	string 	Yes 	'market' or 'limit'
side 	string 	Yes 	'buy' or 'sell'
amount 	float 	Yes 	how much of currency you want to trade in units of base currency
price 	float 	Yes 	the price at which the order is to be fulfilled, in units of the quote currency, ignored in market orders
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.triggerPrice 	float 	No 	The price that a trigger order is triggered at
params.stopLossPrice 	float 	No 	The price that a stop loss order is triggered at
params.takeProfitPrice 	float 	No 	The price that a take profit order is triggered at
params.takeProfit 	object 	No 	takeProfit object in params containing the triggerPrice that the attached take profit order will be triggered
params.takeProfit.triggerPrice 	float 	No 	take profit trigger price
params.stopLoss 	object 	No 	stopLoss object in params containing the triggerPrice that the attached stop loss order will be triggered
params.stopLoss.triggerPrice 	float 	No 	stop loss trigger price
params.triggerBy 	string 	No 	'IndexPrice', 'MarkPrice' or 'LastPrice', default is 'LastPrice', required if no initial value for triggerPrice
params.slTriggerBy 	string 	No 	'IndexPrice', 'MarkPrice' or 'LastPrice', default is 'LastPrice', required if no initial value for stopLoss
params.tpTriggerby 	string 	No 	'IndexPrice', 'MarkPrice' or 'LastPrice', default is 'LastPrice', required if no initial value for takeProfit

bybit.editOrderWs (id, symbol, type, side, amount, price[, params])

cancelOrderWs

cancels an open order

Kind: instance method of bybit
Returns: object - An order structure

See

    https://bybit-exchange.github.io/docs/v5/order/cancel-order
    https://bybit-exchange.github.io/docs/v5/websocket/trade/guideline#createamendcancel-order

Param 	Type 	Required 	Description
id 	string 	Yes 	order id
symbol 	string 	Yes 	unified symbol of the market the order was made in
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.trigger 	boolean 	No 	spot only whether the order is a trigger order
params.orderFilter 	string 	No 	spot only 'Order' or 'StopOrder' or 'tpslOrder'

bybit.cancelOrderWs (id, symbol[, params])

watchTicker

watches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market

Kind: instance method of bybit
Returns: object - a ticker structure

See

    https://bybit-exchange.github.io/docs/v5/websocket/public/ticker
    https://bybit-exchange.github.io/docs/v5/websocket/public/etp-ticker

Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to fetch the ticker for
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.watchTicker (symbol[, params])

watchTickers

watches a price ticker, a statistical calculation with the information calculated over the past 24 hours for all markets of a specific list

Kind: instance method of bybit
Returns: object - a ticker structure

See

    https://bybit-exchange.github.io/docs/v5/websocket/public/ticker
    https://bybit-exchange.github.io/docs/v5/websocket/public/etp-ticker

Param 	Type 	Required 	Description
symbols 	Array<string> 	Yes 	unified symbol of the market to fetch the ticker for
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.watchTickers (symbols[, params])

unWatchTickers

unWatches a price ticker

Kind: instance method of bybit
Returns: object - a ticker structure

See

    https://bybit-exchange.github.io/docs/v5/websocket/public/ticker
    https://bybit-exchange.github.io/docs/v5/websocket/public/etp-ticker

Param 	Type 	Required 	Description
symbols 	Array<string> 	Yes 	unified symbol of the market to fetch the ticker for
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.unWatchTickers (symbols[, params])

unWatchTicker

unWatches a price ticker

Kind: instance method of bybit
Returns: object - a ticker structure

See

    https://bybit-exchange.github.io/docs/v5/websocket/public/ticker
    https://bybit-exchange.github.io/docs/v5/websocket/public/etp-ticker

Param 	Type 	Required 	Description
symbols 	Array<string> 	Yes 	unified symbol of the market to fetch the ticker for
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.unWatchTicker (symbols[, params])

watchBidsAsks

watches best bid & ask for symbols

Kind: instance method of bybit
Returns: object - a ticker structure

See: https://bybit-exchange.github.io/docs/v5/websocket/public/orderbook
Param 	Type 	Required 	Description
symbols 	Array<string> 	Yes 	unified symbol of the market to fetch the ticker for
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.watchBidsAsks (symbols[, params])

watchOHLCV

watches historical candlestick data containing the open, high, low, and close price, and the volume of a market

Kind: instance method of bybit
Returns: Array<Array<int>> - A list of candles ordered as timestamp, open, high, low, close, volume

See

    https://bybit-exchange.github.io/docs/v5/websocket/public/kline
    https://bybit-exchange.github.io/docs/v5/websocket/public/etp-kline

Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to fetch OHLCV data for
timeframe 	string 	Yes 	the length of time each candle represents
since 	int 	No 	timestamp in ms of the earliest candle to fetch
limit 	int 	No 	the maximum amount of candles to fetch
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.watchOHLCV (symbol, timeframe[, since, limit, params])

watchOHLCVForSymbols

watches historical candlestick data containing the open, high, low, and close price, and the volume of a market

Kind: instance method of bybit
Returns: object - A list of candles ordered as timestamp, open, high, low, close, volume

See

    https://bybit-exchange.github.io/docs/v5/websocket/public/kline
    https://bybit-exchange.github.io/docs/v5/websocket/public/etp-kline

Param 	Type 	Required 	Description
symbolsAndTimeframes 	Array<Array<string>> 	Yes 	array of arrays containing unified symbols and timeframes to fetch OHLCV data for, example [['BTC/USDT', '1m'], ['LTC/USDT', '5m']]
since 	int 	No 	timestamp in ms of the earliest candle to fetch
limit 	int 	No 	the maximum amount of candles to fetch
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.watchOHLCVForSymbols (symbolsAndTimeframes[, since, limit, params])

unWatchOHLCVForSymbols

unWatches historical candlestick data containing the open, high, low, and close price, and the volume of a market

Kind: instance method of bybit
Returns: object - A list of candles ordered as timestamp, open, high, low, close, volume

See

    https://bybit-exchange.github.io/docs/v5/websocket/public/kline
    https://bybit-exchange.github.io/docs/v5/websocket/public/etp-kline

Param 	Type 	Required 	Description
symbolsAndTimeframes 	Array<Array<string>> 	Yes 	array of arrays containing unified symbols and timeframes to fetch OHLCV data for, example [['BTC/USDT', '1m'], ['LTC/USDT', '5m']]
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.unWatchOHLCVForSymbols (symbolsAndTimeframes[, params])

unWatchOHLCV

unWatches historical candlestick data containing the open, high, low, and close price, and the volume of a market

Kind: instance method of bybit
Returns: Array<Array<int>> - A list of candles ordered as timestamp, open, high, low, close, volume

See

    https://bybit-exchange.github.io/docs/v5/websocket/public/kline
    https://bybit-exchange.github.io/docs/v5/websocket/public/etp-kline

Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to fetch OHLCV data for
timeframe 	string 	Yes 	the length of time each candle represents
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.unWatchOHLCV (symbol, timeframe[, params])

watchOrderBook

watches information on open orders with bid (buy) and ask (sell) prices, volumes and other data

Kind: instance method of bybit
Returns: object - A dictionary of order book structures indexed by market symbols

See: https://bybit-exchange.github.io/docs/v5/websocket/public/orderbook
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to fetch the order book for
limit 	int 	No 	the maximum amount of order book entries to return.
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.watchOrderBook (symbol[, limit, params])

watchOrderBookForSymbols

watches information on open orders with bid (buy) and ask (sell) prices, volumes and other data

Kind: instance method of bybit
Returns: object - A dictionary of order book structures indexed by market symbols

See: https://bybit-exchange.github.io/docs/v5/websocket/public/orderbook
Param 	Type 	Required 	Description
symbols 	Array<string> 	Yes 	unified array of symbols
limit 	int 	No 	the maximum amount of order book entries to return.
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.watchOrderBookForSymbols (symbols[, limit, params])

unWatchOrderBookForSymbols

unsubscribe from the orderbook channel

Kind: instance method of bybit
Returns: object - A dictionary of order book structures indexed by market symbols

See: https://bybit-exchange.github.io/docs/v5/websocket/public/orderbook
Param 	Type 	Required 	Description
symbols 	Array<string> 	Yes 	unified symbol of the market to unwatch the trades for
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.limit 	int 	No 	orderbook limit, default is undefined

bybit.unWatchOrderBookForSymbols (symbols[, params])

unWatchOrderBook

unsubscribe from the orderbook channel

Kind: instance method of bybit
Returns: object - A dictionary of order book structures indexed by market symbols

See: https://bybit-exchange.github.io/docs/v5/websocket/public/orderbook
Param 	Type 	Required 	Description
symbol 	string 	Yes 	symbol of the market to unwatch the trades for
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.limit 	int 	No 	orderbook limit, default is undefined

bybit.unWatchOrderBook (symbol[, params])

watchTrades

watches information on multiple trades made in a market

Kind: instance method of bybit
Returns: Array<object> - a list of trade structures

See: https://bybit-exchange.github.io/docs/v5/websocket/public/trade
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol of the market trades were made in
since 	int 	No 	the earliest time in ms to fetch trades for
limit 	int 	No 	the maximum number of trade structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.watchTrades (symbol[, since, limit, params])

watchTradesForSymbols

get the list of most recent trades for a list of symbols

Kind: instance method of bybit
Returns: Array<object> - a list of trade structures

See: https://bybit-exchange.github.io/docs/v5/websocket/public/trade
Param 	Type 	Required 	Description
symbols 	Array<string> 	Yes 	unified symbol of the market to fetch trades for
since 	int 	No 	timestamp in ms of the earliest trade to fetch
limit 	int 	No 	the maximum amount of trades to fetch
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.watchTradesForSymbols (symbols[, since, limit, params])

unWatchTradesForSymbols

unsubscribe from the trades channel

Kind: instance method of bybit
Returns: any - status of the unwatch request

See: https://bybit-exchange.github.io/docs/v5/websocket/public/trade
Param 	Type 	Required 	Description
symbols 	Array<string> 	Yes 	unified symbol of the market to unwatch the trades for
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.unWatchTradesForSymbols (symbols[, params])

unWatchTrades

unsubscribe from the trades channel

Kind: instance method of bybit
Returns: any - status of the unwatch request

See: https://bybit-exchange.github.io/docs/v5/websocket/public/trade
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to unwatch the trades for
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.unWatchTrades (symbol[, params])

watchMyTrades

watches information on multiple trades made by the user

Kind: instance method of bybit
Returns: Array<object> - a list of order structures

See: https://bybit-exchange.github.io/docs/v5/websocket/private/execution
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol of the market orders were made in
since 	int 	No 	the earliest time in ms to fetch orders for
limit 	int 	No 	the maximum number of order structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.unifiedMargin 	boolean 	No 	use unified margin account

bybit.watchMyTrades (symbol[, since, limit, params])

unWatchMyTrades

unWatches information on multiple trades made by the user

Kind: instance method of bybit
Returns: Array<object> - a list of order structures

See: https://bybit-exchange.github.io/docs/v5/websocket/private/execution
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol of the market orders were made in
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.unifiedMargin 	boolean 	No 	use unified margin account

bybit.unWatchMyTrades (symbol[, params])

watchPositions

watch all open positions

Kind: instance method of bybit
Returns: Array<object> - a list of position structure

See: https://bybit-exchange.github.io/docs/v5/websocket/private/position
Param 	Type 	Required 	Description
symbols 	Array<string> 	No 	list of unified market symbols
since 	int 	No 	the earliest time in ms to fetch positions for
limit 	int 	No 	the maximum number of positions to retrieve
params 	object 	Yes 	extra parameters specific to the exchange API endpoint

bybit.watchPositions ([symbols, since, limit, params])

watchLiquidations

watch the public liquidations of a trading pair

Kind: instance method of bybit
Returns: object - an array of liquidation structures

See: https://bybit-exchange.github.io/docs/v5/websocket/public/liquidation
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified CCXT market symbol
since 	int 	No 	the earliest time in ms to fetch liquidations for
limit 	int 	No 	the maximum number of liquidation structures to retrieve
params 	object 	No 	exchange specific parameters for the bitmex api endpoint
params.method 	string 	No 	exchange specific method, supported: liquidation, allLiquidation

bybit.watchLiquidations (symbol[, since, limit, params])

watchOrders

watches information on multiple orders made by the user

Kind: instance method of bybit
Returns: Array<object> - a list of order structures

See: https://bybit-exchange.github.io/docs/v5/websocket/private/order
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol of the market orders were made in
since 	int 	No 	the earliest time in ms to fetch orders for
limit 	int 	No 	the maximum number of order structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.watchOrders (symbol[, since, limit, params])

unWatchOrders

unWatches information on multiple orders made by the user

Kind: instance method of bybit
Returns: Array<object> - a list of order structures

See: https://bybit-exchange.github.io/docs/v5/websocket/private/order
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol of the market orders were made in
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.unifiedMargin 	boolean 	No 	use unified margin account

bybit.unWatchOrders (symbol[, params])

watchBalance

watch balance and get the amount of funds available for trading or funds locked in orders

Kind: instance method of bybit
Returns: object - a balance structure

See: https://bybit-exchange.github.io/docs/v5/websocket/private/wallet
Param 	Type 	Required 	Description
params 	object 	No 	extra parameters specific to the exchange API endpoint

bybit.watchBalance ([params])

upbit

Kind: global class
Extends: Exchange

    fetchMarkets
    fetchBalance
    fetchOrderBooks
    fetchOrderBook
    fetchTickers
    fetchTicker
    fetchTrades
    fetchTradingFee
    fetchTradingFees
    fetchOHLCV
    createOrder
    cancelOrder
    fetchDeposits
    fetchDeposit
    fetchWithdrawals
    fetchWithdrawal
    fetchOpenOrders
    fetchClosedOrders
    fetchCanceledOrders
    fetchOrder
    fetchDepositAddresses
    fetchDepositAddress
    createDepositAddress
    withdraw
    watchTicker
    watchTickers
    watchTrades
    watchTradesForSymbols
    watchOrderBook
    watchOrders
    watchMyTrades
    watchBalance

fetchMarkets

retrieves data on all markets for upbit

Kind: instance method of upbit
Returns: Array<object> - an array of objects representing market data

See: https://docs.upbit.com/reference/%EB%A7%88%EC%BC%93-%EC%BD%94%EB%93%9C-%EC%A1%B0%ED%9A%8C
Param 	Type 	Required 	Description
params 	object 	No 	extra parameters specific to the exchange API endpoint

upbit.fetchMarkets ([params])

fetchBalance

query for balance and get the amount of funds available for trading or funds locked in orders

Kind: instance method of upbit
Returns: object - a balance structure

See: https://docs.upbit.com/reference/%EC%A0%84%EC%B2%B4-%EA%B3%84%EC%A2%8C-%EC%A1%B0%ED%9A%8C
Param 	Type 	Required 	Description
params 	object 	No 	extra parameters specific to the exchange API endpoint

upbit.fetchBalance ([params])

fetchOrderBooks

fetches information on open orders with bid (buy) and ask (sell) prices, volumes and other data for multiple markets

Kind: instance method of upbit
Returns: object - a dictionary of order book structures indexed by market symbol

See: https://docs.upbit.com/reference/%ED%98%B8%EA%B0%80-%EC%A0%95%EB%B3%B4-%EC%A1%B0%ED%9A%8C
Param 	Type 	Required 	Description
symbols 	Array<string>, undefined 	Yes 	list of unified market symbols, all symbols fetched if undefined, default is undefined
limit 	int 	No 	not used by upbit fetchOrderBooks ()
params 	object 	No 	extra parameters specific to the exchange API endpoint

upbit.fetchOrderBooks (symbols[, limit, params])

fetchOrderBook

fetches information on open orders with bid (buy) and ask (sell) prices, volumes and other data

Kind: instance method of upbit
Returns: object - A dictionary of order book structures indexed by market symbols

See: https://docs.upbit.com/reference/%ED%98%B8%EA%B0%80-%EC%A0%95%EB%B3%B4-%EC%A1%B0%ED%9A%8C
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to fetch the order book for
limit 	int 	No 	the maximum amount of order book entries to return
params 	object 	No 	extra parameters specific to the exchange API endpoint

upbit.fetchOrderBook (symbol[, limit, params])

fetchTickers

fetches price tickers for multiple markets, statistical information calculated over the past 24 hours for each market

Kind: instance method of upbit
Returns: object - a dictionary of ticker structures

See: https://docs.upbit.com/reference/ticker%ED%98%84%EC%9E%AC%EA%B0%80-%EC%A0%95%EB%B3%B4
Param 	Type 	Required 	Description
symbols 	Array<string>, undefined 	Yes 	unified symbols of the markets to fetch the ticker for, all market tickers are returned if not assigned
params 	object 	No 	extra parameters specific to the exchange API endpoint

upbit.fetchTickers (symbols[, params])

fetchTicker

fetches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market

Kind: instance method of upbit
Returns: object - a ticker structure

See: https://docs.upbit.com/reference/ticker%ED%98%84%EC%9E%AC%EA%B0%80-%EC%A0%95%EB%B3%B4
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to fetch the ticker for
params 	object 	No 	extra parameters specific to the exchange API endpoint

upbit.fetchTicker (symbol[, params])

fetchTrades

get the list of most recent trades for a particular symbol

Kind: instance method of upbit
Returns: Array<Trade> - a list of trade structures

See: https://docs.upbit.com/reference/%EC%B5%9C%EA%B7%BC-%EC%B2%B4%EA%B2%B0-%EB%82%B4%EC%97%AD
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to fetch trades for
since 	int 	No 	timestamp in ms of the earliest trade to fetch
limit 	int 	No 	the maximum amount of trades to fetch
params 	object 	No 	extra parameters specific to the exchange API endpoint

upbit.fetchTrades (symbol[, since, limit, params])

fetchTradingFee

fetch the trading fees for a market

Kind: instance method of upbit
Returns: object - a fee structure

See: https://docs.upbit.com/reference/%EC%A3%BC%EB%AC%B8-%EA%B0%80%EB%8A%A5-%EC%A0%95%EB%B3%B4
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol
params 	object 	No 	extra parameters specific to the exchange API endpoint

upbit.fetchTradingFee (symbol[, params])

fetchTradingFees

fetch the trading fees for markets

Kind: instance method of upbit
Returns: object - a trading fee structure
Param 	Type 	Required 	Description
params 	object 	No 	extra parameters specific to the exchange API endpoint

upbit.fetchTradingFees ([params])

fetchOHLCV

fetches historical candlestick data containing the open, high, low, and close price, and the volume of a market

Kind: instance method of upbit
Returns: Array<Array<int>> - A list of candles ordered as timestamp, open, high, low, close, volume

See: https://docs.upbit.com/reference/%EB%B6%84minute-%EC%BA%94%EB%93%A4-1
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to fetch OHLCV data for
timeframe 	string 	Yes 	the length of time each candle represents
since 	int 	No 	timestamp in ms of the earliest candle to fetch
limit 	int 	No 	the maximum amount of candles to fetch
params 	object 	No 	extra parameters specific to the exchange API endpoint

upbit.fetchOHLCV (symbol, timeframe[, since, limit, params])

createOrder

create a trade order

Kind: instance method of upbit
Returns: object - an order structure

See

    https://docs.upbit.com/reference/%EC%A3%BC%EB%AC%B8%ED%95%98%EA%B8%B0
    https://global-docs.upbit.com/reference/order

Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to create an order in
type 	string 	Yes 	supports 'market' and 'limit'. if params.ordType is set to best, a best-type order will be created regardless of the value of type.
side 	string 	Yes 	'buy' or 'sell'
amount 	float 	Yes 	how much you want to trade in units of the base currency
price 	float 	No 	the price at which the order is to be fulfilled, in units of the quote currency, ignored in market orders
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.cost 	float 	No 	for market buy and best buy orders, the quote quantity that can be used as an alternative for the amount
params.ordType 	string 	No 	this field can be used to place a ‘best’ type order
params.timeInForce 	string 	No 	'IOC' or 'FOK'. only for limit or best type orders. this field is required when the order type is 'best'.

upbit.createOrder (symbol, type, side, amount[, price, params])

cancelOrder

cancels an open order

Kind: instance method of upbit
Returns: object - An order structure

See: https://docs.upbit.com/reference/%EC%A3%BC%EB%AC%B8-%EC%B7%A8%EC%86%8C
Param 	Type 	Required 	Description
id 	string 	Yes 	order id
symbol 	string 	Yes 	not used by upbit cancelOrder ()
params 	object 	No 	extra parameters specific to the exchange API endpoint

upbit.cancelOrder (id, symbol[, params])

fetchDeposits

fetch all deposits made to an account

Kind: instance method of upbit
Returns: Array<object> - a list of transaction structures

See: https://docs.upbit.com/reference/%EC%9E%85%EA%B8%88-%EB%A6%AC%EC%8A%A4%ED%8A%B8-%EC%A1%B0%ED%9A%8C
Param 	Type 	Required 	Description
code 	string 	Yes 	unified currency code
since 	int 	No 	the earliest time in ms to fetch deposits for
limit 	int 	No 	the maximum number of deposits structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint

upbit.fetchDeposits (code[, since, limit, params])

fetchDeposit

fetch information on a deposit

Kind: instance method of upbit
Returns: object - a transaction structure

See: https://global-docs.upbit.com/reference/individual-deposit-inquiry
Param 	Type 	Required 	Description
id 	string 	Yes 	the unique id for the deposit
code 	string 	No 	unified currency code of the currency deposited
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.txid 	string 	No 	withdrawal transaction id, the id argument is reserved for uuid

upbit.fetchDeposit (id[, code, params])

fetchWithdrawals

fetch all withdrawals made from an account

Kind: instance method of upbit
Returns: Array<object> - a list of transaction structures

See: https://docs.upbit.com/reference/%EC%A0%84%EC%B2%B4-%EC%B6%9C%EA%B8%88-%EC%A1%B0%ED%9A%8C
Param 	Type 	Required 	Description
code 	string 	Yes 	unified currency code
since 	int 	No 	the earliest time in ms to fetch withdrawals for
limit 	int 	No 	the maximum number of withdrawals structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint

upbit.fetchWithdrawals (code[, since, limit, params])

fetchWithdrawal

fetch data on a currency withdrawal via the withdrawal id

Kind: instance method of upbit
Returns: object - a transaction structure

See: https://global-docs.upbit.com/reference/individual-withdrawal-inquiry
Param 	Type 	Required 	Description
id 	string 	Yes 	the unique id for the withdrawal
code 	string 	No 	unified currency code of the currency withdrawn
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.txid 	string 	No 	withdrawal transaction id, the id argument is reserved for uuid

upbit.fetchWithdrawal (id[, code, params])

fetchOpenOrders

fetch all unfilled currently open orders

Kind: instance method of upbit
Returns: Array<Order> - a list of order structures

See: https://global-docs.upbit.com/reference/open-order
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol
since 	int 	No 	the earliest time in ms to fetch open orders for
limit 	int 	No 	the maximum number of open order structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.state 	string 	No 	default is 'wait', set to 'watch' for stop limit orders

upbit.fetchOpenOrders (symbol[, since, limit, params])

fetchClosedOrders

fetches information on multiple closed orders made by the user

Kind: instance method of upbit
Returns: Array<Order> - a list of order structures

See: https://global-docs.upbit.com/reference/closed-order
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol of the market orders were made in
since 	int 	No 	the earliest time in ms to fetch orders for
limit 	int 	No 	the maximum number of order structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.until 	int 	No 	timestamp in ms of the latest order

upbit.fetchClosedOrders (symbol[, since, limit, params])

fetchCanceledOrders

fetches information on multiple canceled orders made by the user

Kind: instance method of upbit
Returns: object - a list of order structures

See: https://global-docs.upbit.com/reference/closed-order
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol of the market orders were made in
since 	int 	No 	timestamp in ms of the earliest order, default is undefined
limit 	int 	No 	max number of orders to return, default is undefined
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.until 	int 	No 	timestamp in ms of the latest order

upbit.fetchCanceledOrders (symbol[, since, limit, params])

fetchOrder

fetches information on an order made by the user

Kind: instance method of upbit
Returns: object - An order structure

See: https://docs.upbit.com/reference/%EA%B0%9C%EB%B3%84-%EC%A3%BC%EB%AC%B8-%EC%A1%B0%ED%9A%8C
Param 	Type 	Required 	Description
id 	string 	Yes 	order id
symbol 	string 	Yes 	not used by upbit fetchOrder
params 	object 	No 	extra parameters specific to the exchange API endpoint

upbit.fetchOrder (id, symbol[, params])

fetchDepositAddresses

fetch deposit addresses for multiple currencies and chain types

Kind: instance method of upbit
Returns: object - a list of address structures

See: https://docs.upbit.com/reference/%EC%A0%84%EC%B2%B4-%EC%9E%85%EA%B8%88-%EC%A3%BC%EC%86%8C-%EC%A1%B0%ED%9A%8C
Param 	Type 	Required 	Description
codes 	Array<string>, undefined 	Yes 	list of unified currency codes, default is undefined
params 	object 	No 	extra parameters specific to the exchange API endpoint

upbit.fetchDepositAddresses (codes[, params])

fetchDepositAddress

fetch the deposit address for a currency associated with this account

Kind: instance method of upbit
Returns: object - an address structure

See: https://docs.upbit.com/reference/%EC%A0%84%EC%B2%B4-%EC%9E%85%EA%B8%88-%EC%A3%BC%EC%86%8C-%EC%A1%B0%ED%9A%8C
Param 	Type 	Required 	Description
code 	string 	Yes 	unified currency code
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.network 	string 	Yes 	deposit chain, can view all chains via this.publicGetWalletAssets, default is eth, unless the currency has a default chain within this.options['networks']

upbit.fetchDepositAddress (code[, params])

createDepositAddress

create a currency deposit address

Kind: instance method of upbit
Returns: object - an address structure

See: https://docs.upbit.com/reference/%EC%9E%85%EA%B8%88-%EC%A3%BC%EC%86%8C-%EC%83%9D%EC%84%B1-%EC%9A%94%EC%B2%AD
Param 	Type 	Required 	Description
code 	string 	Yes 	unified currency code of the currency for the deposit address
params 	object 	No 	extra parameters specific to the exchange API endpoint

upbit.createDepositAddress (code[, params])

withdraw

make a withdrawal

Kind: instance method of upbit
Returns: object - a transaction structure

See

    https://docs.upbit.com/reference/디지털자산-출금하기
    https://docs.upbit.com/reference/%EC%9B%90%ED%99%94-%EC%B6%9C%EA%B8%88%ED%95%98%EA%B8%B0

Param 	Type 	Required 	Description
code 	string 	Yes 	unified currency code
amount 	float 	Yes 	the amount to withdraw
address 	string 	Yes 	the address to withdraw to
tag 	string 	Yes 	
params 	object 	No 	extra parameters specific to the exchange API endpoint

upbit.withdraw (code, amount, address, tag[, params])

watchTicker

watches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market

Kind: instance method of upbit
Returns: object - a ticker structure

See: https://global-docs.upbit.com/reference/websocket-ticker
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to fetch the ticker for
params 	object 	No 	extra parameters specific to the exchange API endpoint

upbit.watchTicker (symbol[, params])

watchTickers

watches a price ticker, a statistical calculation with the information calculated over the past 24 hours for all markets of a specific list

Kind: instance method of upbit
Returns: object - a ticker structure

See: https://global-docs.upbit.com/reference/websocket-ticker
Param 	Type 	Required 	Description
symbols 	Array<string> 	Yes 	unified symbol of the market to fetch the ticker for
params 	object 	No 	extra parameters specific to the exchange API endpoint

upbit.watchTickers (symbols[, params])

watchTrades

get the list of most recent trades for a particular symbol

Kind: instance method of upbit
Returns: Array<object> - a list of trade structures

See: https://global-docs.upbit.com/reference/websocket-trade
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to fetch trades for
since 	int 	No 	timestamp in ms of the earliest trade to fetch
limit 	int 	No 	the maximum amount of trades to fetch
params 	object 	No 	extra parameters specific to the exchange API endpoint

upbit.watchTrades (symbol[, since, limit, params])

watchTradesForSymbols

get the list of most recent trades for a list of symbols

Kind: instance method of upbit
Returns: Array<object> - a list of trade structures

See: https://global-docs.upbit.com/reference/websocket-trade
Param 	Type 	Required 	Description
symbols 	Array<string> 	Yes 	unified symbol of the market to fetch trades for
since 	int 	No 	timestamp in ms of the earliest trade to fetch
limit 	int 	No 	the maximum amount of trades to fetch
params 	object 	No 	extra parameters specific to the exchange API endpoint

upbit.watchTradesForSymbols (symbols[, since, limit, params])

watchOrderBook

watches information on open orders with bid (buy) and ask (sell) prices, volumes and other data

Kind: instance method of upbit
Returns: object - A dictionary of order book structures indexed by market symbols

See: https://global-docs.upbit.com/reference/websocket-orderbook
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to fetch the order book for
limit 	int 	No 	the maximum amount of order book entries to return
params 	object 	No 	extra parameters specific to the exchange API endpoint

upbit.watchOrderBook (symbol[, limit, params])

watchOrders

watches information on multiple orders made by the user

Kind: instance method of upbit
Returns: Array<object> - a list of order structures

See: https://global-docs.upbit.com/reference/websocket-myorder
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol of the market orders were made in
since 	int 	No 	the earliest time in ms to fetch orders for
limit 	int 	No 	the maximum number of order structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint

upbit.watchOrders (symbol[, since, limit, params])

watchMyTrades

watches information on multiple trades made by the user

Kind: instance method of upbit
Returns: Array<object> - a list of trade structures

See: https://global-docs.upbit.com/reference/websocket-myorder
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol of the market orders were made in
since 	int 	No 	the earliest time in ms to fetch orders for
limit 	int 	No 	the maximum number of order structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint

upbit.watchMyTrades (symbol[, since, limit, params])

watchBalance

query for balance and get the amount of funds available for trading or funds locked in orders

Kind: instance method of upbit
Returns: object - a balance structure

See: https://global-docs.upbit.com/reference/websocket-myasset
Param 	Type 	Required 	Description
params 	object 	No 	extra parameters specific to the exchange API endpoint

upbit.watchBalance ([params])