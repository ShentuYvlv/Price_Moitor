This is the list of exchanges in CCXT Pro with support for WebSockets APIs. This list will be updated with new exchanges on a regular basis.

Full list of exchanges available in CCXT via REST: Supported Cryptocurrency Exchange Markets.
Usage

- this part of the doc is under heavy development right now
- there may be some typos, mistakes and missing info here and there
- contributions, pull requests and feedback appreciated

Prerequisites

The best way to understand CCXT Pro is to make sure you grasp the entire CCXT Manual and practice standard CCXT first. CCXT Pro borrows from CCXT. The two libraries share a lot of commonalities, including:

    the concepts of public API and private authenticated API
    markets, symbols, currency codes and ids
    unified data structures and formats, orderbooks, trades, orders, candles, timeframes, ...
    exceptions and error mappings
    authentication and API keys (for private feeds and calls)
    configuration options

The CCXT Pro audience consists mostly of professional algorithmic traders and developers. In order to work efficiently with this library the user is required to be well-familiar with the concepts of streaming. One has to understand the underlying differences between connection-based streaming APIs (WebSocket, CCXT Pro) and request-response based APIs (REST, CCXT).

The general async-style flow for a CCXT application is as follows:


// a RESTful orderbook polling request-response loop

while (condition) {

    try {

        // fetch some of the public data
        orderbook = await exchange.fetchOrderBook (symbol, limit)

        // do something or react somehow based on that data
        // ...

    } catch (e) {

        // handle errors
    }
}

In CCXT Pro each public and private unified RESTful method having a fetch* prefix also has a corresponding stream-based counterpart method prefixed with watch*, as follows:

    Public API
        fetchStatus → watchStatus
        fetchOrderBook → watchOrderBook
        fetchOrderBookForSymbols → watchOrderBookForSymbols
        fetchTicker → watchTicker
        fetchTickers → watchTickers
        fetchOHLCV → watchOHLCV
        fetchOHLCVForSymbols → watchOHLCVForSymbols
        fetchTrades → watchTrades
        fetchTradesForSymbols → watchTradesForSymbols
        fetchBidsAsks → watchBidsAsks
        fetchLiquidations → watchLiquidations
        fetchLiquidationsForSymbols → watchLiquidationsForSymbols
    Private API
        fetchBalance → watchBalance
        fetchOrders → watchOrders
        fetchOrdersForSymbols → watchOrdersForSymbols
        fetchMyTrades → watchMyTrades
        fetchPosition → watchPosition
        fetchPositions → watchPositions
        fetchLiquidations → watchLiquidations
        fetchMyLiquidations → watchMyLiquidations
        fetchMyLiquidationsForSymbols → watchMyLiquidationsForSymbols
        fetchFundingRates → watchFundingRates
    REST alternatives
        fetchTrades → fetchTradesWs
        createOrder → createOrderWs
        editOrder → editOrderWs
        cancelOrder → cancelOrderWs
        cancelOrders → cancelOrdersWs
        cancelAllOrders → cancelAllOrdersWs
        etc ...
    unWatch (stops background subscription for watch-ed methods)
        unWatchOrderBook
        unWatchOrderBooksForSymbols
        unwatchTrades
        etc ...

The Unified CCXT Pro Streaming API inherits CCXT usage patterns to make migration easier.

The general async-style flow for a CCXT Pro application (as opposed to a CCXT application above) is shown below:


// a stream-based (WebSocket) orderbook feed loop

while (condition) {

    try {

        // watch some of the public data
        orderbook = await exchange.watchOrderBook (symbol, limit)

        // do something or react somehow based on that data
        // ...

    } catch (e) {

        // handle errors
    }
}

That usage pattern is usually wrapped up into a core business-logic method called "a tick() function", since it reiterates a reaction to the incoming events (aka ticks). From the two examples above it is obvious that the generic usage pattern in CCXT Pro and CCXT is identical.

Many of the CCXT rules and concepts also apply to CCXT Pro:

    CCXT Pro will load markets and will cache markets upon the first call to a unified API method
    CCXT Pro will call CCXT RESTful methods under the hood if necessary
    CCXT Pro will throw standard CCXT exceptions where necessary
    ...

Streaming Specifics

Despite of the numerous commonalities, streaming-based APIs have their own specifics, because of their connection-based nature.

Having a connection-based interface implies connection-handling mechanisms. Connections are managed by CCXT Pro transparently to the user. Each exchange instance manages its own set of connections.

Upon your first call to any watch*() method the library will establish a connection to a specific stream/resource of the exchange and will maintain it. If the connection already exists – it is reused. The library will handle the subscription request/response messaging sequences as well as the authentication/signing if the requested stream is private.

The library will also watch the status of the uplink and will keep the connection alive. Upon a critical exception, a disconnect or a connection timeout/failure, the next iteration of the tick function will call the watch method that will trigger a reconnection. This way the library handles disconnections and reconnections for the user transparently. CCXT Pro applies the necessary rate-limiting and exponential backoff reconnection delays. All of that functionality is enabled by default and can be configured via exchange properties, as usual.

Most of the exchanges only have a single base URL for streaming APIs (usually, WebSocket, starting with ws:// or wss://). Some of them may have more than one URL for each stream, depending on the feed in question.

Exchanges' Streaming APIs can be classified into two different categories:

    sub or subscribe allows receiving only
    pub or publish allows sending and receiving

Sub

A sub interface usually allows to subscribe to a stream of data and listen for it. Most of exchanges that do support WebSockets will offer a sub type of API only. The sub type includes streaming public market data. Sometimes exchanges also allow subcribing to private user data. After the user subscribes to a data feed the channel effectively starts working one-way sending updates from the exchange towards the user continuously.

Commonly appearing types of public data streams:

    order book (most common) - updates on added, edited and deleted orders (aka change deltas)
    ticker updates upon changing of 24 hour stats
    fills feed (also common) - a live stream of public trades
    ohlcv candlestick feed
    heartbeat
    exchange chat/trollbox

Less common types of private user data streams:

    the stream of private trades of the user
    live order updates
    balance updates
    custom streams
    exchange-specific and other streams

Pub

A pub interface usually allows users to send data requests towards the server. This usually includes common user actions, like:

    placing orders
    canceling orders
    placing withdrawal requests
    posting chat/trollbox messages
    etc

Some exchanges do not offer a pub WS API, they will offer sub WS API only. However, there are exchanges that have a complete Streaming API as well. In most cases a user cannot operate effectively having just the Streaming API. Exchanges will stream public market data sub, and the REST API is still needed for the pub part where missing.
unWatch

Each watchX method establishes a subscription with a stream and will continuously get updates from the exchange. Even if you stop getting the return value from the watchX method, the stream will keep sending that, which is handled and stored in the background. To stop those background subscriptions, you should use unWatch method (eg. watchTrades -> unWatchTrades).
Incremental Data Structures

In many cases due to a unidirectional nature of the underlying data feeds, the application listening on the client-side has to keep a local snapshot of the data in memory and merge the updates received from the exchange server into the local snapshot. The updates coming from the exchange are also often called deltas, because in most cases those updates will contain just the changes between two states of the data and will not include the data that has not changed making it necessary to store the locally cached current state S of all relevant data objects.

All of that functionality is handled by CCXT Pro for the user. To work with CCXT Pro, the user does not have to track or manage subscriptions and related data. CCXT Pro will keep a cache of structures in memory to handle the underlying hassle.

Each incoming update says which parts of the data have changed and the receiving side "increments" local state S by merging the update on top of current state S and moves to next local state S'. In terms of CCXT Pro that is called "incremental state" and the structures involved in the process of storing and updating the cached state are called "incremental structures". CCXT Pro introduces several new base classes to handle the incremental state where necessary.

The incremental structures returned from the unified methods of CCXT Pro are often one of two types:

    JSON-decoded object (object in JavaScript, dict in Python, array() in PHP). This type may be returned from public and private methods like watchOrderBook, watchTicker, watchBalance, watchOrder, etc.
    An array/list of objects (usually sorted in chronological order). This type may be returned from methods like watchOHLCV, watchTrades, watchMyTrades, watchOrders, etc.

The unified methods returning arrays like watchOHLCV, watchTrades, watchMyTrades, watchOrders, are based on the caching layer. The user has to understand the inner workings of the caching layer to work with it efficiently.

The cache is a fixed-size deque aka array/list with two ends. The CCXT Pro library has a reasonable limit on the number of objects stored in memory. By default the caching array structures will store up to 1000 entries of each type (1000 most recent trades, 1000 most recent candles, 1000 most recent orders). The allowed maximum number can be configured by the user upon instantiation or later:

ccxtpro.binance({
    'options': {
        'tradesLimit': 1000,
        'OHLCVLimit': 1000,
        'ordersLimit': 1000,
    },
})

# or

exchange.options['tradesLimit'] = 1000
exchange.options['OHLCVLimit'] = 1000
exchange.options['ordersLimit'] = 1000

The cache limits have to be set prior to calling any watch-methods and cannot change during a program run.

When there is space left in the cache, new elements are simply appended to the end of it. If there's not enough room to fit a new element, the oldest element is deleted from the beginning of the cache to free some space. Thus, for example, the cache grows from 0 to 1000 most recent trades and then stays at 1000 most recent trades max, constantly renewing the stored data with each new update incoming from the exchange. It reminds a sliding frame window or a sliding door, that looks like shown below:

      past > ------------------ > time > - - - - - - - - > future


                           sliding frame
                           of 1000 most
                           recent trades
                        +-----------------+
                        |                 |
                        |===========+=====|
+----------------+------|           |     | - - - - - + - - - - - - - - + - - -
|                |      |           |     |           |                 |
0              1000     |         2000    |         3000              4000  ...
|                |      |           |     |           |                 |
+----------------+------|           |     | - - - - - + - - - - - - - - + - - -
                        |===========+=====|
                        |                 |
                        +---+---------+---+
                            |         |
                      since ^         ^ limit

                   date-based pagination arguments
                         are always applied
                       within the cached frame

The user can configure the cache limits using the exchange.options as was shown above. Do not confuse the cache limits with the pagination limit.

Note, that the since and limit date-based pagination params have a different meaning and are always applied within the cached window! If the user specifies a since argument to the watchTrades() call, CCXT Pro will return all cached trades having timestamp >= since. If the user does not specify a since argument, CCXT pro will return cached trades from the beginning of the sliding window. If the user specifies a limit argument, the library will return up to limit candles starting from since or from the beginning of the cache. For that reason the user cannot paginate beyond the cached frame due to the WebSocket real-time specifics.

exchange.options['tradesLimit'] = 5  # set the size of the cache to 5

# this call will return up to 5 cached trades
await exchange.watchTrades (symbol)

# the following call will return the first 2 of up to 5 cached trades
await exchange.watchTrades (symbol, since=None, limit=2)

# this call will first filter cached trades by trade['timestamp'] >= since
# and will return the first 2 of up to 5 cached trades that pass the filter
since = exchange.iso8601('2020-01-01T00:00:00Z')
limit = 2
await exchange.watchTrades (symbol, since, limit)

newUpdates mode

If you want to always get just the most recent trade, you should instantiate the exchange with the newUpdates flag set to true.

exchange = ccxtpro.binance({'newUpdates': True})
while True:
    trades = await exchange.watchTrades (symbol)
    print(trades)

The newUpdates mode continues to utilize the sliding cache in the background, but the user will only be given the new updates. This is because some exchanges use incremental structures, so we need to keep a cache of objects as the exchange may only provide partial information such as status updates.

The result from the newUpdates mode will be one or more updates that have occurred since the last time exchange.watchMethod resolved. CCXT Pro can return one or more orders that were updated since the previous call. The result of calling exchange.watchOrders will look like shown below:

[
    order, // see https://github.com/ccxt/ccxt/wiki/Manual#order-structure
    order,
    order,
    ...
]

Deprecation Warning: in the future newUpdates: true will be the default mode and you will have to set newUpdates to false to get the sliding cache.

import ccxt.pro as ccxtpro
print('CCXT version', ccxtpro.__version__)
print('Supported exchanges:', ccxtpro.exchanges)

The imported CCXT Pro module wraps the CCXT inside itself – every exchange instantiated via CCXT Pro has all the CCXT methods as well as the additional functionality.
Instantiation

CCXT Pro is designed for async/await style syntax and relies heavily on async primitives such as promises and futures.

Creating a CCXT Pro exchange instance is pretty much identical to creating a CCXT exchange instance.

import ccxt.pro as ccxtpro
from asyncio import run

async def main():
    exchange = ccxtpro.kraken({'newUpdates': False})
    while True:
        orderbook = await exchange.watch_order_book('BTC/USD')
        print(orderbook['asks'][0], orderbook['bids'][0])
    await exchange.close()


run(main())

Exchange Properties

Every CCXT Pro instance contains all properties of the underlying CCXT instance. Apart from the standard CCXT properties, the CCXT Pro instance includes the following:

{
    'has': { // an associative array of extended exchange capabilities
        'ws': true, // only available in CCXT Pro
        'watchOrderBook': true,
        'watchTicker': true,
        'watchTickers': true,
        'watchTrades': true,
        'watchMyTrades': true,
        'watchOHLCV': true,
        'watchBalance': true,
        'watchPositions': true,
        'createOrderWs': true,
        'editOrderWs': true,
        'cancelOrderWs': true,
        'cancelOrdersWs': false,
        'cancelAllOrdersWs': true,
        'fetchOrderWs': true,
        'fetchOrdersWs': true,
        'fetchBalanceWs': true,
        'fetchMyTradesWs': true,
        ...
    },
    'urls': {
        'api': { // will contain a streaming API base URL, depending on the underlying protocol
            'ws': 'wss://ws.exchange.com',            // https://en.wikipedia.org/wiki/WebSocket
            'signalr': 'https://signalr.exchange.com' // https://en.wikipedia.org/wiki/SignalR
            'socketio': 'wss://socket.exchange.io'    // https://socket.io
        },
    },
    'version': '1.21',
    'streaming': {
        'keepAlive': 30000, // integer keep-alive rate in milliseconds
        'maxPingPongMisses': 2.0, // how many ping pong misses to drop and reconnect
        ... // other streaming options
    },
    // incremental data structures
    'orderbooks':   {}, // incremental order books indexed by symbol
    'ohlcvs':       {}, // standard CCXT OHLCVs indexed by symbol by timeframe
    'balance':      {}, // a standard CCXT balance structure, accounts indexed by currency code
    'orders':       {}, // standard CCXT order structures indexed by order id
    'trades':       {}, // arrays of CCXT trades indexed by symbol
    'tickers':      {}, // standard CCXT tickers indexed by symbol
    'transactions': {}, // standard CCXT deposits and withdrawals indexed by id or txid
    ...
}

Unified API

The Unified CCXT Pro API encourages direct control flow for better codestyle, more readable and architecturally superior code compared to using EventEmitters and callbacks. The latter is considered an outdated approach nowadays since it requires inversion of control (people aren't used to inverted thinking).

CCXT Pro goes with the modern approach and it is designed for the async syntax. Under the hood, CCXT Pro will still have to use inverted control flow sometimes because of the dependencies and the WebSocket libs that can't do otherwise.

The same is true not only for JS/ES6 but also for Python 3 async code as well. In PHP the async primitives are borrowed from ReactPHP.

Modern async syntax allows you to combine and split the execution into parallel pathways and then merge them, group them, prioritize them, and what not. With promises one can easily convert from direct async-style control flow to inverted callback-style control flow, back and forth.
Message Queue Configuration

The client will return a message each time a message is received and the watch function is being awaited. However it can happen that due to the users code or a possible race condition a message is received and at that moment the watch function is not being awaited and therefore there is no future to resolve. In this case the message is saved in a messageQueue of the websocket client to be returned next time the watch function is called.

To activate this behavior you can switch on the message queue by setting the following options:

exchange.options['ws']['useMessageQueue'] = true

This can be usefull for watch functions with little traffic.
Real-Time vs Throttling

CCXT Pro supports two modes of tick function loops – the real-time mode and the throttling mode. Both of them are shown below in pseudocode:

// real-time mode
const limit = 5 // optional
while (true) {
    try {
        const orderbook = await exchange.watchOrderBook (symbol, limit)
        // your reaction to the update takes place here
        // you arrive here after receiving the update from the exchange in real time
        console.log (orderbook) // every update
    } catch (e) {
        console.log (e)
        // throw e // uncomment to stop the loop on exceptions
    }
}

// throttling mode
const limit = 5 // optional
// await is optional, alternatively you can launch it in bg without await
await exchange.watchOrderBook (symbol, limit)
while (true) {
    // your reaction takes place here
    // you arrive here every 100 ms regardless of whether there was an update or not
    // in throttling mode offloading the orderbook with .limit () is required
    console.log (exchange.orderbooks[symbol].limit (limit))
    await exchange.sleep (100) // every 100 ms
}

In real-time mode CCXT Pro will return the result as soon as each new delta arrives from the exchange. The general logic of a unified call in a real-time loop is to await for the next delta and immediately return the unified result structure to the user, over and over again. This is useful when reaction time is critical, or has to be as fast as possible.

However, the real-time mode requires programming experience with async flows when it comes to synchronizing multiple parallel tick loops. Apart from that, the exchanges can stream a very large number of updates during periods of high activity or high volatility. Therefore the user developing a real-time algorithm has to make sure that the userland code is capable of consuming data that fast. Working in real-time mode may be more demanding for resources sometimes.

In throttling mode CCXT Pro will receive and manage the data in the background. The user is responsible for calling the results from time to time when necessary. The general logic of the throttling loop is to sleep for most of the time and wake up to check the results occasionally. This is usually done at some fixed frequency, or, "frame rate". The code inside a throttling loop is often easier to synchronize across multiple exchanges. The rationing of time spent in a throttled loop also helps reduce resource usage to a minimum. This is handy when your algorithm is heavy and you want to control the execution precisely to avoid running it too often.

The obvious downside of the throttling mode is being less reactive or responsive to updates. When a trading algorithm has to wait some number milliseconds before being executed – an update or two may arrive sooner than that time expires. In throttling mode the user will only check for those updates upon next wakeup (loop iteration), so the reaction lag may vary within some number of milliseconds over time.
Public Methods
watchOrderBook

The watchOrderBook's interface is identical to fetchOrderBook. It accepts three arguments:

    symbol – string, a unified CCXT symbol, required
    limit – integer, the max number of bids/asks returned, optional
    params – assoc dictionary, optional overrides as described in Overriding Unified API Params

In general, the exchanges can be divided in two categories:

    the exchanges that support limited orderbooks (streaming just the top part of the stack of orders)
    the exchanges that stream full orderbooks only

If the exchange accepts a limiting argument, the limit argument is sent towards the exchange upon subscribing to the orderbook stream over a WebSocket connection. The exchange will then send only the specified amount of orders which helps reduce the traffic. Some exchanges may only accept certain values of limit, like 10, 25, 50, 100 and so on.

If the underlying exchange does not accept a limiting argument, the limiting is done on the client side.

The limit argument does not guarantee that the number of bids or asks will always be equal to limit. It designates the upper boundary or the maximum, so at some moment in time there may be less than limit bids or asks, but never more than limit bids or asks. This is the case when the exchange does not have enough orders on the orderbook, or when one of the top orders in the orderbook gets matched and removed from the orderbook, leaving less than limit entries on either bids side or asks side. The free space in the orderbook usually gets quickly filled with new data.

if exchange.has['watchOrderBook']:
    while True:
        try:
            orderbook = await exchange.watch_order_book(symbol, limit, params)
            print(exchange.iso8601(exchange.milliseconds()), symbol, orderbook['asks'][0], orderbook['bids'][0])
        except Exception as e:
            print(e)
            # stop the loop on exception or leave it commented to retry
            # raise e

watchOrderBookForSymbols

Similar to watchOrderBook but accepts an array of symbols so you can subscribe to multiple orderbooks in a single message.

if exchange.has['watchOrderBookForSymbols']:
    while True:
        try:
            orderbook = await exchange.watchOrderBookForSymbols(['BTC/USDT', 'LTC/USDT'], limit, params)
            print(exchange.iso8601(exchange.milliseconds()), symbol, orderbook['asks'][0], orderbook['bids'][0])
        except Exception as e:
            print(e)
            # stop the loop on exception or leave it commented to retry
            # raise e

watchTicker

Some exchanges allow different topics to listen to tickers (ie: bookTicker). You can set this in exchange.options['watchTicker']['name']

// JavaScript
if (exchange.has['watchTicker']) {
    while (true) {
        try {
            const ticker = await exchange.watchTicker (symbol, params)
            console.log (new Date (), ticker)
        } catch (e) {
            console.log (e)
            // stop the loop on exception or leave it commented to retry
            // throw e
        }
    }
}

# Python
if exchange.has['watchTicker']:
    while True:
        try:
            ticker = await exchange.watch_ticker(symbol, params)
            print(exchange.iso8601(exchange.milliseconds()), ticker)
        except Exception as e:
            print(e)
            # stop the loop on exception or leave it commented to retry
            # raise e

watchTickers

if exchange.has['watchTickers']:
    while True:
        try:
            tickers = await exchange.watch_tickers(symbols, params)
            print(exchange.iso8601(exchange.milliseconds()), tickers)
        except Exception as e:
            print(e)
            # stop the loop on exception or leave it commented to retry
            # raise e

watchOHLCV

A very common misconception about WebSockets is that WS OHLCV streams can somehow speed up a trading strategy. If the purpose of your app is to implement OHLCV-trading or a speculative algorithmic strategy, consider the following carefully.

In general, there's two types of trading data used in the algorithms:

    1st-order real-time data like orderbooks and trades
    2nd-order non-real-time data like tickers, ohlcvs, etc

When developers say "real-time", that usually means pseudo real-time, or, put simply, "as fast and as close to real time as possible".

The 2nd-order data is always calculated from the 1st-order data. OHLCVs are calculated from aggregated trades. Tickers are calculated from trades and orderbooks.

Some exchanges do the calculation of OHLCVs (2nd order data) for you on the exchange side and send you updates over WS (Binance). Other exchanges don't really think that is necessary, for a reason.

Obviously, it takes time to calculate 2nd-order OHLCV candles from trades. Apart from that sending the calculated candle back to all connected users also takes time. Additional delays can happen during periods of high volatility if an exchange is traded very actively under high load.

There is no strict guarantee on how much time it will take from the exchange to calculate the 2nd order data and stream it to you over WS. The delays and lags on OHLCV candles can vary significantly from exchange to exchange. For example, an exchange can send an OHLCV update ~30 seconds after the actual closing of a corresponding period. Other exchanges may send the current OHLCV updates at a regular intervals (say, once every 100ms), while in reality trades can happen much more frequently.

Most people use WS to avoid any sorts of delays and have real-time data. So, in most cases it is much better to not wait for the exchange. Recalculating the 2nd order data from 1st order data on your own may be much faster and that can lower the unnecessary delays. Therefore it does not make much sense to use WS for watching just the OHLCV candles from the exchange. Developers would rather watch_trades() instead and recalculate the OHLCV candles using CCXT's built-in methods like build_ohlcvc().

# Python
exchange = ccxtpro.binance()
if not exchange.has['watchOHLCV']:
    while True:
        try:
            trades = await exchange.watch_trades(symbol)
            ohlcvc = exchange.build_ohlcvc(trades, '1m')
            print(ohlcvc)
        except Exception as e:
            print(e)
            # stop the loop on exception or leave it commented to retry
            # raise e

That explains why some exchanges reasonably think that OHLCVs are not necessary in the WS context, cause users can calculate that information in the userland much faster having just a WS stream of realtime 1st-order trades.

If your application is not very time-critical, you can still subscribe to OHLCV streams, for charting purposes. If the underlying exchange.has['watchOHLCV'], you can watchOHLCV()/watch_ohlcv() as shown below:

if exchange.has['watchOHLCV']:
    while True:
        try:
            candles = await exchange.watch_ohlcv(symbol, timeframe, since, limit, params)
            print(exchange.iso8601(exchange.milliseconds()), candles)
        except Exception as e:
            print(e)
            # stop the loop on exception or leave it commented to retry
            # raise e

watchOHLCVForSymbols

Similar to watchOHLCV but allows multiple subscriptions of symbols and timeframes

if exchange.has['watchOHLCVForSymbols']:
    while True:
        try:
            subscriptions = [[
                ['BTC/USDT', '1d'],
                ['LTC/USDT', '5m'],
                ['ETH/USDT', '1h']
            ]]
            candles = await exchange.watch_ohlcv_for_symbols(subscriptions, since, limit, params)
            print(exchange.iso8601(exchange.milliseconds()), candles)
        except Exception as e:
            print(e)
            # stop the loop on exception or leave it commented to retry
            # raise e

watchTrades

if exchange.has['watchTrades']:
    while True:
        try:
            trades = await exchange.watch_trades(symbol, since, limit, params)
            print(exchange.iso8601(exchange.milliseconds()), trades)
        except Exception as e:
            print(e)
            # stop the loop on exception or leave it commented to retry
            # raise e

watchTradesForSymbols

Similar to watchTrades but allows subscribing to multiple symbols in a single call.

if exchange.has['watchTradesForSymbols']:
    while True:
        try:
            trades = await exchange.watchTradesForSymbols(['LTC/USDT', 'BTC/USDT'], since, limit, params)
            print(exchange.iso8601(exchange.milliseconds()), trades)
        except Exception as e:
            print(e)
            # stop the loop on exception or leave it commented to retry
            # raise e

Private Methods

In most cases the authentication logic is borrowed from CCXT since the exchanges use the same keypairs and signing algorithms for REST APIs and WebSocket APIs. See API Keys Setup for more details.
watchBalance

if exchange.has['watchBalance']:
    while True:
        try:
            balance = await exchange.watch_balance(params)
            print(exchange.iso8601(exchange.milliseconds()), balance)
        except Exception as e:
            print(e)
            # stop the loop on exception or leave it commented to retry
            # raise e

watchOrders

watch_orders(symbol=None, since=None, limit=None, params={})

watchMyTrades

watch_my_trades(symbol=None, since=None, limit=None, params={})

watchPositions

watch all open positions and returns a list of position structure

watch_positions(symbols=None, since=None, limit=None, params={})

createOrderWs

create_order_ws(self, symbol: str, type: OrderType, side: OrderSide, amount: float, price: Optional[float] = None, params={})

editOrderWs

edit_order_ws(self, id, symbol: str, type: OrderType, side: OrderSide, amount: float, price: Optional[float] = None, params={})

cancelOrderWs

cancel_order_ws(self, id, symbol: str, params={})

cancelOrdersWs

cancel_orders_ws(self, ids, symbol: str, params={})

cancelAllOrdersWs

cancel_all_orders_ws(self, symbol: str, params={})

watchTransactions

- this method is a work in progress now (may be unavailable)

Custom handler

If you want to have an access to raw incoming messages and use your custom handlers, you can override exchange's handleMessage/handle_message method, like:

A) By inheritance:


class my_exchange(ccxt.pro.coinbase):
    def handle_message(self, client, message):
        print("Raw incoming message:", message)  # this is the raw update
        super().handle_message(client, message)
        # your extra logic here

async def example():
    ex = my_exchange()
    await ex.watch_ticker('BTC/USDT')

asyncio.run(example())

B) by overriding the method:


def myHandler(instance, ws, data, original_handle_message):
    original_handle_message(ws, data)  # trigger original `handleMessage`
    if your_condition:
        # execute your additional code

async def example():
    e = ccxt.pro.binance()
    original_handle_message = e.handle_message
    e.handle_message = lambda ws, data: myHandler(e, ws, data, original_handle_message)
    await e.watch_ticker('BTC/USDT')

asyncio.run(example())

Error Handling

In case of an error the CCXT Pro will throw a standard CCXT exception, see Error Handling for more details.