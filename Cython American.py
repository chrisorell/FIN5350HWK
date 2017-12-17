import numpy as np
cimport numpy as np
from scipy.stats import binom

cdef class VanillaOption(object):
    def __init__(self, strike, expiry):
        self.strike = strike
        self.expiry = expiry
    def payoff(self, spot):
       pass

cdef class VanillaCallOption(VanillaOption):
    def payoff(self, spot):
        return np.maximum(spot - self.strike, 0.0)

cdef class VanillaPutOption(VanillaOption):
    def payoff(self, spot):
        return np.maximum(self.strike - spot, 0.0)
    
cdef AmericanBinomialPricer(option, S, rate, vol, div, num_steps):

    cdef double H = option.expiry / num_steps
    cdef double up = np.exp(((rate - div) * H) + vol * np.sqrt(H))
    cdef double down = np.exp(((rate - div) * H) - vol * np.sqrt(H))
    cdef double prob_up = (np.exp(rate * H) - down) / (up - down)
    cdef double prob_down = 1 - prob_up
    cdef double disc = np.exp(-rate * H)
    cdef double dpu = disc * prob_up
    cdef double dpd = disc * prob_down
    cdef double Ct = np.zeros(num_nodes)
    cdef double St = np.zeros(num_nodes)
    cdef double [::1] St = np.empty(num_nodes, dtype = np.float64)
    cdef double [::1] Ct = np.empty(num_nodes, dtype = np.float64)
    cdef unsigned long num_nodes = num_steps + 1
    cdef unsigned long i
    cdef unsigned long j

    for i in range(num_nodes):
        St[i] = S * (up **(num_steps - i)) * (down ** i)
        Ct[i] = option.payoff(St[i])

    for i in range((num_steps - 1), -1, -1):
        for j in range(i+1):
            Ct[j] = dpu * Ct[j] + dpd * Ct[j+1]
            St[j] = St[j] / up
            Ct[j] = np.maximum(Ct[j], option.payoff(St[j]))

    Ct[0]
    return Ct[0]

cdef double S = 41 #
cdef double K = 40 #
cdef double rate = 0.08 #Rate
cdef double vol = 0.30 #Volatility
cdef double div = 0.0 #Dividend
cdef double num_steps = 3
cdef double time = 1.0 #Time

cdef double CallOption
cdef double PutOption

CallOption = VanillaCallOption(K, time)
PutOption = VanillaPutOption(K, time)
Call_Price_A = AmericanBinomialPricer(CallOption, S, rate, vol, div, num_steps)
Put_Price_A = AmericanBinomialPricer(PutOption, S, rate, vol, div, num_steps)

print("The 2 period American Call Option Price is = {0:.4f}".format(Call_Price_A))
print("The 2 period American Put Option Price is = {0:.4f}".format(Put_Price_A))