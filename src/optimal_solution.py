from .extract_data import eta, gamma , daily_volatility
import numpy as np 
from scipy.optimize import fsolve
import datetime as dt

def K(s_0,lamda,T,N,ticker,start,w=30):

    '''
    returns the expression of K involved in the optimal solution
    '''
    tau = T/N
    start_minus_w = (dt.datetime.fromisoformat(start) - dt.timedelta(days=w)).isoformat()[:10]

    sigma = daily_volatility(s_0,ticker,start_minus_w,start)
    mu_tilde = eta(ticker,start_minus_w,start) - 0.5*gamma(ticker,start_minus_w,start)*tau

    k_bar =  lamda*(sigma**2)/mu_tilde
    f = lambda x: (2/tau**2)*(np.cosh(x*tau) - 1 ) - k_bar
    return fsolve(f,[1])[0]





def optimal_solutions(s_0,X,lamda,T,N,ticker,start):
    """
    Returns the optimal amount of stocks to sell for every interval
    """
    
    tau = int(T/N)
    assert tau >= 1 
    time_list = np.array([j*tau for j in range(N+1)])
    #range_list = np.array([i for i in range(N+1)])
    k = K(s_0,lamda,T,N,ticker,start)
    f1 = lambda x:  (np.sinh(k*(T-x))/np.sinh(k*T))*X
    #f2 = lambda x:  (2*np.sinh(k*tho/2)/np.sinh(k*T))*np.cosh(k*(T-x*tho + tho/2))*X

    optimal_residues = f1(time_list)
    #optimal_quantities_to_sell = f2(range_list)
    
    
    return -np.diff(optimal_residues) 

