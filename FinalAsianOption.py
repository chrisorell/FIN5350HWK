import numpy as np
from scipy.stats import norm

def ArithmeticAsianCallPayoff(path, strike):
    spot_t = path.mean()
    return np.maximum(spot_t - strike, 0.0)

def NaiveAsianPrice(S, K, r, v, q, T, M, N):
    dt = T / N
    nudt = (r - q - 0.5 * v * v) * dt
    sigdt = v * np. sqrt(dt)
    
    path = np.empty(N)
    
    Ct1 = np.zeros(M)
    
    #For each simulation
    for i in range (M):
        path[0] = S
        z = np.random.normal(size = N)       
        #for each time step
        for t in range (1, N):
            path[t] = path[t -1] * np.exp(nudt + sigdt * z[t])
            
        Ct1[i] += ArithmeticAsianCallPayoff(path, K)

    price = Ct1.mean()
    price *= np.exp(-r * T)
    
    std_err = Ct1.std() / np.sqrt(M)
    return (price, std_err)

def BlackScholesCall(S, K, r, v, q, tau):
    d1 = (np.log(S/K) + (r - q + 0.5 * v * v) * tau) / (v * np.sqrt(tau))
    d2 = d1 - v * np.sqrt(tau)
    callPrc = (S * np.exp(-q * tau) * norm.cdf(d1)) - (K * np.exp(-r * tau) * norm.cdf(d2))
    return callPrc

def BlackScholesDelta(S, K, r, v, q, tau):
    d1 = (np.log(S/K) + (r - q + 0.5 * v * v) * tau) / (v * np.sqrt(tau))
    delta = np.exp(-q * tau) * norm.cdf(d1)
    return delta

def GeometricAsianCall(S, K, r, v, q, tau, N):
    dt = tau / N
    nu = r - q - 0.5 * v * v
    a = N * (N + 1) * (2.0 * N * 1.0) / 6.0
    V = np.exp(-r * tau) * S * np.exp(((N + 1.0) * nu / 2.0 + v * v * a / (2.0 * N * N)) * dt)
    vavg = v * np.sqrt(a) / (N**(1.5))
    return BlackScholesCall(V, K, r, vavg, 0, tau)

def ControlVariatePricing():
    g_star = geoprc
    a_bar = arithprc
    g_bar = bsprc
    ControlVariatePrice = a_bar + (g_bar - g_star)
    return ControlVariatePrice

S = 100.0
K = 100.0
r = 0.06
v = 0.2
q = 0.03
T = 1.
M = 10000
N = 10

geoprc = GeometricAsianCall(S, K, r, v, q, T, N)
arithprc, arithstderr = NaiveAsianPrice(S, K, r, v, q, T, M, N)
delta = BlackScholesDelta(S, K, r, v, q, T)
bsprc = BlackScholesCall(S, K, r, v, q, T)
cvprc = ControlVariatePricing()


print ("The Geometric Asian price is {0:.4f}".format(geoprc))
print ("The Arithmetic Asian price is {0:.4f}".format(arithprc))
print ("The Black-Scholes price is {0:.4f}".format(bsprc))
print ("The Control Variate Price is {0:.4f}".format(cvprc))
print ("The Standard Error is {0:.4f}".format(arithstderr))
print ("The Delta is {0:.4f}".format(delta))
