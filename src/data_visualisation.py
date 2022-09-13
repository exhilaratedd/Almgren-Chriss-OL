import yfinance as yf
from .optimal_solution import optimal_solutions
from .client import Client

def loss_for_client(client: Client,N):
    """
    calculating the difference between the expectation of the client
    which is X*s_0 and what we really managed to gather with our strategy
    """
    start = client.start
    end = client.end
    ticker = client.ticker
    lamda = client.lamda
    X = client.X

    stock = yf.Ticker(ticker)
    column = 'Open'

    s_0 =  stock.history(start = start, end = end)[column][0]

    T = client.real_difference_time(start,end)
    

    optimal_sells = optimal_solutions(s_0,X,lamda,T,N,ticker,start)

    # averaging the price of the stock over each interval of selling

    tau = int(T/N)
    hist = stock.history(start = start, end = end )[column]

    d = hist.rolling(window  =  tau).mean().reset_index().dropna().iloc[::tau,:]
    d = d.reset_index()[column]

    # d = {}
    # for k in range(N):
    #     d[k] = hist.iloc[k*tau:(k+1)*tau].mean()

    pnl = sum([d[k]*optimal_sells[k] for k in range(N)])

    return optimal_sells, ((X*s_0 - pnl)/(X*s_0))*100






