import numpy as np

#class VanillaOption(object):
#    """An abstract interface for plain vanilla options."""
#
#    def __init__(self, strike, expiry):
#        self.strike = strike
#        self.expiry = expiry
#
#    def payoff(self, spot):
#       pass
#
#class VanillaCallOption(VanillaOption):
#    """A concrete class for vanilla call options."""
#    def payoff(self, spot):
#        return np.maximum(spot - self.strike, 0.0)
#
#class VanillaPutOption(VanillaOption):
#    """A concrete class for vanilla put options."""
#    def payoff(self, spot):
#
#        return np.maximum(self.strike - spot, 0.0)

K = 41 #strike
T = 1 #year
S = 40 #spot
vol = 0.3 #volatility SIGMA
r = 0.08 #rate
div = 0.00 #divided yield DELTA
N = 10
M = 10,000 #simulations


def AsianArithmeticOption():
    
    v = r -div - 0.5 * vol * vol
    a = np.log(G[t]) + ((N - M) / N) (np.log(S) + v (t[M + 1] - t) + 0.5 (v) * (T -t[M + 1]))
    b = (((N - M)**2) / N * N) * vol * vol * (t[M + 1] - t) + (((vol * vol) * (T - t[M + 1]) / (6 * (N * N))) * (N - M) * (2 * (N - M) - 1))
    x = ((a - np.log(K) + b) / np.sqrt(b))
       
    price = np.exp(-r * T)(np.exp(a + (0.5 *b)) * N * x - K * N(x - np.sqrt(b)))
    
    asian_price = price
    
    return asian_price