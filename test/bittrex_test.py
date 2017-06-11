import pytest
from cryptotik import Bittrex
from decimal import Decimal

private = pytest.mark.skipif(
    not pytest.config.getoption("--apikey"),
    reason="needs --apikey option to run."
)


def test_format_pair():
    '''test string formating to match API expectations'''

    assert Bittrex.format_pair("btc_ppc") == "btc-ppc"


def test_get_markets():
    '''test get_markets'''

    assert isinstance(Bittrex.get_markets(), list)
    assert "btc-ltc" in Bittrex.get_markets()


def test_get_market_ticker():
    '''test get_market_ticker'''

    ticker = Bittrex.get_market_ticker("btc-ltc")

    assert isinstance(ticker, dict)
    assert list(ticker.keys()) == ['Bid', 'Ask', 'Last']


@pytest.mark.parametrize("depth", [10, 20, 50])
def test_get_market_orders(depth):
    '''test get_market_orderbook'''

    market_orders = Bittrex.get_market_orders("btc-ppc", depth)

    assert isinstance(market_orders, dict)
    assert isinstance(market_orders["buy"], list)
    assert isinstance(market_orders["sell"], list)


def test_get_market_trade_history():
    '''test get_market_trade_history'''

    trade_history = Bittrex.get_market_trade_history("btc-ppc", 10)

    assert isinstance(trade_history, list)
    assert len(trade_history) == 10
    assert list(trade_history[0].keys()) == ['Id', 'TimeStamp', 'Quantity',
                                             'Price', 'Total', 'FillType',
                                             'OrderType']


def test_get_market_depth():
    '''test get_market_depth'''

    market_depth = Bittrex.get_market_depth("btc-ppc")

    assert isinstance(market_depth, dict)
    assert isinstance(market_depth["asks"], Decimal)


def test_get_market_spread():
    '''test get_market spread'''

    assert isinstance(Bittrex.get_market_spread("btc-vtc"), Decimal)


@private
def test_get_balance(apikey, secret):
    '''test get_balances'''

    btrx = Bittrex(apikey, secret)
    balances = btrx.get_balances()

    assert isinstance(balances, list)
    assert list(balances[0].keys()) == ['Currency', 'Balance', 'Available',
                                        'Pending', 'CryptoAddress']


@private
def test_get_open_orders(apikey, secret):
    '''test get_balances'''

    btrx = Bittrex(apikey, secret)
    orders = btrx.get_open_orders()

    if orders:
        assert isinstance(orders, list)
        assert list(orders[0].keys()) == ['Uuid', 'OrderUuid',
                                          'Exchange', 'OrderType',
                                          'Quantity', 'QuantityRemaining',
                                          'Limit', 'CommissionPaid', 'Price',
                                          'PricePerUnit', 'Opened', 'Closed',
                                          'CancelInitiated', 'ImmediateOrCancel',
                                          'IsConditional', 'Condition',
                                          'ConditionTarget']


@private
@pytest.mark.xfail
def test_get_deposit_address(apikey, secret):
    '''test get_deposit_address'''

    btrx = Bittrex(apikey, secret)

    assert isinstance(btrx.get_deposit_address("btc"), str)


@private
def test_buy(apikey, secret):
    '''test buy'''

    btrx = Bittrex(apikey, secret)
    buy = btrx.buy("btc_ppc", 0.0000001, 0.0001)

    assert buy == {'message': 'DUST_TRADE_DISALLOWED_MIN_VALUE_50K_SAT',
                   'result': None,
                   'success': False
                   }


@private
def test_sell(apikey, secret):
    '''test buy'''

    btrx = Bittrex(apikey, secret)
    sell = btrx.sell("btc_ppc", 0.0000001, 0.0001)

    assert sell == {'message': 'DUST_TRADE_DISALLOWED_MIN_VALUE_50K_SAT',
                    'result': None,
                    'success': False
                    }

