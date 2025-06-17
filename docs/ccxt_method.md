addMargin

add margin

Kind: instance
Returns: object - a margin structure
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol
amount 	float 	Yes 	amount of margin to add
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    ascendex
    binance
    bitget
    coincatch
    coinex
    delta
    digifinex
    exmo
    gate
    hitbtc
    hyperliquid
    kucoinfutures
    mexc
    okx
    poloniex
    woo
    xt

borrowCrossMargin

create a loan to borrow margin

Kind: instance
Returns: object - a margin loan structure
Param 	Type 	Required 	Description
code 	string 	Yes 	unified currency code of the currency to borrow
amount 	float 	Yes 	the amount to borrow
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.portfolioMargin 	boolean 	No 	set to true if you would like to borrow margin in a portfolio margin account
Supported exchanges

    binance
    bitget
    bybit
    coinmetro
    htx
    kucoin
    okx

borrowIsolatedMargin

create a loan to borrow margin

Kind: instance
Returns: object - a margin loan structure
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol, required for isolated margin
code 	string 	Yes 	unified currency code of the currency to borrow
amount 	float 	Yes 	the amount to borrow
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    binance
    bitget
    bitmart
    coinex
    gate
    htx
    kucoin

borrowMargin

create a loan to borrow margin

Kind: instance
Returns: object - a margin loan structure
Param 	Type 	Required 	Description
code 	string 	Yes 	unified currency code of the currency to borrow
amount 	float 	Yes 	the amount to borrow
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.rate 	string 	No 	'0.0002' or '0.002' extra parameter required for isolated margin
params.unifiedAccount 	boolean 	No 	set to true for borrowing in the unified account
Supported exchanges

    gate

calculatePricePrecision

Helper function to calculate the Hyperliquid DECIMAL_PLACES price precision

Kind: instance
Returns: int - The calculated price precision
Param 	Type 	Description
price 	float 	the price to use in the calculation
amountPrecision 	int 	the amountPrecision to use in the calculation
maxDecimals 	int 	the maxDecimals to use in the calculation
Supported exchanges

    hyperliquid

cancelAllOrders

cancel all open orders in a market

Kind: instance
Returns: Array<object> - a list of order structures
Param 	Type 	Required 	Description
symbol 	string 	Yes 	alpaca cancelAllOrders cannot setting symbol, it will cancel all open orders
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    alpaca
    apex
    ascendex
    bigone
    binance
    bingx
    bitfinex
    bitget
    bitmart
    bitmex
    bitopro
    bitrue
    bitso
    bitstamp
    bitteam
    bitvavo
    blockchaincom
    bybit
    cex
    coinbaseexchange
    coinbaseinternational
    coincatch
    coinex
    coinlist
    coinsph
    cryptocom
    defx
    delta
    deribit
    derive
    gate
    hashkey
    hitbtc
    hollaex
    htx
    huobijp
    idex
    kraken
    krakenfutures
    kucoin
    kucoinfutures
    latoken
    lbank
    mexc
    ndax
    oceanex
    onetrading
    oxfun
    paradex
    phemex
    poloniex
    tradeogre
    vertex
    whitebit
    woo
    woofipro
    xt

cancelAllOrdersAfter

dead man's switch, cancel all orders after the given timeout

Kind: instance
Returns: object - the api result
Param 	Type 	Required 	Description
timeout 	number 	Yes 	time in milliseconds, 0 represents cancel the timer
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.type 	string 	No 	spot or swap market
Supported exchanges

    bingx
    bitmex
    bybit
    htx
    hyperliquid
    kraken
    krakenfutures
    okx
    whitebit
    woo

cancelAllOrdersWs

cancel all open orders in a market

Kind: instance
Returns: Array<object> - a list of order structures
Param 	Type 	Required 	Description
symbol 	string 	No 	unified market symbol of the market to cancel orders in
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    binance
    bitvavo
    cryptocom
    gate
    okx

cancelOrder

cancels an open order

Kind: instance
Returns: object - An order structure
Param 	Type 	Required 	Description
id 	string 	Yes 	order id
symbol 	string 	Yes 	unified symbol of the market the order was made in
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    alpaca
    apex
    ascendex
    bigone
    binance
    bingx
    bit2c
    bitbank
    bitbns
    bitfinex
    bitflyer
    bitget
    bithumb
    bitmart
    bitmex
    bitopro
    bitrue
    bitso
    bitstamp
    bitteam
    bitvavo
    bl3p
    blockchaincom
    blofin
    btcalpha
    btcbox
    btcmarkets
    btcturk
    bybit
    cex
    coinbase
    coinbaseexchange
    coinbaseinternational
    coincatch
    coincheck
    coinex
    coinlist
    coinmate
    coinmetro
    coinone
    coinsph
    coinspot
    cryptocom
    cryptomus
    defx
    delta
    deribit
    derive
    digifinex
    ellipx
    exmo
    gate
    gemini
    hashkey
    hitbtc
    hollaex
    htx
    huobijp
    hyperliquid
    idex
    independentreserve
    indodax
    kraken
    krakenfutures
    kucoin
    kucoinfutures
    kuna
    latoken
    lbank
    luno
    mercado
    mexc
    ndax
    novadax
    oceanex
    okcoin
    okx
    onetrading
    oxfun
    p2b
    paradex
    paymium
    phemex
    probit
    timex
    tokocrypto
    tradeogre
    upbit
    vertex
    wavesexchange
    whitebit
    woo
    woofipro
    xt
    yobit
    zaif
    zonda

cancelOrderWs

cancel multiple orders

Kind: instance
Returns: object - an list of order structures
Param 	Type 	Required 	Description
id 	string 	Yes 	order id
symbol 	string 	No 	unified market symbol, default is undefined
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.cancelRestrictions 	string, undefined 	No 	Supported values: ONLY_NEW - Cancel will succeed if the order status is NEW. ONLY_PARTIALLY_FILLED - Cancel will succeed if order status is PARTIALLY_FILLED.
Supported exchanges

    binance
    bitvavo
    bybit
    cex
    cryptocom
    gate
    okx
    oxfun

cancelOrders

cancel multiple orders

Kind: instance
Returns: object - an list of order structures
Param 	Type 	Required 	Description
ids 	Array<string> 	Yes 	order ids
symbol 	string 	No 	unified market symbol
params 	object 	No 	extra parameters specific to the exchange API endpoint EXCHANGE SPECIFIC PARAMETERS
params.origClientOrderIdList 	Array<string> 	No 	max length 10 e.g. ["my_id_1","my_id_2"], encode the double quotes. No space after comma
params.recvWindow 	Array<int> 	No 	
Supported exchanges

    binance
    bingx
    bitfinex
    bitget
    bitmart
    bitmex
    bitopro
    bitso
    blofin
    btcmarkets
    bybit
    coinbase
    coincatch
    coinex
    coinlist
    cryptocom
    digifinex
    gate
    hashkey
    htx
    huobijp
    hyperliquid
    kraken
    krakenfutures
    kucoinfutures
    kuna
    mexc
    oceanex
    okcoin
    okx
    onetrading
    oxfun
    timex
    vertex
    woofipro
    xt

cancelOrdersForSymbols

cancel multiple orders for multiple symbols

Kind: instance
Returns: object - an list of order structures
Param 	Type 	Required 	Description
orders 	Array<CancellationRequest> 	Yes 	list of order ids with symbol, example [{"id": "a", "symbol": "BTC/USDT"}, {"id": "b", "symbol": "ETH/USDT"}]
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    bybit
    cryptocom
    gate
    hyperliquid
    okx

cancelOrdersWs

cancel multiple orders

Kind: instance
Returns: object - a list of order structures
Param 	Type 	Required 	Description
ids 	Array<string> 	Yes 	order ids
symbol 	string 	Yes 	not used by cex cancelOrders()
params 	object 	No 	extra parameters specific to the cex api endpoint
Supported exchanges

    cex
    okx
    oxfun

closeAllPositions

closes all open positions for a market type

Kind: instance
Returns: Array<object> - A list of position structures
Param 	Type 	Required 	Description
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.productType 	string 	No 	'USDT-FUTURES', 'USDC-FUTURES', 'COIN-FUTURES', 'SUSDT-FUTURES', 'SUSDC-FUTURES' or 'SCOIN-FUTURES'
Supported exchanges

    bitget
    defx
    delta

closePosition

closes open positions for a market

Kind: instance
Returns: object - an order structure
Param 	Type 	Required 	Description
symbol 	string 	Yes 	Unified CCXT market symbol
side 	string 	No 	not used by bingx
params 	object 	No 	extra parameters specific to the bingx api endpoint
params.positionId 	string, undefined 	No 	the id of the position you would like to close
Supported exchanges

    bingx
    bitget
    blofin
    coinbase
    coinex
    coinmetro
    defx
    gate
    hitbtc
    kucoinfutures
    okx

closePositions

closes open positions for a market

Kind: instance
Returns: Array<object> - a list of position structures
Param 	Type 	Required 	Description
params 	object 	No 	extra parameters specific to the bingx api endpoint
params.recvWindow 	string 	No 	request valid time window value
Supported exchanges

    bitget
    cryptocom
    htx

createConvertTrade

convert from one currency to another

Kind: instance
Returns: object - a conversion structure
Param 	Type 	Required 	Description
id 	string 	Yes 	the id of the trade that you want to make
fromCode 	string 	Yes 	the currency that you want to sell and convert from
toCode 	string 	Yes 	the currency that you want to buy and convert into
amount 	float 	No 	how much you want to trade in units of the from currency
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    binance
    bitget
    bybit
    coinbase
    okx
    phemex
    whitebit
    woo

createDepositAddress

create a currency deposit address

Kind: instance
Returns: object - an address structure
Param 	Type 	Required 	Description
code 	string 	Yes 	unified currency code of the currency for the deposit address
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    bitfinex
    bl3p
    coinbase
    coinbaseexchange
    coinbaseinternational
    coinex
    deribit
    gemini
    hitbtc
    kraken
    kucoin
    kuna
    luno
    mexc
    ndax
    paymium
    poloniex
    upbit
    whitebit
    yobit

createGiftCode

create gift code

Kind: instance
Returns: object - The gift code id, code, currency and amount
Param 	Type 	Required 	Description
code 	string 	Yes 	gift code
amount 	float 	Yes 	amount of currency for the gift
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    binance

createMarkeSellOrderWithCost

create a market sell order by providing the symbol and cost

Kind: instance
Returns: object - an order structure
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to create an order in
cost 	float 	Yes 	how much you want to trade in units of the quote currency
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    bybit

createMarketBuyOrderWithCost

create a market buy order by providing the symbol and cost

Kind: instance
Returns: object - an order structure
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to create an order in
cost 	float 	Yes 	how much you want to trade in units of the quote currency
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    alpaca
    bigone
    binance
    bingx
    bitget
    bitmart
    bitrue
    bybit
    coinbase
    coincatch
    coinex
    digifinex
    exmo
    gate
    hashkey
    htx
    huobijp
    kraken
    kucoin
    lbank
    mexc
    okcoin
    okx
    oxfun
    whitebit
    woo
    xt

createMarketOrderWithCost

create a market order by providing the symbol, side and cost

Kind: instance
Returns: object - an order structure
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to create an order in
side 	string 	Yes 	'buy' or 'sell'
cost 	float 	Yes 	how much you want to trade in units of the quote currency
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    alpaca
    binance
    bingx
    exmo
    kraken
    kucoin
    whitebit

createMarketSellOrderWithCost

create a market sell order by providing the symbol and cost

Kind: instance
Returns: object - an order structure
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to create an order in
cost 	float 	Yes 	how much you want to trade in units of the quote currency
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    alpaca
    binance
    bingx
    exmo
    kucoin
    mexc
    okx
    woo

createOrder

create a trade order

Kind: instance
Returns: object - an order structure
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to create an order in
type 	string 	Yes 	'market', 'limit' or 'stop_limit'
side 	string 	Yes 	'buy' or 'sell'
amount 	float 	Yes 	how much of currency you want to trade in units of base currency
price 	float 	No 	the price at which the order is to be fulfilled, in units of the quote currency, ignored in market orders
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.triggerPrice 	float 	No 	The price at which a trigger order is triggered at
params.cost 	float 	No 	market orders only the cost of the order in units of the quote currency
Supported exchanges

    alpaca
    apex
    ascendex
    bigone
    binance
    bingx
    bit2c
    bitbank
    bitbns
    bitfinex
    bitflyer
    bitget
    bithumb
    bitmart
    bitmex
    bitopro
    bitrue
    bitso
    bitstamp
    bitteam
    bitvavo
    bl3p
    blockchaincom
    blofin
    btcalpha
    btcbox
    btcmarkets
    btcturk
    bybit
    cex
    coinbase
    coinbaseexchange
    coinbaseinternational
    coincatch
    coincheck
    coinex
    coinlist
    coinmate
    coinmetro
    coinone
    coinsph
    coinspot
    cryptocom
    cryptomus
    defx
    delta
    deribit
    derive
    digifinex
    ellipx
    exmo
    gate
    gemini
    hashkey
    hitbtc
    hollaex
    htx
    huobijp
    hyperliquid
    idex
    independentreserve
    indodax
    kraken
    krakenfutures
    kucoin
    kucoinfutures
    kuna
    latoken
    lbank
    luno
    mercado
    mexc
    ndax
    novadax
    oceanex
    okcoin
    okx
    onetrading
    oxfun
    p2b
    paradex
    paymium
    phemex
    poloniex
    probit
    timex
    tokocrypto
    tradeogre
    upbit
    vertex
    wavesexchange
    whitebit
    woo
    woofipro
    xt
    yobit
    zaif
    zonda

createOrderWithTakeProfitAndStopLoss

swap markets only create an order with a stop loss or take profit attached (type 3)

Kind: instance
Returns: object - an order structure
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to create an order in
type 	string 	Yes 	'market' or 'limit'
side 	string 	Yes 	'buy' or 'sell'
amount 	float 	Yes 	how much you want to trade in units of the base currency or the number of contracts
price 	float 	No 	the price to fulfill the order, in units of the quote currency, ignored in market orders
takeProfit 	float 	No 	the take profit price, in units of the quote currency
stopLoss 	float 	No 	the stop loss price, in units of the quote currency
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    coincatch

createOrderWs

create a trade order

Kind: instance
Returns: object - an order structure
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to create an order in
type 	string 	Yes 	'market' or 'limit'
side 	string 	Yes 	'buy' or 'sell'
amount 	float 	Yes 	how much of currency you want to trade in units of base currency
price 	float, undefined 	No 	the price at which the order is to be fulfilled, in units of the quote currency, ignored in market orders
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.test 	boolean 	Yes 	test order, default false
params.returnRateLimits 	boolean 	Yes 	set to true to return rate limit information, default false
Supported exchanges

    binance
    bitvavo
    bybit
    cex
    cryptocom
    gate
    hyperliquid
    okx
    oxfun

createOrders

create a list of trade orders

Kind: instance
Returns: object - an order structure
Param 	Type 	Required 	Description
orders 	Array 	Yes 	list of orders to create, each object should contain the parameters required by createOrder, namely symbol, type, side, amount, price and params
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.timeInForce 	string 	No 	"GTC", "IOC", "FOK", or "PO"
params.postOnly 	bool 	No 	true or false
params.triggerPrice 	float 	No 	the price at which a trigger order is triggered at
Supported exchanges

    ascendex
    binance
    bingx
    bitfinex
    bitget
    bitmart
    blofin
    bybit
    coincatch
    coinex
    cryptocom
    digifinex
    gate
    hashkey
    htx
    hyperliquid
    krakenfutures
    kucoin
    kucoinfutures
    mexc
    okx
    oxfun
    woofipro

createOrdersRequest

create a list of trade orders

Kind: instance
Returns: object - an order structure
Param 	Type 	Description
orders 	Array 	list of orders to create, each object should contain the parameters required by createOrder, namely symbol, type, side, amount, price and params
Supported exchanges

    hyperliquid

createOrdersWs

create a list of trade orders

Kind: instance
Returns: object - an order structure
Param 	Type 	Required 	Description
orders 	Array 	Yes 	list of orders to create, each object should contain the parameters required by createOrder, namely symbol, type, side, amount, price and params
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    gate
    hyperliquid

createSpotOrder

create a trade order on spot market

Kind: instance
Returns: object - an order structure
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to create an order in
type 	string 	Yes 	'market' or 'limit'
side 	string 	Yes 	'buy' or 'sell'
amount 	float 	Yes 	how much of you want to trade in units of the base currency
price 	float 	No 	the price that the order is to be fulfilled, in units of the quote currency, ignored in market orders
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.cost 	float 	No 	market buy only the quote quantity that can be used as an alternative for the amount
params.triggerPrice 	float 	No 	the price that the order is to be triggered at
params.postOnly 	bool 	No 	if true, the order will only be posted to the order book and not executed immediately
params.timeInForce 	string 	No 	'GTC', 'IOC', 'FOK' or 'PO'
params.clientOrderId 	string 	No 	a unique id for the order (max length 40)
Supported exchanges

    coincatch
    hashkey

createSwapOrder

create a trade order on swap market

Kind: instance
Returns: object - an order structure
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to create an order in
type 	string 	Yes 	'market' or 'limit'
side 	string 	Yes 	'buy' or 'sell'
amount 	float 	Yes 	how much of you want to trade in units of the base currency
price 	float 	No 	the price that the order is to be fulfilled, in units of the quote currency, ignored in market orders
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.postOnly 	bool 	No 	non-trigger orders only if true, the order will only be posted to the order book and not executed immediately
params.reduceOnly 	bool 	No 	true or false whether the order is reduce only
params.timeInForce 	string 	No 	non-trigger orders only 'GTC', 'FOK', 'IOC' or 'PO'
params.clientOrderId 	string 	No 	a unique id for the order
params.triggerPrice 	float 	No 	the price that the order is to be triggered at
params.stopLossPrice 	float 	No 	The price at which a stop loss order is triggered at
params.takeProfitPrice 	float 	No 	The price at which a take profit order is triggered at
params.takeProfit 	object 	No 	takeProfit object in params containing the triggerPrice at which the attached take profit order will be triggered (perpetual swap markets only)
params.takeProfit.triggerPrice 	float 	No 	take profit trigger price
params.stopLoss 	object 	No 	stopLoss object in params containing the triggerPrice at which the attached stop loss order will be triggered (perpetual swap markets only)
params.stopLoss.triggerPrice 	float 	No 	stop loss trigger price
Supported exchanges

    coincatch
    hashkey

createTrailingAmountOrder

create a trailing order by providing the symbol, type, side, amount, price and trailingAmount

Kind: instance
Returns: object - an order structure
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to create an order in
type 	string 	Yes 	'market' or 'limit'
side 	string 	Yes 	'buy' or 'sell'
amount 	float 	Yes 	how much you want to trade in units of the base currency, or number of contracts
price 	float 	No 	the price for the order to be filled at, in units of the quote currency, ignored in market orders
trailingAmount 	float 	Yes 	the quote amount to trail away from the current market price
trailingTriggerPrice 	float 	Yes 	the price to activate a trailing order, default uses the price argument
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    woo

createTrailingPercentOrder

create a trailing order by providing the symbol, type, side, amount, price and trailingPercent

Kind: instance
Returns: object - an order structure
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to create an order in
type 	string 	Yes 	'market' or 'limit'
side 	string 	Yes 	'buy' or 'sell'
amount 	float 	Yes 	how much you want to trade in units of the base currency, or number of contracts
price 	float 	No 	the price for the order to be filled at, in units of the quote currency, ignored in market orders
trailingPercent 	float 	Yes 	the percent to trail away from the current market price
trailingTriggerPrice 	float 	Yes 	the price to activate a trailing order, default uses the price argument
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    htx
    woo

createVault

creates a value

Kind: instance
Returns: object - the api result
Param 	Type 	Required 	Description
name 	string 	Yes 	The name of the vault
description 	string 	Yes 	The description of the vault
initialUsd 	number 	Yes 	The initialUsd of the vault
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    hyperliquid

deposit

make a deposit

Kind: instance
Returns: object - a transaction structure
Param 	Type 	Required 	Description
code 	string 	Yes 	unified currency code
amount 	float 	Yes 	the amount to deposit
id 	string 	Yes 	the payment method id to be used for the deposit, can be retrieved from v2PrivateGetPaymentMethods
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.accountId 	string 	No 	the id of the account to deposit into
Supported exchanges

    coinbase

editContractOrder

edit a trade order

Kind: instance
Returns: object - an order structure
Param 	Type 	Required 	Description
id 	string 	Yes 	cancel order id
symbol 	string 	Yes 	unified symbol of the market to create an order in
type 	string 	Yes 	'market' or 'limit'
side 	string 	Yes 	'buy' or 'sell'
amount 	float 	Yes 	how much of currency you want to trade in units of base currency
price 	float 	No 	the price at which the order is to be fulfilled, in units of the quote currency, ignored in market orders
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.portfolioMargin 	boolean 	No 	set to true if you would like to edit an order in a portfolio margin account
Supported exchanges

    binance

editOrder

edit a trade order

Kind: instance
Returns: object - an order structure
Param 	Type 	Required 	Description
id 	string 	Yes 	order id
symbol 	string 	No 	unified symbol of the market to create an order in
type 	string 	No 	'market', 'limit' or 'stop_limit'
side 	string 	No 	'buy' or 'sell'
amount 	float 	No 	how much of the currency you want to trade in units of the base currency
price 	float 	No 	the price for the order, in units of the quote currency, ignored in market orders
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.triggerPrice 	string 	No 	the price to trigger a stop order
params.timeInForce 	string 	No 	for crypto trading either 'gtc' or 'ioc' can be used
params.clientOrderId 	string 	No 	a unique identifier for the order, automatically generated if not sent
Supported exchanges

    alpaca
    binance
    bingx
    bitfinex
    bitget
    bitmart
    bitvavo
    bybit
    coinbase
    coinbaseinternational
    coincatch
    coinex
    coinlist
    delta
    deribit
    derive
    exmo
    gate
    hyperliquid
    kraken
    krakenfutures
    kucoin
    okx
    phemex
    poloniex
    upbit
    vertex
    whitebit
    woo
    woofipro
    xt

editOrderWs

edit a trade order

Kind: instance
Returns: object - an order structure
Param 	Type 	Required 	Description
id 	string 	Yes 	order id
symbol 	string 	Yes 	unified symbol of the market to create an order in
type 	string 	Yes 	'market' or 'limit'
side 	string 	Yes 	'buy' or 'sell'
amount 	float 	Yes 	how much of the currency you want to trade in units of the base currency
price 	float, undefined 	No 	the price at which the order is to be fulfilled, in units of the quote currency, ignored in market orders
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    binance
    bitvavo
    bybit
    cex
    gate
    hyperliquid
    okx
    oxfun

editOrders

edit a list of trade orders

Kind: instance
Returns: object - an order structure
Param 	Type 	Required 	Description
orders 	Array 	Yes 	list of orders to create, each object should contain the parameters required by createOrder, namely symbol, type, side, amount, price and params
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    binance
    bybit
    hyperliquid

enableDemoTrading

enables or disables demo trading mode

Kind: instance
Param 	Type 	Required 	Description
enable 	boolean 	No 	true if demo trading should be enabled, false otherwise
Supported exchanges

    bybit

fetchAccount

query for balance and get the amount of funds available for trading or funds locked in orders

Kind: instance
Returns: object - a balance structure
Param 	Type 	Required 	Description
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    apex

fetchAccountIdByType

fetch all the accounts by a type and marginModeassociated with a profile

Kind: instance
Returns: object - a dictionary of account structures indexed by the account type
Param 	Type 	Required 	Description
type 	string 	Yes 	'spot', 'swap' or 'future
marginMode 	string 	No 	'cross' or 'isolated'
symbol 	string 	No 	unified ccxt market symbol
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    htx

fetchAccounts

fetch all the accounts associated with a profile

Kind: instance
Returns: object - a dictionary of account structures indexed by the account type
Param 	Type 	Required 	Description
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    ascendex
    coinbase
    coinbaseexchange
    coinbaseinternational
    coinlist
    cryptocom
    deribit
    hashkey
    htx
    huobijp
    kucoin
    luno
    mexc
    ndax
    novadax
    okx
    oxfun
    woo

fetchBalance

query for balance and get the amount of funds available for trading or funds locked in orders

Kind: instance
Returns: object - a balance structure
Param 	Type 	Required 	Description
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    alpaca
    apex
    ascendex
    bigone
    binance
    bingx
    bit2c
    bitbank
    bitbns
    bitfinex
    bitflyer
    bitget
    bithumb
    bitmart
    bitmex
    bitopro
    bitrue
    bitso
    bitstamp
    betteam
    bitvavo
    bl3p
    blockchaincom
    blofin
    btcalpha
    btcbox
    btcmarkets
    btcturk
    bybit
    cex
    coinbase
    coinbaseexchange
    coinbaseinternational
    coincatch
    coincheck
    coinex
    coinlist
    coinmate
    coinmetro
    coinone
    coinsph
    coinspot
    cryptocom
    cryptomus
    defx
    delta
    deribit
    derive
    digifinex
    ellipx
    exmo
    gate
    gemini
    hashkey
    hitbtc
    hollaex
    htx
    huobijp
    hyperliquid
    idex
    independentreserve
    indodax
    kraken
    krakenfutures
    kucoin
    kucoinfutures
    kuna
    latoken
    lbank
    luno
    mercado
    mexc
    ndax
    novadax
    oceanex
    okcoin
    okx
    onetrading
    oxfun
    p2b
    paradex
    paymium
    phemex
    poloniex
    probit
    timex
    tokocrypto
    tradeogre
    upbit
    vertex
    wavesexchange
    whitebit
    woo
    woofipro
    xt
    yobit
    zaif
    zonda

fetchBalanceWs

fetch balance and get the amount of funds available for trading or funds locked in orders

Kind: instance
Returns: object - a balance structure
Param 	Type 	Required 	Description
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.type 	string, undefined 	No 	'future', 'delivery', 'savings', 'funding', or 'spot'
params.marginMode 	string, undefined 	No 	'cross' or 'isolated', for margin trading, uses this.options.defaultMarginMode if not passed, defaults to undefined/None/null
params.symbols 	Array<string>, undefined 	No 	unified market symbols, only used in isolated margin mode
params.method 	string, undefined 	No 	method to use. Can be account.balance, account.status, v2/account.balance or v2/account.status
Supported exchanges

    binance
    bitvavo
    cex

fetchBidsAsks

fetches the bid and ask price and volume for multiple markets

Kind: instance
Returns: object - a dictionary of ticker structures
Param 	Type 	Required 	Description
symbols 	Array<string>, undefined 	Yes 	unified symbols of the markets to fetch the bids and asks for, all markets are returned if not assigned
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.subType 	string 	No 	"linear" or "inverse"
Supported exchanges

    binance
    bitrue
    bybit
    coinbase
    coinmetro
    kucoinfutures
    mexc
    tokocrypto
    xt

fetchBorrowInterest

fetch the interest owed by the user for borrowing currency for margin trading

Kind: instance
Returns: Array<object> - a list of borrow interest structures
Param 	Type 	Required 	Description
code 	string 	No 	unified currency code
symbol 	string 	No 	unified market symbol when fetch interest in isolated markets
since 	int 	No 	the earliest time in ms to fetch borrrow interest for
limit 	int 	No 	the maximum number of structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.portfolioMargin 	boolean 	No 	set to true if you would like to fetch the borrow interest in a portfolio margin account
Supported exchanges

    binance
    bitget
    bitmart
    bybit
    coinex
    gate
    htx
    kucoin
    okx
    whitebit

fetchBorrowRateHistories

retrieves a history of a multiple currencies borrow interest rate at specific time slots, returns all currencies if no symbols passed, default is undefined

Kind: instance
Returns: object - a dictionary of borrow rate structures indexed by the market symbol
Param 	Type 	Required 	Description
codes 	Array<string>, undefined 	Yes 	list of unified currency codes, default is undefined
since 	int 	No 	timestamp in ms of the earliest borrowRate, default is undefined
limit 	int 	No 	max number of borrow rate prices to return, default is undefined
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.marginMode 	string 	No 	'cross' or 'isolated' default is 'cross'
params.until 	int 	No 	the latest time in ms to fetch entries for
Supported exchanges

    kucoin
    okx

fetchBorrowRateHistory

retrieves a history of a currencies borrow interest rate at specific time slots

Kind: instance
Returns: Array<object> - an array of borrow rate structures
Param 	Type 	Required 	Description
code 	string 	Yes 	unified currency code
since 	int 	No 	timestamp for the earliest borrow rate
limit 	int 	No 	the maximum number of borrow rate structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    binance
    bybit
    kucoin
    okx

fetchCanceledAndClosedOrders

fetches information on multiple canceled orders made by the user

Kind: instance
Returns: Array<object> - a list of order structures
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol of the market the orders were made in
since 	int 	No 	the earliest time in ms to fetch orders for
limit 	int 	No 	the maximum number of order structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.paginate 	boolean 	No 	default false, when true will automatically paginate by calling this endpoint multiple times. See in the docs all the available parameters
params.portfolioMargin 	boolean 	No 	set to true if you would like to fetch orders in a portfolio margin account
params.trigger 	boolean 	No 	set to true if you would like to fetch portfolio margin account trigger or conditional orders
Supported exchanges

    binance
    bingx
    bitget
    bybit
    coincatch
    coinmetro
    hashkey
    hyperliquid

fetchCanceledOrders

fetches information on multiple canceled orders made by the user

Kind: instance
Returns: Array<object> - a list of order structures
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol of the market the orders were made in
since 	int 	No 	the earliest time in ms to fetch orders for
limit 	int 	No 	the maximum number of order structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.paginate 	boolean 	No 	default false, when true will automatically paginate by calling this endpoint multiple times. See in the docs all the available parameters
params.portfolioMargin 	boolean 	No 	set to true if you would like to fetch orders in a portfolio margin account
params.trigger 	boolean 	No 	set to true if you would like to fetch portfolio margin account trigger or conditional orders
Supported exchanges

    binance
    bingx
    bitget
    bitmart
    bitteam
    blockchaincom
    bybit
    coinbase
    coinlist
    defx
    derive
    exmo
    hyperliquid
    krakenfutures
    mexc
    okx
    upbit
    xt

fetchClosedOrder

fetch an open order by it's id

Kind: instance
Returns: object - an order structure
Param 	Type 	Required 	Description
id 	string 	Yes 	order id
symbol 	string 	Yes 	unified market symbol, default is undefined
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    bitfinex
    bybit
    cex

fetchClosedOrders

fetches information on multiple closed orders made by the user

Kind: instance
Returns: Array<Order> - a list of order structures
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol of the market orders were made in
since 	int 	No 	the earliest time in ms to fetch orders for
limit 	int 	No 	the maximum number of order structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.until 	int 	No 	the latest time in ms to fetch orders for
Supported exchanges

    alpaca
    ascendex
    bigone
    binance
    bingx
    bitfinex
    bitflyer
    bitget
    bitmart
    bitmex
    bitopro
    bitrue
    bitteam
    blockchaincom
    blofin
    btcalpha
    btcmarkets
    bybit
    cex
    coinbase
    coinbaseexchange
    coinex
    coinlist
    coinsph
    defx
    delta
    deribit
    derive
    gate
    hitbtc
    hollaex
    htx
    huobijp
    hyperliquid
    idex
    independentreserve
    indodax
    kraken
    krakenfutures
    kucoin
    kucoinfutures
    kuna
    luno
    mexc
    novadax
    oceanex
    okcoin
    okx
    onetrading
    p2b
    phemex
    poloniex
    probit
    timex
    tokocrypto
    upbit
    wavesexchange
    whitebit
    woo
    woofipro
    xt
    zaif

fetchClosedOrdersWs

fetch closed orders

Kind: instance
Returns: Array<object> - a list of order structures
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol
since 	int 	No 	the earliest time in ms to fetch open orders for
limit 	int 	No 	the maximum number of open orders structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    binance
    gate

fetchConvertCurrencies

fetches all available currencies that can be converted

Kind: instance
Returns: object - an associative dictionary of currencies
Param 	Type 	Required 	Description
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    binance
    bitget
    bybit
    okx
    woo

fetchConvertQuote

fetch a quote for converting from one currency to another

Kind: instance
Returns: object - a conversion structure
Param 	Type 	Required 	Description
fromCode 	string 	Yes 	the currency that you want to sell and convert from
toCode 	string 	Yes 	the currency that you want to buy and convert into
amount 	float 	Yes 	how much you want to trade in units of the from currency
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.walletType 	string 	No 	either 'SPOT' or 'FUNDING', the default is 'SPOT'
Supported exchanges

    binance
    bitget
    bybit
    coinbase
    okx
    phemex
    whitebit
    woo

fetchConvertTrade

fetch the data for a conversion trade

Kind: instance
Returns: object - a conversion structure
Param 	Type 	Required 	Description
id 	string 	Yes 	the id of the trade that you want to fetch
code 	string 	No 	the unified currency code of the conversion trade
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    binance
    bybit
    coinbase
    okx
    woo

fetchConvertTradeHistory

fetch the users history of conversion trades

Kind: instance
Returns: Array<object> - a list of conversion structures
Param 	Type 	Required 	Description
code 	string 	No 	the unified currency code
since 	int 	No 	the earliest time in ms to fetch conversions for
limit 	int 	No 	the maximum number of conversion structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.until 	int 	No 	timestamp in ms of the latest conversion to fetch
Supported exchanges

    binance
    bitget
    bybit
    okx
    phemex
    whitebit
    woo

fetchCrossBorrowRate

fetch the rate of interest to borrow a currency for margin trading

Kind: instance
Returns: object - a borrow rate structure
Param 	Type 	Required 	Description
code 	string 	Yes 	unified currency code
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    binance
    bitget
    bybit
    digifinex
    okx
    whitebit

fetchCrossBorrowRates

fetch the borrow interest rates of all currencies

Kind: instance
Returns: object - a list of borrow rate structures
Param 	Type 	Required 	Description
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    digifinex
    okx

fetchCurrencies

fetches all available currencies on an exchange

Kind: instance
Returns: object - an associative dictionary of currencies
Param 	Type 	Required 	Description
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    apex
    ascendex
    bigone
    binance
    bingx
    bitfinex
    bitget
    bitmart
    bitmex
    bitopro
    bitrue
    bitstamp
    bitteam
    bitvavo
    bybit
    cex
    coinbase
    coinbaseexchange
    coinbaseinternational
    coincatch
    coinex
    coinlist
    coinmetro
    coinone
    cryptomus
    delta
    deribit
    derive
    digifinex
    ellipx
    exmo
    gate
    gemini
    hashkey
    hitbtc
    hollaex
    htx
    huobijp
    hyperliquid
    idex
    kraken
    kucoin
    kuna
    latoken
    mexc
    ndax
    okcoin
    okx
    onetrading
    oxfun
    phemex
    poloniex
    probit
    timex
    vertex
    whitebit
    woo
    woofipro
    xt

fetchCurrenciesWs

fetches all available currencies on an exchange

Kind: instance
Returns: object - an associative dictionary of currencies
Param 	Type 	Required 	Description
params 	object 	No 	extra parameters specific to the bitvavo api endpoint
Supported exchanges

    bitvavo

fetchDeposit

fetch information on a deposit

Kind: instance
Returns: object - a transaction structure
Param 	Type 	Required 	Description
id 	string 	Yes 	deposit id
code 	string 	Yes 	not used by bitmart fetchDeposit ()
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    bitmart
    bitso
    blockchaincom
    coinbase
    exmo
    idex
    kuna
    okx
    upbit
    whitebit

fetchDepositAddress

fetch the deposit address for a currency associated with this account

Kind: instance
Returns: object - an address structure
Param 	Type 	Required 	Description
code 	string 	Yes 	unified currency code
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    alpaca
    ascendex
    bigone
    binance
    bingx
    bit2c
    bitbank
    bitbns
    bitfinex
    bitget
    bitmart
    bitmex
    bitso
    bitstamp
    bitvavo
    blockchaincom
    bybit
    cex
    coinbase
    coincatch
    coinex
    coinsph
    cryptocom
    delta
    deribit
    digifinex
    ellipx
    exmo
    gate
    gemini
    hashkey
    hitbtc
    htx
    idex
    independentreserve
    kraken
    kucoin
    kucoinfutures
    kuna
    lbank
    luno
    mexc
    ndax
    okcoin
    okx
    oxfun
    paymium
    phemex
    poloniex
    probit
    timex
    tokocrypto
    upbit
    wavesexchange
    whitebit
    woo
    xt
    yobit
    zonda

fetchDepositAddresses

fetch deposit addresses for multiple currencies and chain types

Kind: instance
Returns: object - a list of address structures
Param 	Type 	Required 	Description
codes 	Array<string>, undefined 	Yes 	list of unified currency codes, default is undefined
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    coinone
    hollaex
    indodax
    paymium
    probit
    upbit
    zonda

fetchDepositAddressesByNetwork

fetch the deposit addresses for a currency associated with this account

Kind: instance
Returns: object - a dictionary address structures, indexed by the network
Param 	Type 	Required 	Description
code 	string 	Yes 	unified currency code
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    bingx
    bybit
    cryptocom
    gate
    gemini
    htx
    kucoin
    mexc
    oceanex
    okcoin
    okx

fetchDepositMethodId

fetch the deposit id for a fiat currency associated with this account

Kind: instance
Returns: object - a deposit id structure
Param 	Type 	Required 	Description
id 	string 	Yes 	the deposit payment method id
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    coinbase

fetchDepositMethodIds

fetch the deposit id for a fiat currency associated with this account

Kind: instance
Returns: object - an array of deposit id structures
Param 	Type 	Required 	Description
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    coinbase

fetchDepositMethods

fetch deposit methods for a currency associated with this account

Kind: instance
Returns: object - of deposit methods
Param 	Type 	Required 	Description
code 	string 	Yes 	unified currency code
params 	object 	No 	extra parameters specific to the kraken api endpoint
Supported exchanges

    kraken

fetchDepositWithdrawFee

fetch the fee for deposits and withdrawals

Kind: instance
Returns: object - a fee structure
Param 	Type 	Required 	Description
code 	string 	Yes 	unified currency code
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.network 	string 	No 	the network code of the currency
Supported exchanges

    bitmart
    coinex
    kucoin

fetchDepositWithdrawFees

fetch deposit and withdraw fees

Kind: instance
Returns: object - a list of fee structures
Param 	Type 	Required 	Description
codes 	Array<string>, undefined 	Yes 	list of unified currency codes
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    ascendex
    binance
    bingx
    bitget
    bitmex
    bitopro
    bitrue
    bitso
    bitstamp
    bitvavo
    bybit
    coincatch
    cryptocom
    deribit
    digifinex
    exmo
    gate
    hitbtc
    hollaex
    htx
    kucoin
    lbank
    mexc
    okx
    poloniex
    probit
    wavesexchange
    whitebit

fetchDeposits

fetch all deposits made to an account

Kind: instance
Returns: Array<object> - a list of transaction structures
Param 	Type 	Required 	Description
code 	string 	No 	unified currency code
since 	int 	No 	the earliest time in ms to fetch deposits for
limit 	int 	No 	the maximum number of deposit structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    alpaca
    ascendex
    bigone
    binance
    bingx
    bitbns
    bitflyer
    bitget
    bitmart
    bitopro
    bitrue
    bitso
    bitvavo
    blockchaincom
    blofin
    btcalpha
    btcmarkets
    bybit
    coinbase
    coinbaseexchange
    coinbaseinternational
    coincatch
    coincheck
    coinex
    coinsph
    cryptocom
    deribit
    derive
    digifinex
    exmo
    gate
    hashkey
    hitbtc
    hollaex
    htx
    huobijp
    hyperliquid
    idex
    kraken
    kucoin
    kucoinfutures
    kuna
    lbank
    mexc
    ndax
    novadax
    okcoin
    okx
    oxfun
    phemex
    poloniex
    probit
    timex
    tokocrypto
    upbit
    whitebit
    woo
    woofipro
    xt

fetchDepositsWithdrawals

fetch history of deposits and withdrawals

Kind: instance
Returns: object - a list of transaction structure
Param 	Type 	Required 	Description
code 	string 	No 	unified currency code for the currency of the deposit/withdrawals, default is undefined
since 	int 	No 	timestamp in ms of the earliest deposit/withdrawal, default is undefined
limit 	int 	No 	max number of deposit/withdrawals to return, default is undefined
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    alpaca
    ascendex
    bitfinex
    bitmex
    bitstamp
    bitteam
    btcmarkets
    cex
    coinbase
    coinbaseexchange
    exchange
    coinlist
    coinmate
    exmo
    gemini
    hitbtc
    indodax
    novadax
    poloniex
    probit
    whitebit
    woo
    woofipro

fetchDepositsWs

fetch all deposits made to an account

Kind: instance
Returns: Array<object> - a list of transaction structures
Param 	Type 	Required 	Description
code 	string 	Yes 	unified currency code
since 	int 	No 	the earliest time in ms to fetch deposits for
limit 	int 	No 	the maximum number of deposits structures to retrieve
params 	object 	No 	extra parameters specific to the bitvavo api endpoint
Supported exchanges

    bitvavo

fetchFundingHistory

fetches information on multiple orders made by the user classic accounts only

Kind: instance
Returns: Array<Trade> - a list of trade structures
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol of the market orders were made in
since 	int 	No 	the earliest time in ms to fetch orders for
limit 	int 	No 	the maximum number of order structures to retrieve, default 100
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.until 	object 	No 	end time, ms
params.side 	boolean 	No 	BUY or SELL
params.page 	boolean 	No 	Page numbers start from 0
Supported exchanges

    apex
    ascendex
    binance
    bitget
    bitmart
    bybit
    coinbaseinternational
    coinex
    derive
    digifinex
    gate
    htx
    hyperliquid
    kucoinfutures
    mexc
    okx
    oxfun
    phemex
    whitebit
    woo
    xt

fetchFundingInterval

fetch the current funding rate interval

Kind: instance
Returns: object - a funding rate structure
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    bitget
    coinex
    digifinex
    kucoinfutures
    mexc
    okx
    woo
    woofipro
    xt

fetchFundingIntervals

fetch the funding rate interval for multiple markets

Kind: instance
Returns: Array<object> - a list of funding rate structures
Param 	Type 	Required 	Description
symbols 	Array<string> 	No 	list of unified market symbols
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.subType 	string 	No 	"linear" or "inverse"
Supported exchanges

    binance

fetchFundingRate

fetch the current funding rate

Kind: instance
Returns: object - a funding rate structure
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    binance
    bingx
    bitflyer
    bitget
    bitmart
    blofin
    coincatch
    coinex
    coinlist
    defx
    delta
    deribit
    derive
    digifinex
    gate
    hashkey
    hitbtc
    htx
    kucoinfutures
    lbank
    mexc
    okx
    phemex
    vertex
    whitebit
    woo
    woofipro
    xt

fetchFundingRateHistory

fetches historical funding rate prices

Kind: instance
Returns: Array<object> - a list of funding rate structures
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to fetch the funding rate history for
since 	int 	No 	timestamp in ms of the earliest funding rate to fetch
limit 	int 	No 	the maximum amount of funding rate structures to fetch
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.until 	int 	No 	timestamp in ms of the latest funding rate
params.paginate 	boolean 	No 	default false, when true will automatically paginate by calling this endpoint multiple times. See in the docs all the availble parameters
Supported exchanges

    apex
    binance
    bingx
    bitfinex
    bitget
    bitmart
    bitmex
    blofin
    bybit
    coinbaseinternational
    coincatch
    coinex
    cryptocom
    deribit
    derive
    digifinex
    gate
    hashkey
    hitbtc
    htx
    hyperliquid
    krakenfutures
    kucoinfutures
    mexc
    okx
    oxfun
    phemex
    woo
    woofipro
    xt

fetchFundingRates

fetch the funding rate for multiple markets

Kind: instance
Returns: Array<object> - a list of funding rates structures, indexe by market symbols
Param 	Type 	Required 	Description
symbols 	Array<string>, undefined 	Yes 	list of unified market symbols
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    ascendex
    binance
    bingx
    bitfinex
    bitget
    bitmex
    bybit
    coinex
    delta
    gate
    hashkey
    hitbtc
    htx
    hyperliquid
    krakenfutures
    lbank
    oxfun
    vertex
    whitebit
    woo
    woofipro

fetchGreeks

fetches an option contracts greeks, financial metrics used to measure the factors that affect the price of an options contract

Kind: instance
Returns: object - a greeks structure
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to fetch greeks for
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    binance
    bybit
    delta
    deribit
    gate
    okx

fetchIsolatedBorrowRate

fetch the rate of interest to borrow a currency for margin trading

Kind: instance
Returns: object - an isolated borrow rate structure
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol
params 	object 	No 	extra parameters specific to the exchange API endpoint EXCHANGE SPECIFIC PARAMETERS
params.vipLevel 	object 	No 	user's current specific margin data will be returned if viplevel is omitted
Supported exchanges

    binance
    bitget
    bitmart
    coinex

fetchIsolatedBorrowRates

fetch the borrow interest rates of all currencies

Kind: instance
Returns: object - a borrow rate structure
Param 	Type 	Required 	Description
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.symbol 	object 	No 	unified market symbol EXCHANGE SPECIFIC PARAMETERS
params.vipLevel 	object 	No 	user's current specific margin data will be returned if viplevel is omitted
Supported exchanges

    binance
    bitmart
    htx

fetchL3OrderBook

fetches level 3 information on open orders with bid (buy) and ask (sell) prices, volumes and other data

Kind: instance
Returns: object - an order book structure
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol
limit 	int 	No 	max number of orders to return, default is undefined
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    blockchaincom
    kuna

fetchLastPrices

fetches the last price for multiple markets

Kind: instance
Returns: object - a dictionary of lastprices structures
Param 	Type 	Required 	Description
symbols 	Array<string>, undefined 	Yes 	unified symbols of the markets to fetch the last prices
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.subType 	string 	No 	"linear" or "inverse"
Supported exchanges

    binance
    hashkey
    htx

fetchLedger

fetch the history of changes, actions done by the user or operations that altered the balance of the user

Kind: instance
Returns: object - a ledger structure
Param 	Type 	Required 	Description
code 	string 	No 	unified currency code
since 	int 	No 	timestamp in ms of the earliest ledger entry
limit 	int 	No 	max number of ledger entries to return
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.until 	int 	No 	timestamp in ms of the latest ledger entry
params.paginate 	boolean 	No 	default false, when true will automatically paginate by calling this endpoint multiple times. See in the docs all the available parameters
params.portfolioMargin 	boolean 	No 	set to true if you would like to fetch the ledger for a portfolio margin account
params.subType 	string 	No 	"linear" or "inverse"
Supported exchanges

    binance
    bitfinex
    bitget
    bitmart
    bitmex
    bitso
    bitstamp
    blofin
    bybit
    cex
    coinbase
    coinbaseexchange
    coincatch
    coinlist
    coinmetro
    cryptocom
    defx
    delta
    digifinex
    gate
    hashkey
    htx
    hyperliquid
    kraken
    kucoin
    luno
    ndax
    okcoin
    okx
    woo
    woofipro
    xt
    zonda

fetchLedgerEntry

fetch the history of changes, actions done by the user or operations that altered the balance of the user

Kind: instance
Returns: object - a ledger structure
Param 	Type 	Required 	Description
id 	string 	Yes 	the identification number of the ledger entry
code 	string 	Yes 	unified currency code
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    binance

fetchLeverage

fetch the set leverage for a market

Kind: instance
Returns: object - a leverage structure
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    bingx
    bitget
    blofin
    bybit
    coincatch
    coinex
    delta
    gate
    hashkey
    hitbtc
    krakenfutures
    kucoinfutures
    mexc
    okx
    paradex
    poloniex
    woo
    woofipro

fetchLeverageTiers

retrieve information on the maximum leverage, and maintenance margin for trades of varying trade sizes

Kind: instance
Returns: object - a dictionary of leverage tiers structures, indexed by market symbols
Param 	Type 	Required 	Description
symbols 	Array<string>, undefined 	Yes 	list of unified market symbols
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    ascendex
    binance
    bybit
    coinex
    digifinex
    gate
    hashkey
    htx
    krakenfutures
    mexc
    oxfun
    phemex
    xt

fetchLeverages

fetch the set leverage for all contract markets

Kind: instance
Returns: object - a list of leverage structures
Param 	Type 	Required 	Description
symbols 	Array<string> 	No 	a list of unified market symbols
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    ascendex
    binance
    bitmex
    blofin
    gate
    krakenfutures

fetchLiquidations

retrieves the public liquidations of a trading pair

Kind: instance
Returns: object - an array of liquidation structures
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified CCXT market symbol
since 	int 	No 	the earliest time in ms to fetch liquidations for
limit 	int 	No 	the maximum number of liquidation structures to retrieve
params 	object 	No 	exchange specific parameters
params.until 	int 	No 	timestamp in ms of the latest liquidation
params.paginate 	boolean 	No 	default false, when true will automatically paginate by calling this endpoint multiple times. See in the docs all the available parameters
Supported exchanges

    bitfinex
    bitmex
    deribit
    gate
    htx
    paradex

fetchLongShortRatioHistory

fetches the long short ratio history for a unified market symbol

Kind: instance
Returns: Array<object> - an array of long short ratio structures
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to fetch the long short ratio for
timeframe 	string 	No 	the period for the ratio, default is 24 hours
since 	int 	No 	the earliest time in ms to fetch ratios for
limit 	int 	No 	the maximum number of long short ratio structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.until 	int 	No 	timestamp in ms of the latest ratio to fetch
Supported exchanges

    binance
    bitget
    bybit
    okx

fetchMarginAdjustmentHistory

fetches the history of margin added or reduced from contract isolated positions

Kind: instance
Returns: Array<object> - a list of margin structures
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol
type 	string 	No 	"add" or "reduce"
since 	int 	No 	timestamp in ms of the earliest change to fetch
limit 	int 	No 	the maximum amount of changes to fetch
params 	object 	Yes 	extra parameters specific to the exchange api endpoint
params.until 	int 	No 	timestamp in ms of the latest change to fetch
Supported exchanges

    binance
    coinex
    okx

fetchMarginMode

fetches the margin mode of a specific symbol

Kind: instance
Returns: object - a margin mode structure
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market the order was made in
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.subType 	string 	No 	"linear" or "inverse"
Supported exchanges

    binance
    bingx
    bitget
    blofin
    coincatch
    delta
    kucoinfutures
    paradex

fetchMarginModes

fetches the set margin mode of the user

Kind: instance
Returns: object - a list of margin mode structures
Param 	Type 	Required 	Description
symbols 	Array<string> 	No 	a list of unified market symbols
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    ascendex
    binance
    hitbtc

fetchMarkPrice

fetches mark price for the market

Kind: instance
Returns: object - a dictionary of ticker structures
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to fetch the ticker for
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.subType 	string 	No 	"linear" or "inverse"
Supported exchanges

    binance
    bingx
    bitget
    blofin
    defx
    kucoin
    kucoinfutures
    okx

fetchMarkPrices

fetches mark prices for multiple markets

Kind: instance
Returns: object - a dictionary of ticker structures
Param 	Type 	Required 	Description
symbols 	Array<string> 	No 	unified symbols of the markets to fetch the ticker for, all market tickers are returned if not assigned
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.subType 	string 	No 	"linear" or "inverse"
Supported exchanges

    binance
    bingx
    kucoin
    okx

fetchMarketLeverageTiers

retrieve information on the maximum leverage, and maintenance margin for trades of varying trade sizes for a single market

Kind: instance
Returns: object - a leverage tiers structure
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.marginMode 	string 	No 	for spot margin 'cross' or 'isolated', default is 'isolated'
params.code 	string 	No 	required for cross spot margin
params.productType 	string 	No 	contract only 'USDT-FUTURES', 'USDC-FUTURES', 'COIN-FUTURES', 'SUSDT-FUTURES', 'SUSDC-FUTURES' or 'SCOIN-FUTURES'
Supported exchanges

    bitget
    bybit
    digifinex
    gate
    kucoinfutures
    okx
    xt

fetchMarkets

retrieves data on all markets for alpaca

Kind: instance
Returns: Array<object> - an array of objects representing market data
Param 	Type 	Required 	Description
params 	object 	No 	extra parameters specific to the exchange api endpoint
Supported exchanges

    alpaca
    apex
    ascendex
    bigone
    binance
    bingx
    bitbank
    bitbns
    bitfinex
    bitflyer
    bitget
    bithumb
    bitmart
    bitmex
    bitopro
    bitrue
    bitso
    bitstamp
    bitteam
    bitvavo
    blockchaincom
    blofin
    btcalpha
    btcbox
    btcmarkets
    btcturk
    bybit
    cex
    coinbase
    coinbaseexchange
    coinbaseinternational
    coincatch
    coinex
    coinlist
    coinmate
    coinmetro
    coinone
    coinsph
    cryptocom
    cryptomus
    defx
    delta
    deribit
    derive
    digifinex
    ellipx
    exmo
    gate
    gemini
    hashkey
    hitbtc
    hollaex
    htx
    huobijp
    hyperliquid
    idex
    independentreserve
    indodax
    kraken
    krakenfutures
    kucoin
    kucoinfutures
    kuna
    latoken
    lbank
    luno
    mercado
    mexc
    ndax
    novadax
    oceanex
    okcoin
    okx
    onetrading
    oxfun
    p2b
    paradex
    phemex
    poloniex
    probit
    timex
    tokocrypto
    tradeogre
    upbit
    vertex
    wavesexchange
    whitebit
    woo
    woofipro
    xt
    yobit
    zaif
    zonda

fetchMarketsWs

retrieves data on all markets for bitvavo

Kind: instance
Returns: Array<object> - an array of objects representing market data
Param 	Type 	Required 	Description
params 	object 	No 	extra parameters specific to the exchange api endpoint
Supported exchanges

    bitvavo

fetchMyDustTrades

fetch all dust trades made by the user

Kind: instance
Returns: Array<object> - a list of trade structures
Param 	Type 	Required 	Description
symbol 	string 	Yes 	not used by binance fetchMyDustTrades ()
since 	int 	No 	the earliest time in ms to fetch my dust trades for
limit 	int 	No 	the maximum number of dust trades to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.type 	string 	No 	'spot' or 'margin', default spot
Supported exchanges

    binance

fetchMyLiquidations

retrieves the users liquidated positions

Kind: instance
Returns: object - an array of liquidation structures
Param 	Type 	Required 	Description
symbol 	string 	No 	unified CCXT market symbol
since 	int 	No 	the earliest time in ms to fetch liquidations for
limit 	int 	No 	the maximum number of liquidation structures to retrieve
params 	object 	No 	exchange specific parameters for the binance api endpoint
params.until 	int 	No 	timestamp in ms of the latest liquidation
params.paginate 	boolean 	No 	spot only default false, when true will automatically paginate by calling this endpoint multiple times. See in the docs all the available parameters
params.portfolioMargin 	boolean 	No 	set to true if you would like to fetch liquidations in a portfolio margin account
params.type 	string 	No 	"spot"
params.subType 	string 	No 	"linear" or "inverse"
Supported exchanges

    binance
    bingx
    bitget
    bitmart
    bybit
    deribit
    gate

fetchMySettlementHistory

fetches historical settlement records of the user

Kind: instance
Returns: Array<object> - a list of [settlement history objects]
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol of the settlement history
since 	int 	No 	timestamp in ms
limit 	int 	No 	number of records
params 	object 	No 	exchange specific params
Supported exchanges

    binance
    bybit
    gate

fetchMyTrades

fetch all trades made by the user

Kind: instance
Returns: Array<Trade> - a list of trade structures
Param 	Type 	Required 	Description
symbol 	string 	No 	unified market symbol
since 	int 	No 	the earliest time in ms to fetch trades for
limit 	int 	No 	the maximum number of trade structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.until 	int 	No 	the latest time in ms to fetch trades for
params.page_token 	string 	No 	page_token - used for paging
Supported exchanges

    alpaca
    apex
    bigone
    binance
    bingx
    bit2c
    bitbank
    bitbns
    bitfinex
    bitflyer
    bitget
    bitmart
    bitmex
    bitopro
    bitrue
    bitso
    bitstamp
    bitteam
    bitvavo
    blockchaincom
    blofin
    btcalpha
    btcmarkets
    btcturk
    bybit
    coinbase
    coinbaseexchange
    coinbaseinternational
    coincatch
    coincheck
    coinex
    coinlist
    coinmate
    coinmetro
    coinone
    coinsph
    coinspot
    cryptocom
    defx
    delta
    deribit
    derive
    digifinex
    exmo
    gate
    gemini
    hashkey
    hitbtc
    hollaex
    htx
    huobijp
    hyperliquid
    idex
    independentreserve
    kraken
    krakenfutures
    kucoin
    kucoinfutures
    kuna
    latoken
    lbank
    luno
    mercado
    mexc
    ndax
    novadax
    okcoin
    okx
    onetrading
    oxfun
    p2b
    paradex
    phemex
    poloniex
    probit
    timex
    tokocrypto
    vertex
    wavesexchange
    whitebit
    woo
    woofipro
    xt
    yobit
    zonda

fetchMyTradesWs

fetch all trades made by the user

Kind: instance
Returns: Array<object> - a list of trade structures
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol
since 	int, undefined 	No 	the earliest time in ms to fetch trades for
limit 	int, undefined 	No 	the maximum number of trades structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.endTime 	int 	No 	the latest time in ms to fetch trades for
params.fromId 	int 	No 	first trade Id to fetch
Supported exchanges

    binance
    bitvavo

fetchOHLCV

fetches historical candlestick data containing the open, high, low, and close price, and the volume of a market

Kind: instance
Returns: Array<Array<int>> - A list of candles ordered as timestamp, open, high, low, close, volume
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to fetch OHLCV data for
timeframe 	string 	Yes 	the length of time each candle represents
since 	int 	No 	timestamp in ms of the earliest candle to fetch
limit 	int 	No 	the maximum amount of candles to fetch
params 	object 	No 	extra parameters specific to the alpha api endpoint
params.loc 	string 	No 	crypto location, default: us
params.method 	string 	No 	method, default: marketPublicGetV1beta3CryptoLocBars
Supported exchanges

    alpaca
    apex
    ascendex
    bigone
    binance
    bingx
    bitbank
    bitfinex
    bitget
    bithumb
    bitmart
    bitmex
    bitopro
    bitrue
    bitso
    bitstamp
    bitteam
    bitvavo
    blofin
    btcalpha
    btcmarkets
    btcturk
    bybit
    cex
    coinbase
    coinbaseexchange
    coinbaseinternational
    coincatch
    coinex
    coinlist
    coinmetro
    coinsph
    cryptocom
    defx
    delta
    deribit
    digifinex
    ellipx
    exmo
    gateio
    gemini
    hashkey
    hitbtc
    hollaex
    htx
    huobijp
    hyperliquid
    idex
    indodax
    kraken
    krakenfutures
    kucoin
    kucoinfutures
    lbank
    luno
    mercado
    mexc
    ndax
    novadax
    oceanex
    okcoin
    okx
    onetrading
    oxfun
    p2b
    paradex
    phemex
    poloniex
    probit
    timex
    tokocrypto
    tradeogre
    upbit
    vertex
    wavesexchange
    whitebit
    woo
    woofipro
    xt
    zonda

fetchOHLCVWs

query historical candlestick data containing the open, high, low, and close price, and the volume of a market

Kind: instance
Returns: Array<Array<int>> - A list of candles ordered as timestamp, open, high, low, close, volume
Param 	Type 	Description
symbol 	string 	unified symbol of the market to query OHLCV data for
timeframe 	string 	the length of time each candle represents
since 	int 	timestamp in ms of the earliest candle to fetch
limit 	int 	the maximum amount of candles to fetch
params 	object 	extra parameters specific to the exchange API endpoint
params.until 	int 	timestamp in ms of the earliest candle to fetch EXCHANGE SPECIFIC PARAMETERS
params.timeZone 	string 	default=0 (UTC)
Supported exchanges

    binance
    bitvavo
    lbank

fetchOpenInterest

retrieves the open interest of a contract trading pair

Kind: instance
Returns: object - an open interest structurehttps://docs.ccxt.com/#/?id=open-interest-structure
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified CCXT market symbol
params 	object 	No 	exchange specific parameters
Supported exchanges

    apex
    binance
    bingx
    bitfinex
    bitget
    bitmart
    bybit
    delta
    gate
    hitbtc
    htx
    hyperliquid
    okx
    paradex
    phemex
    vertex

fetchOpenInterestHistory

Retrieves the open interest history of a currency

Kind: instance
Returns: object - an array of open interest structure
Param 	Type 	Required 	Description
symbol 	string 	Yes 	Unified CCXT market symbol
timeframe 	string 	Yes 	"5m","15m","30m","1h","2h","4h","6h","12h", or "1d"
since 	int 	No 	the time(ms) of the earliest record to retrieve as a unix timestamp
limit 	int 	No 	default 30, max 500
params 	object 	No 	exchange specific parameters
params.until 	int 	No 	the time(ms) of the latest record to retrieve as a unix timestamp
params.paginate 	boolean 	No 	default false, when true will automatically paginate by calling this endpoint multiple times. See in the docs all the availble parameters
Supported exchanges

    binance
    bitfinex
    bybit
    htx
    okx

fetchOpenInterests

Retrieves the open interest for a list of symbols

Kind: instance
Returns: Array<object> - a list of open interest structures
Param 	Type 	Required 	Description
symbols 	Array<string> 	No 	a list of unified CCXT market symbols
params 	object 	No 	exchange specific parameters
Supported exchanges

    bitfinex
    hitbtc
    htx
    hyperliquid
    vertex

fetchOpenOrder

fetch an open order by the id

Kind: instance
Returns: object - an order structure
Param 	Type 	Required 	Description
id 	string 	Yes 	order id
symbol 	string 	Yes 	unified market symbol
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.trigger 	string 	No 	set to true if you would like to fetch portfolio margin account stop or conditional orders
params.portfolioMargin 	boolean 	No 	set to true if you would like to fetch for a portfolio margin account
Supported exchanges

    binance
    bitfinex
    bybit
    cex
    hitbtc
    hollaex

fetchOpenOrders

fetch all unfilled currently open orders

Kind: instance
Returns: Array<Order> - a list of order structures
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol of the market orders were made in
since 	int 	No 	the earliest time in ms to fetch orders for
limit 	int 	No 	the maximum number of order structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.until 	int 	No 	the latest time in ms to fetch orders for
Supported exchanges

    alpaca
    apex
    ascendex
    bigone
    binance
    bingx
    bit2c
    bitbank
    bitbns
    bitfinex
    bitflyer
    bitget
    bithumb
    bitmart
    bitmex
    bitopro
    bitrue
    bitso
    bitstamp
    bitteam
    bitvavo
    blockchaincom
    blofin
    btcalpha
    btcbox
    btcmarkets
    btcturk
    bybit
    cex
    coinbase
    coinbaseexchange
    coinbaseinternational
    coincatch
    coincheck
    coinex
    coinlist
    coinmate
    coinmetro
    coinone
    coinsph
    cryptocom
    cryptomus
    defx
    delta
    deribit
    derive
    digifinex
    ellipx
    exmo
    gate
    gemini
    hashkey
    hitbtc
    hollaex
    htx
    huobijp
    hyperliquid
    idex
    independentreserve
    indodax
    kraken
    krakenfutures
    kucoin
    kucoinfutures
    kuna
    latoken
    lbank
    luno
    mercado
    mexc
    ndax
    novadax
    oceanex
    okcoin
    okx
    onetrading
    oxfun
    p2b
    paradex
    phemex
    poloniex
    probit
    timex
    tokocrypto
    tradeogre
    upbit
    vertex
    wavesexchange
    whitebit
    woo
    woofipro
    xt
    yobit
    zaif
    zonda

fetchOpenOrdersWs

fetch all unfilled currently open orders

Kind: instance
Returns: Array<object> - a list of order structures
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol
since 	int, undefined 	No 	the earliest time in ms to fetch open orders for
limit 	int, undefined 	No 	the maximum number of open orders structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    binance
    bitvavo
    cex
    gate

fetchOption

fetches option data that is commonly found in an option chain

Kind: instance
Returns: object - an option chain structure
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    binance
    bybit
    delta
    deribit
    gate
    okx

fetchOptionChain

fetches data for an underlying asset that is commonly found in an option chain

Kind: instance
Returns: object - a list of option chain structures
Param 	Type 	Required 	Description
code 	string 	Yes 	base currency to fetch an option chain for
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    bybit
    deribit
    gate
    okx

fetchOptionPositions

fetch data on open options positions

Kind: instance
Returns: Array<object> - a list of position structures
Param 	Type 	Required 	Description
symbols 	Array<string>, undefined 	Yes 	list of unified market symbols
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    binance

fetchOrder

fetches information on an order made by the user

Kind: instance
Returns: object - An order structure
Param 	Type 	Required 	Description
id 	string 	Yes 	the order id
symbol 	string 	Yes 	unified symbol of the market the order was made in
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    alpaca
    apex
    ascendex
    bigone
    binance
    bingx
    bit2c
    bitbank
    bitbns
    bitfinex
    bitflyer
    bitget
    bithumb
    bitmart
    bitmex
    bitopro
    bitrue
    bitso
    bitstamp
    bitteam
    bitvavo
    blockchaincom
    btcalpha
    btcbox
    btcmarkets
    bybit
    coinbase
    coinbaseexchange
    coinbaseinternational
    coincatch
    coinex
    coinlist
    coinmate
    coinmetro
    coinone
    coinsph
    cryptocom
    defx
    deribit
    digifinex
    ellipx
    exmo
    gate
    gemini
    hashkey
    hitbtc
    hollaex
    htx
    huobijp
    hyperliquid
    idex
    independentreserve
    indodax
    kraken
    kucoin
    kucoinfutures
    kuna
    latoken
    lbank
    luno
    mercado
    mexc
    ndax
    novadax
    oceanex
    okcoin
    okx
    onetrading
    oxfun
    paradex
    phemex
    poloniex
    probit
    timex
    tokocrypto
    tradeogre
    upbit
    vertex
    wavesexchange
    woo
    woofipro
    xt
    yobit

fetchOrderBook

fetches information on open orders with bid (buy) and ask (sell) prices, volumes and other data

Kind: instance
Returns: object - A dictionary of order book structures indexed by market symbols
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to fetch the order book for
limit 	int 	No 	the maximum amount of order book entries to return
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.loc 	string 	No 	crypto location, default: us
Supported exchanges

    alpaca
    apex
    ascendex
    bigone
    binance
    bingx
    bit2c
    bitbank
    bitbns
    bitfinex
    bitflyer
    bitget
    bithumb
    bitmart
    bitmex
    bitopro
    bitrue
    bitso
    bitstamp
    bitteam
    bitvavo
    bl3p
    blockchaincom
    blofin
    btcalpha
    btcbox
    btcmarkets
    btcturk
    bybit
    cex
    coinbase
    coinbaseexchange
    coincatch
    coincheck
    coinex
    coinlist
    coinmate
    coinmetro
    coinone
    coinsph
    coinspot
    cryptocom
    cryptomus
    defx
    delta
    deribit
    digifinex
    ellipx
    exmo
    gate
    gemini
    hashkey
    hitbtc
    hollaex
    htx
    huobijp
    hyperliquid
    idex
    independentreserve
    indodax
    kraken
    krakenfutures
    kucoin
    kucoinfutures
    kuna
    latoken
    lbank
    luno
    mercado
    mexc
    ndax
    novadax
    oceanex
    okcoin
    okx
    onetrading
    oxfun
    p2b
    paradex
    paymium
    phemex
    poloniex
    probit
    timex
    tokocrypto
    tradeogre
    upbit
    vertex
    wavesexchange
    whitebit
    woo
    woofipro
    xt
    yobit
    zaif
    zonda

fetchOrderBookWs

fetches information on open orders with bid (buy) and ask (sell) prices, volumes and other data

Kind: instance
Returns: object - A dictionary of order book structures indexed by market symbols
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to fetch the order book for
limit 	int 	No 	the maximum amount of order book entries to return
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    binance
    lbank

fetchOrderBooks

fetches information on open orders with bid (buy) and ask (sell) prices, volumes and other data for multiple markets

Kind: instance
Returns: object - a dictionary of order book structures indexed by market symbol
Param 	Type 	Required 	Description
symbols 	Array<string>, undefined 	Yes 	list of unified market symbols, all symbols fetched if undefined, default is undefined
limit 	int 	No 	max number of entries per orderbook to return, default is undefined
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    exmo
    hitbtc
    hollaex
    oceanex
    upbit
    yobit

fetchOrderClassic

fetches information on an order made by the user classic accounts only

Kind: instance
Returns: object - An order structure
Param 	Type 	Required 	Description
id 	string 	Yes 	the order id
symbol 	string 	Yes 	unified symbol of the market the order was made in
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    bybit

fetchOrderTrades

fetch all the trades made from a single order

Kind: instance
Returns: Array<object> - a list of trade structures
Param 	Type 	Required 	Description
id 	string 	Yes 	order id
symbol 	string 	Yes 	unified market symbol
since 	int 	No 	the earliest time in ms to fetch trades for
limit 	int 	No 	the maximum number of trades to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    apex
    binance
    bitfinex
    bitmart
    bitso
    bybit
    coinbaseexchange
    coincatch
    coinlist
    coinsph
    deribit
    derive
    ellipx
    exmo
    gate
    hitbtc
    htx
    huobijp
    kraken
    kucoin
    mexc
    ndax
    novadax
    okcoin
    okx
    onetrading
    p2b
    poloniex
    whitebit
    woo
    woofipro

fetchOrderWs

fetches information on an order made by the user

Kind: instance
Returns: object - An order structure
Param 	Type 	Required 	Description
id 	string 	Yes 	order id
symbol 	string 	No 	unified symbol of the market the order was made in
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    binance
    bitvavo
    cex
    gate

fetchOrders

fetches information on multiple orders made by the user

Kind: instance
Returns: Array<Order> - a list of order structures
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol of the market orders were made in
since 	int 	No 	the earliest time in ms to fetch orders for
limit 	int 	No 	the maximum number of order structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.until 	int 	No 	the latest time in ms to fetch orders for
Supported exchanges

    alpaca
    apex
    bigone
    binance
    bingx
    bitflyer
    bitmex
    bitopro
    bitteam
    bitvavo
    blockchaincom
    btcalpha
    btcbox
    btcmarkets
    btcturk
    bybit
    cex
    coinbase
    coinbaseexchange
    coinlist
    coinmate
    cryptocom
    cryptomus
    defx
    derive
    digifinex
    ellipx
    gemini
    hollaex
    htx
    huobijp
    hyperliquid
    latoken
    lbank
    luno
    mercado
    mexc
    ndax
    novadax
    oceanex
    paradex
    phemex
    tokocrypto
    vertex
    wavesexchange
    woo
    woofipro
    xt

fetchOrdersByIds

fetch orders by the list of order id

Kind: instance
Returns: Array<object> - a list of order structure
Param 	Type 	Required 	Description
ids 	Array<string> 	No 	list of order id
symbol 	string 	No 	unified ccxt market symbol
params 	object 	No 	extra parameters specific to the kraken api endpoint
Supported exchanges

    kraken

fetchOrdersByStatus

fetch a list of orders

Kind: instance
Returns: Array<Order> - a list of order structures
Param 	Type 	Required 	Description
status 	string 	Yes 	order status to fetch for
symbol 	string 	Yes 	unified market symbol of the market orders were made in
since 	int 	No 	the earliest time in ms to fetch orders for
limit 	int 	No 	the maximum number of order structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.trigger 	boolean 	No 	set to true for fetching trigger orders
params.marginMode 	string 	No 	'cross' or 'isolated' for fetching spot margin orders
Supported exchanges

    coinex
    ellipx
    kucoin
    kucoinfutures
    kuna

fetchOrdersClassic

fetches information on multiple orders made by the user classic accounts only

Kind: instance
Returns: Array<Order> - a list of order structures
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
Supported exchanges

    bybit

fetchOrdersWs

fetches information on multiple orders made by the user

Kind: instance
Returns: Array<object> - a list of order structures
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol of the market orders were made in
since 	int, undefined 	No 	the earliest time in ms to fetch orders for
limit 	int, undefined 	No 	the maximum number of order structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.orderId 	int 	No 	order id to begin at
params.startTime 	int 	No 	earliest time in ms to retrieve orders for
params.endTime 	int 	No 	latest time in ms to retrieve orders for
params.limit 	int 	No 	the maximum number of order structures to retrieve
Supported exchanges

    binance
    bitvavo
    gate

fetchPortfolioDetails

Fetch details for a specific portfolio by UUID

Kind: instance
Returns: Array<any> - An account structure https://docs.ccxt.com/#/?id=account-structure
Param 	Type 	Required 	Description
portfolioUuid 	string 	Yes 	The unique identifier of the portfolio to fetch
params 	Dict 	No 	Extra parameters specific to the exchange API endpoint
Supported exchanges

    coinbase

fetchPortfolios

fetch all the portfolios

Kind: instance
Returns: object - a dictionary of account structures indexed by the account type
Param 	Type 	Required 	Description
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    coinbase

fetchPosition

fetch data on an open position

Kind: instance
Returns: object - a position structure
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol of the market the position is held in
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    binance
    bingx
    bitget
    bitmart
    blofin
    bybit
    coinbase
    coinbaseinternational
    coincatch
    coinex
    cryptocom
    defx
    delta
    deribit
    digifinex
    gate
    hitbtc
    htx
    hyperliquid
    kucoinfutures
    mexc
    okx
    paradex
    whitebit
    woofipro
    xt

fetchPositionHistory

fetches historical positions

Kind: instance
Returns: Array<object> - a list of position structures
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified contract symbol
since 	int 	No 	the earliest time in ms to fetch positions for
limit 	int 	No 	the maximum amount of records to fetch
params 	object 	No 	extra parameters specific to the exchange api endpoint
params.until 	int 	No 	the latest time in ms to fetch positions for
Supported exchanges

    bingx
    coinex
    whitebit

fetchPositionMode

fetchs the position mode, hedged or one way, hedged for binance is set identically for all linear markets or all inverse markets

Kind: instance
Returns: object - an object detailing whether the market is in hedged or one-way mode
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to fetch the order book for
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.subType 	string 	No 	"linear" or "inverse"
Supported exchanges

    binance
    bingx
    bitmart
    coincatch
    mexc
    okx
    poloniex

fetchPositionWs

fetch data on an open position

Kind: instance
Returns: object - a position structure
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol of the market the position is held in
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    binance

fetchPositions

fetch all open positions

Kind: instance
Returns: Array<object> - a list of position structure
Param 	Type 	Required 	Description
symbols 	Array<string> 	No 	list of unified market symbols
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    apex
    ascendex
    binance
    bingx
    bitfinex
    bitflyer
    bitget
    bitmart
    bitmex
    blofin
    bybit
    coinbase
    coinbaseinternational
    coincatch
    coinex
    cryptocom
    defx
    delta
    deribit
    derive
    digifinex
    gate
    hashkey
    hitbtc
    htx
    hyperliquid
    kraken
    krakenfutures
    kucoinfutures
    mexc
    okx
    oxfun
    paradex
    phemex
    poloniex
    vertex
    whitebit
    woofipro
    xt

fetchPositionsForSymbol

fetch all open positions for specific symbol

Kind: instance
Returns: Array<object> - a list of position structure
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    coincatch
    hashkey
    okx

fetchPositionsHistory

fetches historical positions

Kind: instance
Returns: Array<object> - a list of position structures
Param 	Type 	Required 	Description
symbols 	Array<string> 	No 	unified contract symbols
since 	int 	No 	timestamp in ms of the earliest position to fetch, default=3 months ago, max range for params["until"] - since is 3 months
limit 	int 	No 	the maximum amount of records to fetch, default=20, max=100
params 	object 	Yes 	extra parameters specific to the exchange api endpoint
params.until 	int 	No 	timestamp in ms of the latest position to fetch, max range for params["until"] - since is 3 months EXCHANGE SPECIFIC PARAMETERS
params.productType 	string 	No 	USDT-FUTURES (default), COIN-FUTURES, USDC-FUTURES, SUSDT-FUTURES, SCOIN-FUTURES, or SUSDC-FUTURES
Supported exchanges

    bitget
    bybit
    gate
    kucoinfutures
    mexc
    okx

fetchPositionsWs

fetch all open positions

Kind: instance
Returns: Array<object> - a list of position structure
Param 	Type 	Required 	Description
symbols 	Array<string> 	No 	list of unified market symbols
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.returnRateLimits 	boolean 	No 	set to true to return rate limit informations, defaults to false.
params.method 	string, undefined 	No 	method to use. Can be account.position or v2/account.position
Supported exchanges

    binance

fetchSettlementHistory

fetches historical settlement records

Kind: instance
Returns: Array<object> - a list of settlement history objects
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol of the settlement history
since 	int 	No 	timestamp in ms
limit 	int 	No 	number of records, default 100, max 100
params 	object 	No 	exchange specific params
Supported exchanges

    binance
    bybit
    cryptocom
    delta
    gate
    htx
    okx

fetchSpotMarkets

retrieves data on all spot markets for hyperliquid

Kind: instance
Returns: Array<object> - an array of objects representing market data
Param 	Type 	Required 	Description
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    hyperliquid

fetchStatus

the latest known information on the availability of the exchange API

Kind: instance
Returns: object - a status structure
Param 	Type 	Required 	Description
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    binance
    bitbns
    bitfinex
    bitmart
    bitrue
    coinsph
    defx
    delta
    deribit
    digifinex
    hashkey
    htx
    idex
    kraken
    kucoin
    kucoinfutures
    mexc
    okx
    paradex
    vertex
    whitebit
    woo
    woofipro

fetchSwapMarkets

retrieves data on all swap markets for hyperliquid

Kind: instance
Returns: Array<object> - an array of objects representing market data
Param 	Type 	Required 	Description
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    hyperliquid

fetchTicker

fetches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market

Kind: instance
Returns: object - a ticker structure
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to fetch the ticker for
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.loc 	string 	No 	crypto location, default: us
Supported exchanges

    alpaca
    apex
    ascendex
    bigone
    binance
    bingx
    bit2c
    bitbank
    bitfinex
    bitflyer
    bitget
    bithumb
    bitmart
    bitmex
    bitopro
    bitrue
    bitso
    bitstamp
    bitteam
    bitvavo
    bl3p
    blockchaincom
    blofin
    btcalpha
    btcbox
    btcmarkets
    btcturk
    bybit
    cex
    coinbase
    coinbaseexchange
    coinbaseinternational
    coincatch
    coincheck
    coinex
    coinlist
    coinmate
    coinone
    coinsph
    coinspot
    cryptocom
    defx
    delta
    deribit
    derive
    digifinex
    ellipx
    exmo
    gate
    gemini
    hashkey
    hitbtc
    hollaex
    htx
    huobijp
    idex
    independentreserve
    indodax
    kraken
    kucoin
    kucoinfutures
    kuna
    latoken
    lbank
    luno
    mercado
    mexc
    ndax
    novadax
    oceanex
    okcoin
    okx
    onetrading
    oxfun
    p2b
    paradex
    paymium
    phemex
    poloniex
    probit
    timex
    tokocrypto
    tradeogre
    upbit
    wavesexchange
    whitebit
    xt
    yobit
    zaif
    zonda

fetchTickerWs

fetches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market

Kind: instance
Returns: object - a ticker structure
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to fetch the ticker for
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.method 	string 	No 	method to use can be ticker.price or ticker.book
params.returnRateLimits 	boolean 	No 	return the rate limits for the exchange
Supported exchanges

    binance
    cex
    lbank

fetchTickers

fetches price tickers for multiple markets, statistical information calculated over the past 24 hours for each market

Kind: instance
Returns: object - a dictionary of ticker structures
Param 	Type 	Required 	Description
symbols 	Array<string> 	Yes 	unified symbols of the markets to fetch tickers for
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.loc 	string 	No 	crypto location, default: us
Supported exchanges

    alpaca
    apex
    ascendex
    bigone
    binance
    bingx
    bitbns
    bitfinex
    bitget
    bithumb
    bitmart
    bitmex
    bitopro
    bitrue
    bitstamp
    bitteam
    bitvavo
    blockchaincom
    blofin
    btcalpha
    btcbox
    btcturk
    bybit
    cex
    coinbase
    coinbaseexchange
    coinbaseinternational
    coincatch
    coinex
    coinlist
    coinmate
    coinmetro
    coinone
    coinsph
    coinspot
    cryptocom
    cryptomus
    defx
    delta
    deribit
    digifinex
    exmo
    gate
    gemini
    hashkey
    hitbtc
    hollaex
    htx
    huobijp
    hyperliquid
    idex
    indodax
    kraken
    krakenfutures
    kucoin
    kucoinfutures
    kuna
    latoken
    lbank
    luno
    mexc
    novadax
    oceanex
    okcoin
    okx
    onetrading
    oxfun
    p2b
    paradex
    phemex
    poloniex
    probit
    timex
    tokocrypto
    tradeogre
    upbit
    vertex
    wavesexchange
    whitebit
    xt
    yobit

fetchTime

fetches the current integer timestamp in milliseconds from the exchange server

Kind: instance
Returns: int - the current integer timestamp in milliseconds from the exchange server
Param 	Type 	Required 	Description
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    alpaca
    apex
    ascendex
    bigone
    binance
    bingx
    bitget
    bitmart
    bitrue
    bitvavo
    btcmarkets
    bybit
    cex
    coinbase
    coinbaseexchange
    coincatch
    coinex
    coinlist
    coinsph
    defx
    delta
    deribit
    derive
    digifinex
    gate
    hashkey
    htx
    huobijp
    idex
    indodax
    kraken
    kucoin
    kucoinfutures
    kuna
    latoken
    lbank
    mexc
    novadax
    oceanex
    okcoin
    okx
    onetrading
    paradex
    poloniex
    probit
    timex
    tokocrypto
    vertex
    whitebit
    woo
    woofipro
    xt

fetchTrades

get the list of most recent trades for a particular symbol

Kind: instance
Returns: Array<Trade> - a list of trade structures
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to fetch trades for
since 	int 	No 	timestamp in ms of the earliest trade to fetch
limit 	int 	No 	the maximum amount of trades to fetch
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.loc 	string 	No 	crypto location, default: us
params.method 	string 	No 	method, default: marketPublicGetV1beta3CryptoLocTrades
Supported exchanges

    alpaca
    apex
    ascendex
    bigone
    binance
    bingx
    bit2c
    bitbank
    bitbns
    bitfinex
    bitflyer
    bitget
    bithumb
    bitmart
    bitmex
    bitopro
    bitrue
    bitso
    bitstamp
    bitteam
    bitvavo
    bl3p
    blofin
    btcalpha
    btcbox
    btcmarkets
    btcturk
    bybit
    cex
    coinbase
    coinbaseexchange
    coincatch
    coincheck
    coinex
    coinlist
    coinmate
    coinmetro
    coinone
    coinsph
    coinspot
    cryptocom
    cryptomus
    defx
    delta
    deribit
    derive
    digifinex
    ellipx
    exmo
    gate
    gemini
    hashkey
    hitbtc
    hollaex
    htx
    huobijp
    hyperliquid
    idex
    independentreserve
    indodax
    kraken
    krakenfutures
    kucoin
    kucoinfutures
    kuna
    latoken
    lbank
    luno
    mercado
    mexc
    ndax
    novadax
    oceanex
    okcoin
    okx
    oxfun
    p2b
    paradex
    paymium
    phemex
    poloniex
    probit
    timex
    tokocrypto
    tradeogre
    upbit
    vertex
    wavesexchange
    whitebit
    woo
    woofipro
    xt
    yobit
    zaif
    zonda

fetchTradesWs

fetch all trades made by the user

Kind: instance
Returns: Array<object> - a list of trade structures
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol
since 	int 	No 	the earliest time in ms to fetch trades for
limit 	int 	No 	the maximum number of trades structures to retrieve, default=500, max=1000
params 	object 	No 	extra parameters specific to the exchange API endpoint EXCHANGE SPECIFIC PARAMETERS
params.fromId 	int 	No 	trade ID to begin at
Supported exchanges

    binance
    lbank

fetchTradingFee

fetch the trading fees for a market

Kind: instance
Returns: object - a fee structure
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.portfolioMargin 	boolean 	No 	set to true if you would like to fetch trading fees in a portfolio margin account
params.subType 	string 	No 	"linear" or "inverse"
Supported exchanges

    binance
    bingx
    bitflyer
    bitget
    bitmart
    bitstamp
    bybit
    coinex
    coinmate
    coinsph
    cryptocom
    digifinex
    ellipx
    gate
    hashkey
    hitbtc
    htx
    hyperliquid
    kraken
    kucoin
    kucoinfutures
    latoken
    lbank
    luno
    mexc
    okx
    timex
    upbit

fetchTradingFees

fetch the trading fees for multiple markets

Kind: instance
Returns: object - a dictionary of fee structures indexed by market symbols
Param 	Type 	Required 	Description
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    ascendex
    binance
    bit2c
    bitbank
    bitfinex
    bitget
    bitopro
    bitso
    bitstamp
    bitvavo
    bl3p
    blockchaincom
    bybit
    cex
    coinbase
    coinbaseexchange
    coincheck
    coinex
    coinlist
    coinsph
    cryptocom
    cryptomus
    deribit
    exmo
    gate
    gemini
    hashkey
    hitbtc
    hollaex
    idex
    independentreserve
    lbank
    oceanex
    onetrading
    poloniex
    upbit
    vertex
    whitebit
    woo
    woofipro
    yobit

fetchTradingFeesWs

fetch the trading fees for multiple markets

Kind: instance
Returns: object - a dictionary of fee structures indexed by market symbols
Param 	Type 	Required 	Description
params 	object 	No 	extra parameters specific to the bitvavo api endpoint
Supported exchanges

    bitvavo

fetchTransactionFee

please use fetchDepositWithdrawFee instead

Kind: instance
Returns: object - a fee structure
Param 	Type 	Required 	Description
code 	string 	Yes 	unified currency code
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.network 	string 	No 	the network code of the currency
Supported exchanges

    bitmart
    indodax
    kucoin

fetchTransactionFees

please use fetchDepositWithdrawFees instead

Kind: instance
Returns: Array<object> - a list of fee structures
Param 	Type 	Required 	Description
codes 	Array<string>, undefined 	Yes 	not used by binance fetchTransactionFees ()
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    binance
    bitso
    bitstamp
    exmo
    gate
    lbank
    mexc
    whitebit

fetchTransactions

use fetchDepositsWithdrawals instead

Kind: instance
Returns: object - a list of transaction structure
Param 	Type 	Required 	Description
code 	string 	Yes 	unified currency code for the currency of the transactions, default is undefined
since 	int 	No 	timestamp in ms of the earliest transaction, default is undefined
limit 	int 	No 	max number of transactions to return, default is undefined
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    latoken

fetchTransfer

fetches a transfer

Kind: instance
Returns: object - a transfer structure
Param 	Type 	Required 	Description
id 	string 	Yes 	transfer id
code 	string 	No 	not used by mexc fetchTransfer
params 	object 	Yes 	extra parameters specific to the exchange api endpoint
Supported exchanges

    mexc

fetchTransfers

fetch a history of internal transfers made on an account

Kind: instance
Returns: Array<object> - a list of transfer structures
Param 	Type 	Required 	Description
code 	string 	Yes 	unified currency code of the currency transferred
since 	int 	No 	the earliest time in ms to fetch transfers for
limit 	int 	No 	the maximum number of transfers structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.until 	int 	No 	the latest time in ms to fetch transfers for
params.paginate 	boolean 	No 	default false, when true will automatically paginate by calling this endpoint multiple times. See in the docs all the available parameters
params.internal 	boolean 	No 	default false, when true will fetch pay trade history
Supported exchanges

    binance
    bingx
    bitget
    bitmart
    bitrue
    bybit
    coinbaseinternational
    coinex
    coinlist
    deribit
    digifinex
    latoken
    mexc
    okx
    oxfun
    paradex
    phemex
    woo

fetchUnderlyingAssets

fetches the market ids of underlying assets for a specific contract market type

Kind: instance
Returns: Array<object> - a list of underlying assets
Param 	Type 	Required 	Description
params 	object 	No 	exchange specific params
params.type 	string 	No 	the contract market type, 'option', 'swap' or 'future', the default is 'option'
Supported exchanges

    gate
    okx

fetchVolatilityHistory

fetch the historical volatility of an option market based on an underlying asset

Kind: instance
Returns: Array<object> - a list of volatility history objects
Param 	Type 	Required 	Description
code 	string 	Yes 	unified currency code
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.period 	int 	No 	the period in days to fetch the volatility for: 7,14,21,30,60,90,180,270
Supported exchanges

    bybit
    deribit

fetchWithdrawal

fetch data on a currency withdrawal via the withdrawal id

Kind: instance
Returns: object - a transaction structure
Param 	Type 	Required 	Description
id 	string 	Yes 	withdrawal id
code 	string 	Yes 	not used by bitmart.fetchWithdrawal
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    bitmart
    bitopro
    blockchaincom
    exmo
    hollaex
    idex
    kuna
    okx
    upbit

fetchWithdrawals

fetch all withdrawals made from an account

Kind: instance
Returns: Array<object> - a list of transaction structures
Param 	Type 	Required 	Description
code 	string 	No 	unified currency code
since 	int 	No 	the earliest time in ms to fetch withdrawals for
limit 	int 	No 	the maximum number of withdrawal structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    alpaca
    ascendex
    bigone
    binance
    bingx
    bitbns
    bitflyer
    bitget
    bitmart
    bitopro
    bitrue
    bitstamp
    bitvavo
    blockchaincom
    blofin
    btcalpha
    btcmarkets
    bybit
    coinbase
    coinbaseexchange
    coinbaseinternational
    coincatch
    coincheck
    coinex
    coinsph
    cryptocom
    deribit
    derive
    digifinex
    exmo
    gate
    hashkey
    hitbtc
    hollaex
    htx
    huobijp
    hyperliquid
    idex
    kraken
    kucoin
    kucoinfutures
    kuna
    lbank
    mexc
    ndax
    novadax
    okcoin
    okx
    oxfun
    paradex
    phemex
    poloniex
    probit
    timex
    tokocrypto
    upbit
    woo
    woofipro
    xt

fetchWithdrawalsWs

fetch all withdrawals made from an account

Kind: instance
Returns: Array<object> - a list of transaction structures
Param 	Type 	Required 	Description
code 	string 	Yes 	unified currency code
since 	int 	No 	the earliest time in ms to fetch withdrawals for
limit 	int 	No 	the maximum number of withdrawals structures to retrieve
params 	object 	No 	extra parameters specific to the bitvavo api endpoint
Supported exchanges

    bitvavo

isUnifiedEnabled

returns [enableUnifiedMargin, enableUnifiedAccount] so the user can check if unified account is enabled

Kind: instance
Returns: any - [enableUnifiedMargin, enableUnifiedAccount]
Param 	Type 	Required 	Description
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    bybit

loadMigrationStatus

loads the migration status for the account (hf or not)

Kind: instance
Returns: any - ignore
Param 	Type 	Description
force 	boolean 	load account state for non hf
Supported exchanges

    kucoin

loadUnifiedStatus

returns unifiedAccount so the user can check if the unified account is enabled

Kind: instance
Returns: boolean - true or false if the enabled unified account is enabled or not and sets the unifiedAccount option if it is undefined
Param 	Type 	Required 	Description
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    gate

market

calculates the presumptive fee that would be charged for an order

Kind: instance
Returns: object - contains the rate, the percentage multiplied to the order amount to obtain the fee amount, and cost, the total value of the fee in units of the quote currency, for the order
Param 	Type 	Description
symbol 	string 	unified market symbol
type 	string 	not used by btcmarkets.calculateFee
side 	string 	not used by btcmarkets.calculateFee
amount 	float 	how much you want to trade, in units of the base currency on most exchanges, or number of contracts
price 	float 	the price for the order to be filled at, in units of the quote currency
takerOrMaker 	string 	'taker' or 'maker'
params 	object 	
Supported exchanges

    <anonymous>

redeemGiftCode

redeem gift code

Kind: instance
Returns: object - response from the exchange
Param 	Type 	Required 	Description
giftcardCode 	string 	Yes 	
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    binance

reduceMargin

remove margin from a position

Kind: instance
Returns: object - a margin structure
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol
amount 	float 	Yes 	the amount of margin to remove
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    ascendex
    binance
    bitget
    coincatch
    coinex
    delta
    digifinex
    exmo
    gate
    hitbtc
    hyperliquid
    mexc
    okx
    poloniex
    woo
    xt

repayCrossMargin

repay borrowed margin and interest

Kind: instance
Returns: object - a margin loan structure
Param 	Type 	Required 	Description
code 	string 	Yes 	unified currency code of the currency to repay
amount 	float 	Yes 	the amount to repay
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.portfolioMargin 	boolean 	No 	set to true if you would like to repay margin in a portfolio margin account
params.repayCrossMarginMethod 	string 	No 	portfolio margin only 'papiPostRepayLoan' (default), 'papiPostMarginRepayDebt' (alternative)
params.specifyRepayAssets 	string 	No 	portfolio margin papiPostMarginRepayDebt only specific asset list to repay debt
Supported exchanges

    binance
    bitget
    bybit
    gate
    htx
    kucoin
    okx

repayIsolatedMargin

repay borrowed margin and interest

Kind: instance
Returns: object - a margin loan structure
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol, required for isolated margin
code 	string 	Yes 	unified currency code of the currency to repay
amount 	float 	Yes 	the amount to repay
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    binance
    bitget
    bitmart
    coinex
    htx
    kucoin

repayMargin

repay borrowed margin and interest

Kind: instance
Returns: object - a margin loan structure
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol
code 	string 	Yes 	unified currency code of the currency to repay
amount 	float 	Yes 	the amount to repay
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.mode 	string 	No 	'all' or 'partial' payment mode, extra parameter required for isolated margin
params.id 	string 	No 	'34267567' loan id, extra parameter required for isolated margin
Supported exchanges

    gate
    woo

setLeverage

set the level of leverage for a market

Kind: instance
Returns: object - response from the exchange
Param 	Type 	Required 	Description
leverage 	float 	Yes 	the rate of leverage
symbol 	string 	Yes 	unified market symbol
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    apex
    ascendex
    binance
    bingx
    bitget
    bitmart
    bitmex
    bitrue
    blofin
    bybit
    coincatch
    coinex
    defx
    delta
    digifinex
    gate
    hashkey
    hitbtc
    htx
    hyperliquid
    krakenfutures
    kucoin
    kucoinfutures
    mexc
    okx
    paradex
    phemex
    poloniex
    whitebit
    woo
    woofipro
    xt

setMargin

Either adds or reduces margin in an isolated position in order to set the margin to a specific value

Kind: instance
Returns: object - A margin structure
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol of the market to set margin in
amount 	float 	Yes 	the amount to set the margin to
params 	object 	No 	parameters specific to the bingx api endpoint
Supported exchanges

    bingx
    bitfinex
    bitrue
    coinbaseinternational
    phemex

setMarginMode

set margin mode to 'cross' or 'isolated'

Kind: instance
Returns: object - response from the exchange
Param 	Type 	Required 	Description
marginMode 	string 	Yes 	'cross' or 'isolated'
symbol 	string 	Yes 	unified market symbol
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    ascendex
    binance
    bingx
    bitget
    bitmex
    bybit
    coincatch
    coinex
    digifinex
    hyperliquid
    kucoinfutures
    mexc
    okx
    paradex
    phemex
    xt

setPositionMode

set hedged to true or false for a market

Kind: instance
Returns: object - response from the exchange
Param 	Type 	Required 	Description
hedged 	bool 	Yes 	set to true to use dualSidePosition
symbol 	string 	Yes 	not used by binance setPositionMode ()
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.portfolioMargin 	boolean 	No 	set to true if you would like to set the position mode for a portfolio margin account
params.subType 	string 	No 	"linear" or "inverse"
Supported exchanges

    binance
    bingx
    bitget
    bitmart
    bybit
    coincatch
    gate
    htx
    mexc
    okx
    phemex
    poloniex
    woo

signIn

sign in, must be called prior to using other authenticated methods

Kind: instance
Returns: response from exchange
Param 	Type 	Required 	Description
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    ndax
    probit
    wavesexchange

transfer

transfer currency internally between wallets on the same account

Kind: instance
Returns: object - a transfer structure
Param 	Type 	Required 	Description
code 	string 	Yes 	unified currency code
amount 	float 	Yes 	amount to transfer
fromAccount 	string 	Yes 	account to transfer from
toAccount 	string 	Yes 	account to transfer to
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.transferId 	string 	No 	UUID, which is unique across the platform
Supported exchanges

    apex
    ascendex
    bigone
    binance
    bingx
    bitfinex
    bitget
    bitmart
    bitrue
    bitstamp
    blofin
    bybit
    cex
    coinbaseinternational
    coincatch
    coinex
    coinlist
    deribit
    digifinex
    gate
    hashkey
    hitbtc
    htx
    hyperliquid
    kraken
    krakenfutures
    kucoin
    kucoinfutures
    latoken
    mexc
    novadax
    okcoin
    okx
    oxfun
    paymium
    phemex
    poloniex
    whitebit
    woo
    xt
    zonda

transferOut

transfer from spot wallet to futures wallet

Kind: instance
Returns: a transfer structure
Param 	Type 	Required 	Description
code 	str 	Yes 	Unified currency code
amount 	float 	Yes 	Size of the transfer
params 	dict 	No 	Exchange specific parameters
Supported exchanges

    kraken
    krakenfutures

unWatchMyTrades

unWatches information on multiple trades made by the user

Kind: instance
Returns: Array<object> - a list of order structures
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol of the market orders were made in
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.unifiedMargin 	boolean 	No 	use unified margin account
Supported exchanges

    bybit

unWatchOHLCV

unWatches historical candlestick data containing the open, high, low, and close price, and the volume of a market

Kind: instance
Returns: Array<Array<int>> - A list of candles ordered as timestamp, open, high, low, close, volume
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to fetch OHLCV data for
timeframe 	string 	Yes 	the length of time each candle represents
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.timezone 	object 	No 	if provided, kline intervals are interpreted in that timezone instead of UTC, example '+08:00'
Supported exchanges

    binance
    bitget
    bybit
    coincatch
    cryptocom
    defx
    hyperliquid
    okx

unWatchOHLCVForSymbols

unWatches historical candlestick data containing the open, high, low, and close price, and the volume of a market

Kind: instance
Returns: Array<Array<int>> - A list of candles ordered as timestamp, open, high, low, close, volume
Param 	Type 	Required 	Description
symbolsAndTimeframes 	Array<Array<string>> 	Yes 	array of arrays containing unified symbols and timeframes to fetch OHLCV data for, example [['BTC/USDT', '1m'], ['LTC/USDT', '5m']]
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.timezone 	object 	No 	if provided, kline intervals are interpreted in that timezone instead of UTC, example '+08:00'
Supported exchanges

    binance
    bybit
    defx
    okx

unWatchOrderBook

unWatches information on open orders with bid (buy) and ask (sell) prices, volumes and other data

Kind: instance
Returns: object - A dictionary of order book structures indexed by market symbols
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified array of symbols
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    binance
    bitget
    bybit
    coincatch
    cryptocom
    defx
    derive
    gate
    hyperliquid
    kucoin
    kucoinfutures
    okx

unWatchOrderBookForSymbols

unWatches information on open orders with bid (buy) and ask (sell) prices, volumes and other data

Kind: instance
Returns: object - A dictionary of order book structures indexed by market symbols
Param 	Type 	Required 	Description
symbols 	Array<string> 	Yes 	unified array of symbols
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    binance
    bybit
    cryptocom
    defx
    kucoin
    kucoinfutures
    okx

unWatchOrders

unWatches information on multiple orders made by the user

Kind: instance
Returns: Array<object> - a list of order structures
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol of the market orders were made in
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.unifiedMargin 	boolean 	No 	use unified margin account
Supported exchanges

    bybit

unWatchTicker

unWatches a price ticker, a statistical calculation with the information calculated over the past 24 hours for all markets of a specific list

Kind: instance
Returns: object - a ticker structure
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to fetch the ticker for
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    binance
    bitget
    bybit
    coincatch
    cryptocom
    defx
    okx

unWatchTickers

unWatches a price ticker, a statistical calculation with the information calculated over the past 24 hours for all markets of a specific list

Kind: instance
Returns: object - a ticker structure
Param 	Type 	Required 	Description
symbols 	Array<string> 	Yes 	unified symbol of the market to fetch the ticker for
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    binance
    bybit
    cryptocom
    defx
    hyperliquid
    okx

unWatchTrades

unsubscribes from the trades channel

Kind: instance
Returns: Array<object> - a list of trade structures
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to fetch trades for
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.name 	string 	No 	the name of the method to call, 'trade' or 'aggTrade', default is 'trade'
Supported exchanges

    binance
    bitget
    bybit
    coincatch
    cryptocom
    defx
    derive
    gate
    hyperliquid
    kucoin
    kucoinfutures
    okx

unWatchTradesForSymbols

unsubscribes from the trades channel

Kind: instance
Returns: Array<object> - a list of trade structures
Param 	Type 	Required 	Description
symbols 	Array<string> 	Yes 	unified symbol of the market to fetch trades for
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.name 	string 	No 	the name of the method to call, 'trade' or 'aggTrade', default is 'trade'
Supported exchanges

    binance
    bybit
    cryptocom
    defx
    gate
    kucoin
    kucoinfutures
    okx

upgradeUnifiedTradeAccount

upgrades the account to unified trade account warning this is irreversible

Kind: instance
Returns: any - nothing
Param 	Type 	Required 	Description
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    bybit

verifyGiftCode

verify gift code

Kind: instance
Returns: object - response from the exchange
Param 	Type 	Required 	Description
id 	string 	Yes 	reference number id
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    binance

watchBalance

watch balance and get the amount of funds available for trading or funds locked in orders

Kind: instance
Returns: object - a balance structure
Param 	Type 	Required 	Description
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    ascendex
    binance
    bingx
    bitfinex
    bitget
    bitmart
    bitmex
    bitopro
    bitrue
    blockchaincom
    blofin
    bybit
    cex
    coincatch
    coinex
    cryptocom
    defx
    deribit
    exmo
    gate
    hashkey
    hollaex
    htx
    kucoin
    kucoinfutures
    mexc
    okcoin
    okx
    onetrading
    oxfun
    phemex
    probit
    upbit
    whitebit
    woo
    woofipro

watchBidsAsks

watches best bid & ask for symbols

Kind: instance
Returns: object - a ticker structure
Param 	Type 	Required 	Description
symbols 	Array<string> 	Yes 	unified symbol of the market to fetch the ticker for
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    binance
    bitget
    bitmart
    bitvavo
    blofin
    bybit
    coinex
    cryptocom
    defx
    deribit
    gate
    gemini
    kucoin
    kucoinfutures
    mexc
    okx
    oxfun
    woo
    woofipro

watchFundingRate

watch the current funding rate

Kind: instance
Returns: object - a funding rate structure
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    okx

watchFundingRates

watch the funding rate for multiple markets

Kind: instance
Returns: object - a dictionary of funding rates structures, indexe by market symbols
Param 	Type 	Required 	Description
symbols 	Array<string> 	Yes 	list of unified market symbols
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    coinbaseinternational

watchLiquidations

watch the public liquidations of a trading pair

Kind: instance
Returns: object - an array of liquidation structures
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified CCXT market symbol
since 	int 	No 	the earliest time in ms to fetch liquidations for
limit 	int 	No 	the maximum number of liquidation structures to retrieve
params 	object 	No 	exchange specific parameters for the bitmex api endpoint
Supported exchanges

    binance
    bitmex
    bybit

watchLiquidationsForSymbols

watch the public liquidations of a trading pair

Kind: instance
Returns: object - an array of liquidation structures
Param 	Type 	Required 	Description
symbols 	Array<string> 	Yes 	list of unified market symbols
since 	int 	No 	the earliest time in ms to fetch liquidations for
limit 	int 	No 	the maximum number of liquidation structures to retrieve
params 	object 	No 	exchange specific parameters for the bitmex api endpoint
Supported exchanges

    binance
    bitmex
    okx

watchMarkPrice

watches a mark price for a specific market

Kind: instance
Returns: object - a ticker structure
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to fetch the ticker for
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.use1sFreq 	boolean 	No 	default is true if set to true, the mark price will be updated every second, otherwise every 3 seconds
Supported exchanges

    binance
    okx

watchMarkPrices

watches the mark price for all markets

Kind: instance
Returns: object - a ticker structure
Param 	Type 	Required 	Description
symbols 	Array<string> 	Yes 	unified symbol of the market to fetch the ticker for
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.use1sFreq 	boolean 	No 	default is true if set to true, the mark price will be updated every second, otherwise every 3 seconds
Supported exchanges

    binance
    okx

watchMyLiquidations

watch the private liquidations of a trading pair

Kind: instance
Returns: object - an array of liquidation structures
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified CCXT market symbol
since 	int 	No 	the earliest time in ms to fetch liquidations for
limit 	int 	No 	the maximum number of liquidation structures to retrieve
params 	object 	No 	exchange specific parameters for the bitmex api endpoint
Supported exchanges

    binance
    gate

watchMyLiquidationsForSymbols

watch the private liquidations of a trading pair

Kind: instance
Returns: object - an array of liquidation structures
Param 	Type 	Required 	Description
symbols 	Array<string> 	Yes 	list of unified market symbols
since 	int 	No 	the earliest time in ms to fetch liquidations for
limit 	int 	No 	the maximum number of liquidation structures to retrieve
params 	object 	No 	exchange specific parameters for the bitmex api endpoint
Supported exchanges

    binance
    gate
    okx

watchMyTrades

watches information on multiple trades made by the user

Kind: instance
Returns: Array<object> - a list of trade structures
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol of the market trades were made in
since 	int 	No 	the earliest time in ms to fetch trades for
limit 	int 	No 	the maximum number of trade structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint
params.unifiedMargin 	boolean 	No 	use unified margin account
Supported exchanges

    alpaca
    apex
    binance
    bingx
    bitfinex
    bitget
    bitmex
    bitopro
    bitvavo
    bybit
    cex
    coinbaseexchange
    coinex
    cryptocom
    deribit
    derive
    exmo
    gate
    hashkey
    hollaex
    htx
    hyperliquid
    kucoin
    mexc
    okx
    onetrading
    phemex
    probit
    upbit
    vertex
    whitebit
    woo
    woofipro

watchMyTradesForSymbols

watches information on multiple trades made by the user

Kind: instance
Returns: Array<object> - a list of trade structures
Param 	Type 	Required 	Description
symbols 	Array<string> 	Yes 	unified symbol of the market to fetch trades for
since 	int 	No 	the earliest time in ms to fetch trades for
limit 	int 	No 	the maximum number of trade structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    coinbaseexchange

watchOHLCV

watches historical candlestick data containing the open, high, low, and close price, and the volume of a market

Kind: instance
Returns: Array<Array<int>> - A list of candles ordered as timestamp, open, high, low, close, volume
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to fetch OHLCV data for
timeframe 	string 	Yes 	the length of time each candle represents
since 	int 	No 	timestamp in ms of the earliest candle to fetch
limit 	int 	No 	the maximum amount of candles to fetch
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    alpaca
    apex
    ascendex
    binance
    bingx
    bitfinex
    bitget
    bitmart
    bitmex
    bitvavo
    blockchaincom
    blofin
    bybit
    cex
    coincatch
    cryptocom
    defx
    deribit
    gate
    gemini
    hashkey
    htx
    huobijp
    hyperliquid
    idex
    kucoin
    kucoinfutures
    lbank
    mexc
    ndax
    okcoin
    okx
    onetrading
    oxfun
    phemex
    whitebit
    woo
    woofipro

watchOHLCVForSymbols

watches historical candlestick data containing the open, high, low, and close price, and the volume of a market

Kind: instance
Returns: object - A list of candles ordered as timestamp, open, high, low, close, volume
Param 	Type 	Required 	Description
symbolsAndTimeframes 	Array<Array<string>> 	Yes 	array of arrays containing unified symbols and timeframes to fetch OHLCV data for, example [['BTC/USDT', '1m'], ['LTC/USDT', '5m']]
since 	int 	No 	timestamp in ms of the earliest candle to fetch
limit 	int 	No 	the maximum amount of candles to fetch
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    apex
    binance
    bingx
    blofin
    bybit
    defx
    deribit
    okx
    oxfun

watchOrderBook

watches information on open orders with bid (buy) and ask (sell) prices, volumes and other data

Kind: instance
Returns: object - A dictionary of order book structures indexed by market symbols
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to fetch the order book for
limit 	int 	No 	the maximum amount of order book entries to return.
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    alpaca
    apex
    ascendex
    binance
    bingx
    bitfinex
    bitget
    bithumb
    bitmart
    bitmex
    bitopro
    bitstamp
    bitvavo
    blockchaincom
    blofin
    bybit
    cex
    coinbaseexchange
    coincatch
    coincheck
    coinex
    coinone
    cryptocom
    defx
    deribit
    derive
    exmo
    gate
    gemini
    hashkey
    hollaex
    htx
    huobijp
    hyperliquid
    idex
    independentreserve
    kucoin
    kucoinfutures
    lbank
    luno
    mexc
    ndax
    okcoin
    okx
    onetrading
    oxfun
    phemex
    probit
    tradeogre
    upbit
    vertex
    whitebit
    woo
    woofipro

watchOrderBookForSymbols

watches information on open orders with bid (buy) and ask (sell) prices, volumes and other data

Kind: instance
Returns: object - A dictionary of order book structures indexed by market symbols
Param 	Type 	Required 	Description
symbols 	Array<string> 	Yes 	unified array of symbols
limit 	int 	No 	the maximum amount of order book entries to return.
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    apex
    binance
    bingx
    bitget
    bitmart
    bitmex
    blofin
    bybit
    coinbaseexchange
    coincatch
    coinex
    cryptocom
    defx
    deribit
    gemini
    kucoin
    kucoinfutures
    okx
    oxfun

watchOrders

watches information on multiple orders made by the user

Kind: instance
Returns: Array<object> - a list of order structures
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol of the market orders were made in
since 	int 	No 	the earliest time in ms to fetch orders for
limit 	int 	No 	the maximum number of order structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    alpaca
    apex
    ascendex
    binance
    bingx
    bitfinex
    bitget
    bitmart
    bitmex
    bitrue
    bitstamp
    bitvavo
    biofin
    bybit
    cex
    coinbaseexchange
    coincatch
    coinex
    cryptocom
    defx
    deribit
    derive
    exmo
    gate
    hashkey
    hollaex
    htx
    hyperliquid
    idex
    kucoin
    kucoinfutures
    lbank
    mexc
    okcoin
    okx
    onetrading
    oxfun
    phemex
    probit
    upbit
    vertex
    whitebit
    woo
    woofipro

watchOrdersForSymbols

watches information on multiple orders made by the user across multiple symbols

Kind: instance
Returns: Array<object> - a list of [order structures]{@link https://docs.ccxt.com/#/?id=order-structure
Param 	Type 	Required 	Description
symbols 	Array<string> 	Yes 	
since 	int 	No 	the earliest time in ms to fetch orders for
limit 	int 	No 	the maximum number of order structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    blofin
    coinbaseexchange

watchPosition

watch open positions for a specific symbol

Kind: instance
Returns: object - a position structure
Param 	Type 	Description
symbol 	string, undefined 	unified market symbol
params 	object 	extra parameters specific to the exchange API endpoint
Supported exchanges

    kucoinfutures

watchPositions

watch all open positions

Kind: instance
Returns: Array<object> - a list of position structure
Param 	Type 	Required 	Description
symbols 	Array<string> 	No 	list of unified market symbols
since 	int 	No 	the earliest time in ms to fetch positions for
limit 	int 	No 	the maximum number of positions to retrieve
params 	object 	Yes 	extra parameters specific to the exchange API endpoint
Supported exchanges

    apex
    binance
    bitget
    bitmart
    bitmex
    blofin
    bybit
    coincatch
    cryptocom
    defx
    gate
    hashkey
    htx
    okx
    oxfun
    vertex
    woo
    woofipro

watchTicker

watches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market

Kind: instance
Returns: object - a ticker structure
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified symbol of the market to fetch the ticker for
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    alpaca
    apex
    binance
    bingx
    bitfinex
    bitget
    bithumb
    bitmart
    bitmex
    bitopro
    bitvavo
    blockchaincom
    blofin
    bybit
    cex
    coinbaseexchange
    coincatch
    coinex
    coinone
    cryptocom
    defx
    deribit
    derive
    exmo
    gate
    hahskey
    htx
    huobijp
    hyperliquid
    idex
    kucoin
    kucoinfutures
    lbank
    mexc
    ndax
    okcoin
    okx
    onetrading
    oxfun
    phemex
    probit
    upbit
    vertex
    whitebit
    woo
    woofipro

watchTickers

watches a price ticker, a statistical calculation with the information calculated over the past 24 hours for all markets of a specific list

Kind: instance
Returns: object - a ticker structure
Param 	Type 	Required 	Description
symbols 	Array<string> 	Yes 	unified symbol of the market to fetch the ticker for
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    apex
    binance
    bingx
    bitget
    bithumb
    bitmart
    bitmex
    bitvavo
    blofin
    bybit
    cex
    coinbaseexchange
    coincatch
    coinex
    cryptocom
    defx
    deribit
    exmo
    gate
    hyperliquid
    kucoin
    kucoinfutures
    mexc
    okx
    onetrading
    oxfun
    phemex
    upbit
    whitebit
    woo
    woofipro

watchTrades

watches information on multiple trades made in a market

Kind: instance
Returns: Array<object> - a list of trade structures
Param 	Type 	Required 	Description
symbol 	string 	Yes 	unified market symbol of the market trades were made in
since 	int 	No 	the earliest time in ms to fetch orders for
limit 	int 	No 	the maximum number of trade structures to retrieve
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    alpaca
    apex
    ascendex
    binance
    bingx
    bitfinex
    bitget
    bithumb
    bitmart
    bitmex
    bitopro
    bitstamp
    bitvavo
    blockchaincom
    blofin
    bybit
    cex
    coinbaseexchange
    coincatch
    coincheck
    coinex
    coinone
    cryptocom
    defx
    deribit
    derive
    exmo
    gate
    gemini
    hashkey
    hollaex
    htx
    huobijp
    idex
    independentreserve
    kucoin
    kucoinfutures
    lbank
    luno
    mexc
    ndax
    okcoin
    okx
    oxfun
    phemex
    probit
    tradeogre
    upbit
    vertex
    whitebit
    woo
    woofipro

watchTradesForSymbols

get the list of most recent trades for a list of symbols

Kind: instance
Returns: Array<object> - a list of trade structures
Param 	Type 	Required 	Description
symbols 	Array<string> 	Yes 	unified symbol of the market to fetch trades for
since 	int 	No 	timestamp in ms of the earliest trade to fetch
limit 	int 	No 	the maximum amount of trades to fetch
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    apex
    ascendex
    binance
    bitget
    bitmart
    bitmex
    blofin
    bybit
    coinbase
    coincatch
    coinex
    cryptocom
    defx
    deribit
    gate
    gemini
    kucoin
    kucoinfutures
    okx
    oxfun
    tradeogre
    upbit

withdraw

make a withdrawal

Kind: instance
Returns: object - a transaction structure
Param 	Type 	Required 	Description
code 	string 	Yes 	unified currency code
amount 	float 	Yes 	the amount to withdraw
address 	string 	Yes 	the address to withdraw to
tag 	string 	Yes 	a memo for the transaction
params 	object 	No 	extra parameters specific to the exchange API endpoint
Supported exchanges

    alpaca
    bigone
    binance
    bingx
    bitbank
    bitfinex
    bitflyer
    bitget
    bithumb
    bitmart
    bitmex
    bitopro
    bitrue
    bitso
    bitstamp
    bitvavo
    blockchaincom
    btcmarkets
    bybit
    coinbase
    coinbaseexchange
    coinbaseinternational
    coincatch
    coinex
    coinlist
    coinmate
    coinsph
    cryptocom
    defx
    deribit
    digifinex
    ellipx
    exmo
    gate
    gemini
    hashkey
    hitbtc
    hollaex
    htx
    huobijp
    hyperliquid
    idex
    independentreserve
    indodax
    kraken
    kucoin
    kuna
    lbank
    mercado
    mexc
    ndax
    novadax
    okcoin
    okx
    oxfun
    phemex
    poloniex
    probit
    tokocrypto
    upbit
    vertex
    wavesexchange
    whitebit
    woo
    woofipro
    xt
    yobit
    zaif
    zonda

withdrawWs

make a withdrawal

Kind: instance
Returns: object - a transaction structure
Param 	Type 	Required 	Description
code 	string 	Yes 	unified currency code
amount 	float 	Yes 	the amount to withdraw
address 	string 	Yes 	the address to withdraw to
tag 	string 	Yes 	
params 	object 	No 	extra parameters specific to the bitvavo api endpoint
Supported exchanges

    bitvavo