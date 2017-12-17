import numpy as np
cimport numpy as np
from scipy.stats import norm

cdef ArithmeticAsianCallPayoff(path, strike):
    spot_t = path.mean()
    return np.maximum(spot_t - strike, 0.0)

cdef NaiveAsianPrice(S, K, r, v, q, T, M, N):
    cdef double dt = T / N
    cdef double nudt = (r - q - 0.5 * v * v) * dt
    cdef double sigdt = v * np. sqrt(dt)
    
    cdef double path = np.empty(N)
    
    cdef double Ct1 = 0.0
    
    #For each simulation
    for i in range (M):
        path[0] = S
        z = np.random.normal(size = N)       
        #for each time step
        for t in range (1, N):
            path[t] = path[t -1] * np.exp(nudt + sigdt * z[t])
            
        Ct1[i] += ArithmeticAsianCallPayoff(path, K)

    Ct1 /= M
    Ct1 *= np.exp(-r * T)
    
    #StandardDeviation(Ct1)
    return (Ct1)

cdef StandardDeviation(Ct1, M):
    cdef double the_array = np.std(Ct1)/np.sqrt(M)
    return the_array

cdef BlackScholesCall(S, K, r, v, q, tau):
    cdef double d1 = (np.log(S/K) + (r - q + 0.5 * v * v) * tau) / (v * np.sqrt(tau))
    cdef double d2 = d1 - v * np.sqrt(tau)
    cdef double callPrc = (S * np.exp(-q * tau) * norm.cdf(d1)) - (K * np.exp(-r * tau) * norm.cdf(d2))
    return callPrc

cdef BlackScholesDelta(S, K, r, v, q, tau):
    cdef double d1 = (np.log(S/K) + (r - q + 0.5 * v * v) * tau) / (v * np.sqrt(tau))
    cdef double delta = np.exp(-q * tau) * norm.cdf(d1)
    return delta

cdef GeometricAsianCall(S, K, r, v, q, tau, N):
    cdef double dt = tau / N
    cdef double nu = r - q - 0.5 * v * v
    cdef double a = N * (N + 1) * (2.0 * N * 1.0) / 6.0
    cdef double V = np.exp(-r * tau) * S * np.exp(((N + 1.0) * nu / 2.0 + v * v * a / (2.0 * N * N)) * dt)
    cdef double vavg = v * np.sqrt(a) / (N**(1.5))
    return BlackScholesCall(V, K, r, vavg, 0, tau)

cdef ControlVariatePricing():
    cdef double g_star = geoprc
    cdef double a_bar = arithprc
    cdef double g_bar = bsprc
    cdef double ControlVariatePrice = a_bar + (g_bar - g_star)
    return ControlVariatePrice

cdef double S = 100.0
cdef double K = 100.0
cdef double r = 0.06
cdef double v = 0.2
cdef double q = 0.03
cdef double T = 1.0
cdef double M = 100
cdef double N = 10
cdef double the_array = 0
cdef double Ct1 = 0

cdef double thenumber = StandardDeviation(Ct1, M)
cdef double geoprc = GeometricAsianCall(S, K, r, v, q, T, N)
cdef double arithprc = NaiveAsianPrice(S, K, r, v, q, T, M, N)
cdef double delta = BlackScholesDelta(S, K, r, v, q, T)
cdef double bsprc = BlackScholesCall(S, K, r, v, q, T)
cdef double cvprc = ControlVariatePricing()

print("The Standard Deviation is", thenumber)
print ("The geometric price is {0:.4f}".format(geoprc))
print ("The arithmetic price is {0:.4f}".format(arithprc))
print ("The Control Variate Price is {0:.4f}".format(cvprc))
print ("The BlackScholes price is {0:.4f}".format(bsprc))
print ("The delta is {0:.4f}".format(delta))