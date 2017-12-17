import numpy as np
from scipy.stats import binom

class VanillaOption(object):
    def __init__(self, strike, expiry):
        self.strike = strike
        self.expiry = expiry
    def payoff(self, spot):
       pass

class VanillaCallOption(VanillaOption):
    def payoff(self, spot):
        return np.maximum(spot - self.strike, 0.0)

class VanillaPutOption(VanillaOption):
    def payoff(self, spot):
        return np.maximum(self.strike - spot, 0.0)

def EuropeanBinomialPricer(option, S, rate, vol, div, num_steps):
    #dividend = beta, volatility = sd
    num_nodes = num_steps + 1
    spotT = 0.0
    callT = 0.0
    H = option.expiry / num_steps
    up = np.exp(((rate - div) * H) + vol * (np.sqrt(H)))
    down = np.exp(((rate - div) * H) - vol * (np.sqrt(H)))
    prob_up = (np.exp(rate * H) - down) / (up - down)
    prob_down = 1 - prob_up

    for i in range(num_nodes):
        spotT = S * (up ** (num_steps - i)) * (down ** (i))
        callT += option.payoff(spotT) * binom.pmf(num_steps - i, num_steps, prob_up)

    price = callT * np.exp(-rate * time)

    return price

def AmericanBinomialPricer(option, S, rate, vol, div, num_steps):

    num_nodes = num_steps + 1
    H = option.expiry / num_steps
    up = np.exp(((rate - div) * H) + vol * np.sqrt(H))
    down = np.exp(((rate - div) * H) - vol * np.sqrt(H))
    prob_up = (np.exp(rate * H) - down) / (up - down)
    prob_down = 1 - prob_up
    disc = np.exp(-rate * H)
    dpu = disc * prob_up
    dpd = disc * prob_down

    Ct = np.zeros(num_nodes)
    St = np.zeros(num_nodes)

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

S = 41 #
K = 40 #
rate = 0.08 #Rate
vol = 0.30 #Volatility
div = 0.0 #Dividend
num_steps = 3
time = 1.0 #Time

CallOption = VanillaCallOption(K, time)
PutOption = VanillaPutOption(K, time)
Call_Price_A = AmericanBinomialPricer(CallOption, S, rate, vol, div, num_steps)
Put_Price_A = AmericanBinomialPricer(PutOption, S, rate, vol, div, num_steps)
Call_Price_E = EuropeanBinomialPricer(CallOption, S, rate, vol, div, num_steps)
Put_Price_E = EuropeanBinomialPricer(PutOption, S, rate, vol, div, num_steps)
print("The 2 period American Call Option Price is = {0:.4f}".format(Call_Price_A))
print("The 2 period American Put Option Price is = {0:.4f}".format(Put_Price_A))
print("The 2 period European Put Option Price is = {0:.4f}".format(Put_Price_E))
print("The 2 period European Call Option Price is = {0:.4f}".format(Call_Price_E))
