# Reproduce results from fig2
# of raanes'2014 "extending sqrt method to model noise"

# Lessons:
# - Multidim. multiplicative noise incorporation has a tendency to go
#   awry.
# - This happens coz of some strange very strong, regular correlation
# patters that arise when dt=1 (dt = c*dx).
# - It also happens if X0pat does not use centering.

from common import *

m = 1000;
p = 40;

obsInds = equi_spaced_integers(m,p)

# Burn-in allows damp*x and x+noise balance out
tseq = Chronology(dt=1,dkObs=5,T=500,BurnIn=60)

@atmost_2d
def hmod(E,t):
  return E[:,obsInds]

h = {
    'm': p,
    'model': hmod,
    'noise': GaussRV(C=0.01*eye(p))
    }


wnum  = 25
X0 = RV(sampling_func = lambda N: \
    sqrt(5)/10 * sinusoidal_sample(m,wnum,N))



# sinusoidal_sample() can be replicated by a
# covariance matrix approach.
# However, for strict equivalence one would have to use
# uniform random numbers to multiply with
# the covariance (cholesky factor).
# This approach has a prescribed covariance matrix,
# and so it can be treated in the ensemble in interesting ways,
# (ie. not just additive sampling).
# But, for efficiency, only a m-by-rank cholesky factor
# should be specified.
wnumQ     = 25
NQ        = 2*wnumQ+1
A         = sinusoidal_sample(m,wnumQ,NQ)
A         = 1/10 * anom(A)[0] / sqrt(NQ)
Q         = A.T @ A
Q         = GaussRV(C = 5*Q)

#TODO:
# **Instead of** the above, generate huge (N) sample,
# compute its cov, so that:
load average_sinusoidal_cov.datafile
Q = GaussRV(C = X0pat_cov)
## F.noise.chol = tsqrt(A*A',2*wnumQ)


damp = 0.98;
Fm = Fmat(m,-1,1,tseq.dt)
def step(x,t,dt):
  assert dt == tseq.dt
  return x @ Fm.T

f = {
    'm': m,
    'model': damp * step,
    'noise': Q
    }




