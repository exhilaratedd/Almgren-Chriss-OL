import numpy as np
import yfinance as yf


def expected_annual_return(ticker,start,end):
    """
    function that returns the expected annual return of a stock
    using the formula (1 + Return) ^ (1 / N) - 1 where N is the number of periods measured
    """
    stock = yf.Ticker(ticker)
    hist = stock.history(start = start, end = end)
    open_price = hist['Open']
    N = int(end[:4]) - int(start[:4]) + 1
    ending_price = open_price[-1]
    beggining_price = open_price[0]
    overall_return = (ending_price-beggining_price)/beggining_price
    return (1+overall_return)**(1/N) - 1

def daily_expected_return(s_0,ticker,start,end):
    """
    returns the expected fractional return scaled by the initial price
    """
    return (expected_annual_return(ticker,start,end)/252)*s_0

def daily_volatility(s_0,ticker,start,end):
    '''
    returns daily volatility of a stock scaled by the initial price
    '''
    column = 'Open'
    stock = yf.Ticker(ticker)
    hist = stock.history(start = start, end = end)
    open_price = hist[column]
    data = open_price[:-1].reset_index()
    new_data = open_price[1:].reset_index()
    data[column] = new_data[column]/data[column] - 1 # obtaining returns
    return np.sqrt(data[column].var())*s_0

def bid_ask_spread(ticker):

    stock = yf.Ticker(ticker)
    ask = stock.info['ask']
    bid = stock.info['bid']
    assert ask >= bid
    return np.abs(ask-bid)

def median_daily_trading_volume(ticker,start,end):
    
    stock = yf.Ticker(ticker)
    hist = stock.history(start = start, end = end )
    return np.median(hist['Volume'])


def eta(ticker,start,end):
    """
    returns an estimation of mu involved in the temporary impact
    """
    spread = bid_ask_spread(ticker)
    impact_of_market = 0.01
    median_volume = median_daily_trading_volume(ticker,start,end)
    return spread/(impact_of_market*median_volume)


def gamma(ticker,start,end):
    """
    returns an estimation of gamma involved in the permanent impact
    """

    spread = bid_ask_spread(ticker)
    median_volume = median_daily_trading_volume(ticker,start,end)
    return spread/(0.1*median_volume)















