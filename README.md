# Optimal European Option Pricing Model using Monte Carlo and Crank–Nicolson Methods

This project prices a European call option under the Black–Scholes model using:

- Monte Carlo simulation
- Black–Scholes closed-form pricing
- Crank–Nicolson finite-difference PDE pricing

The numerical methods are validated against the analytical Black–Scholes price.

## Model

Under the risk-neutral measure, the asset price follows geometric Brownian motion:

$$
dS_t = rS_tdt + \sigma S_tdW_t.
$$

The exact terminal asset price is

$$
S_T = S_0 \exp\left[ \left( r - \frac{1}{2}\sigma^2 \right) T + \sigma\sqrt{T}Z \right], \quad Z \sim \mathcal{N}(0,1)
$$

For a European call option, the payoff is

$$
C_T = \max(S_T-K, 0).
$$ 

## Monte Carlo Pricing

The Monte Carlo estimator is

$$
\hat{C}_N =
e^{-rT}
\frac{1}{N}
\sum_{i=1}^{N}
\max(S_T^{(i)}-K, 0).
$$

Monte Carlo error decreases at approximately

$$
O(N^{-1/2}).
$$

## Black–Scholes Benchmark

The analytical price of a European call is

$$
C = S_0N(d_1)-Ke^{-rT}N(d_2),
$$

where

$$
d_1 =
\frac{
\ln(S_0/K)
+
\left(r+\frac{1}{2}\sigma^2\right)T
}{
\sigma\sqrt{T}
},
$$

$$
d_2 = d_1 - \sigma\sqrt{T}.
$$

## PDE Method

The Black–Scholes PDE is

$$
\frac{\partial C}{\partial t} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 C}{\partial S^2} + rS \frac{\partial C}{\partial S} - rC = 0.
$$

The terminal condition is

$$
C(S,T) = \max(S-K,0).
$$

A Crank–Nicolson finite-difference scheme solves this PDE backward from maturity to obtain the option price at \(t=0\).

## Example Parameters

```python
S0 = 100.0
K = 100.0
T = 1.0
r = 0.05
sigma = 0.20
n_simulations = 1000
```

For these parameters, the Black–Scholes European call price is approximately:

```text
10.4506
```

## Future Work

- Implement Quasi-Monte Carlo methods to improve convergence of MC simulation
- Plot log-log curve of convergence between Crank-Nicolson/MC simulations
- Test all three models on real-market data
