import numpy as np
import datetime as dt

class Client:

    def __init__(self,ticker,start,end,X,lamda):

        '''
        Class defined by the type of client:
        ticker: the stock to be sold
        T: the window of selling
        X: the quantity to be sold during the window
        lamda: the aversion of risk
        '''
        self.ticker = ticker
        self.start = start
        self.end = end
        self.X = X
        self.lamda = lamda


    def real_difference_time(self,start,end):
        '''
        returns the real difference of days between the start and end (without weekends)
        '''
        if type(start) == str:
            d1 = dt.date(*[int(x) for x in start.split('-')])
            d2 = dt.date(*[int(x) for x in end.split('-')])
        else:
            d1 = start
            d2 = end

        T = np.busday_count( d1, d2 )
        # to take into account  the holidays we are going to remove int(T*8/260)
        # because for a year: T = 260 and the real value should be 252 because of holidays.
        # so this is a good and simple approximation of the real number of working days taking into account holidays.
        return T - int(T*8/260)

