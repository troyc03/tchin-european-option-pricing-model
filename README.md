# European Option Pricing with Monte Carlo and Crank–Nicolson

A numerical pricing project for **European call options** under the Black–Scholes model. The repository compares three equivalent pricing approaches:

1. **Monte Carlo simulation** under risk-neutral geometric Brownian motion  
2. **Black–Scholes closed-form pricing**  
3. **Crank–Nicolson finite-difference solution** of the Black–Scholes PDE  

The goal is to show how stochastic simulation, analytical pricing, and numerical PDE methods converge to the same no-arbitrage option value.

---

## Table of Contents

- [Overview](#overview)
- [Project Objectives](#project-objectives)
- [Financial Background](#financial-background)
- [Mathematical Formulation](#mathematical-formulation)
- [Monte Carlo Method](#monte-carlo-method)
- [Black–Scholes Formula](#blackscholes-formula)
- [Crank–Nicolson PDE Method](#cranknicolson-pde-method)
- [Validation](#validation)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Model Parameters](#model-parameters)
- [Numerical Considerations](#numerical-considerations)
- [Variance Reduction](#variance-reduction)
- [Testing](#testing)
- [Limitations](#limitations)
- [Possible Extensions](#possible-extensions)
- [References](#references)
- [Disclaimer](#disclaimer)

---

## Overview

This project prices a European call option under the standard Black–Scholes assumptions.

For a call option with strike price \(K\) and maturity \(T\), the payoff at expiration is

\[
C_T = \max(S_T - K, 0).
\]

The pricing workflow is:

1. Model the underlying asset with risk-neutral geometric Brownian motion.
2. Simulate terminal prices using Monte Carlo.
3. Estimate the discounted expected payoff.
4. Compute the Black–Scholes analytical benchmark.
5. Solve the Black–Scholes PDE numerically using Crank–Nicolson.
6. Compare the results and analyze numerical error.

The Monte Carlo estimator is

\[
\hat{C}_N
=
e^{-rT}
\frac{1}{N}
\sum_{i=1}^{N}
\max\left(S_T^{(i)} - K, 0\right).
\]

---

## Project Objectives

- Implement Monte Carlo pricing for a European call option.
- Implement the Black–Scholes closed-form solution.
- Solve the Black–Scholes PDE using a Crank–Nicolson finite-difference scheme.
- Validate the Monte Carlo and PDE results against the analytical price.
- Measure Monte Carlo statistical uncertainty with standard errors and confidence intervals.
- Demonstrate convergence as the number of simulation paths and PDE grid resolution increase.
- Provide a foundation for more advanced derivative-pricing projects.

---

## Financial Background

### European Call Option

A European call option gives its holder the right, but not the obligation, to buy an underlying asset at strike price \(K\) on the expiration date \(T\).

Its payoff is

\[
C_T = (S_T - K)^+,
\]

where

\[
x^+ = \max(x, 0).
\]

The option is:

- **In the money** when \(S_T > K\)
- **At the money** when \(S_T = K\)
- **Out of the money** when \(S_T < K\)

### Risk-Neutral Valuation

Under the risk-neutral measure \( \mathbb{Q} \), the present value of a derivative with payoff \(\Phi(S_T)\) is

\[
V_0
=
e^{-rT}
\mathbb{E}^{\mathbb{Q}}
\left[
\Phi(S_T)
\right].
\]

For a European call option,

\[
C_0
=
e^{-rT}
\mathbb{E}^{\mathbb{Q}}
\left[
(S_T-K)^+
\right].
\]

---

## Mathematical Formulation

### Risk-Neutral Geometric Brownian Motion

Under the Black–Scholes model, the asset price follows

\[
dS_t
=
rS_t\,dt
+
\sigma S_t\,dW_t^{\mathbb{Q}},
\]

where:

| Symbol | Description |
|:---:|---|
| \(S_t\) | Asset price at time \(t\) |
| \(r\) | Continuously compounded risk-free rate |
| \(\sigma\) | Annualized volatility |
| \(W_t^{\mathbb{Q}}\) | Brownian motion under the risk-neutral measure |

The exact terminal-price distribution is

\[
S_T
=
S_0
\exp\left[
\left(r - \frac{1}{2}\sigma^2\right)T
+
\sigma\sqrt{T}Z
\right],
\]

where

\[
Z \sim \mathcal{N}(0,1).
\]

Because this expression is exact, there is no need to discretize the SDE with Euler–Maruyama when pricing a vanilla European option from terminal values alone.

---

## Monte Carlo Method

### Estimator

Generate \(N\) independent standard-normal samples:

\[
Z_1, Z_2, \ldots, Z_N
\sim
\mathcal{N}(0,1).
\]

For each sample, simulate

\[
S_T^{(i)}
=
S_0
\exp\left[
\left(r-\frac{1}{2}\sigma^2\right)T
+
\sigma\sqrt{T}Z_i
\right].
\]

Then calculate the payoff

\[
P_i
=
\max(S_T^{(i)} - K, 0).
\]

The Monte Carlo price estimate is

\[
\hat{C}_N
=
e^{-rT}
\frac{1}{N}
\sum_{i=1}^{N}
P_i.
\]

### Standard Error and Confidence Interval

Define discounted payoffs as

\[
X_i
=
e^{-rT}
\max(S_T^{(i)}-K, 0).
\]

The sample standard deviation is

\[
s_X
=
\sqrt{
\frac{1}{N-1}
\sum_{i=1}^{N}
\left(X_i-\hat{C}_N\right)^2
}.
\]

The estimated standard error is

\[
\widehat{\operatorname{SE}}
=
\frac{s_X}{\sqrt{N}}.
\]

For sufficiently large \(N\), an approximate 95% confidence interval is

\[
\hat{C}_N
\pm
1.96\widehat{\operatorname{SE}}.
\]

Monte Carlo convergence follows

\[
\widehat{\operatorname{SE}}
=
O\left(N^{-1/2}\right).
\]

This means reducing error by a factor of 10 typically requires approximately 100 times more simulated paths.

---

## Black–Scholes Formula

For a non-dividend-paying asset, the Black–Scholes price of a European call is

\[
C_{\mathrm{BS}}
=
S_0N(d_1)
-
Ke^{-rT}N(d_2),
\]

where \(N(\cdot)\) is the standard normal cumulative distribution function.

\[
d_1
=
\frac{
\ln(S_0/K)
+
\left(r+\frac{1}{2}\sigma^2\right)T
}{
\sigma\sqrt{T}
},
\]

\[
d_2
=
d_1-\sigma\sqrt{T}.
\]

The closed-form result serves as the primary benchmark for validating both numerical methods.

---

## Crank–Nicolson PDE Method

The Black–Scholes PDE for a European call is

\[
\frac{\partial C}{\partial t}
+
\frac{1}{2}\sigma^2S^2
\frac{\partial^2 C}{\partial S^2}
+
rS
\frac{\partial C}{\partial S}
-
rC
=
0.
\]

The terminal condition is

\[
C(S,T)
=
\max(S-K,0).
\]

Boundary conditions are

\[
C(0,t)=0,
\]

and, for sufficiently large \(S_{\max}\),

\[
C(S_{\max},t)
\approx
S_{\max}
-
Ke^{-r(T-t)}.
\]

### Crank–Nicolson Scheme

The Crank–Nicolson method averages the explicit and implicit finite-difference approximations. It is commonly used because it is more accurate than first-order Euler schemes and is generally stable for the Black–Scholes PDE.

The computational domain is discretized as

\[
S \in [0, S_{\max}],
\qquad
t \in [0,T].
\]

The solver proceeds backward from maturity:

\[
C(S,T)
=
\max(S-K,0)
\]

to the initial time:

\[
C(S_0,0).
\]

As the spatial and temporal grids are refined, the Crank–Nicolson price should converge toward the Black–Scholes closed-form value.

---

## Validation

The three approaches solve the same pricing problem:

\[
\text{Risk-Neutral SDE}
\longleftrightarrow
\text{Monte Carlo Expectation}
\longleftrightarrow
\text{Black–Scholes PDE}.
\]

This connection is formalized by the Feynman–Kac theorem.

A typical experiment compares:

| Method | Expected behavior |
|---|---|
| Monte Carlo | Fluctuates around the analytical price within statistical uncertainty |
| Black–Scholes formula | Deterministic analytical benchmark |
| Crank–Nicolson PDE | Converges toward the analytical price as the grid is refined |

Example convergence table:

| Simulations | Monte Carlo Price | Standard Error | 95% Confidence Interval | Black–Scholes Price | Absolute Error |
|---:|---:|---:|---:|---:|---:|
| 1,000 | ... | ... | ... | ... | ... |
| 10,000 | ... | ... | ... | ... | ... |
| 100,000 | ... | ... | ... | ... | ... |
| 1,000,000 | ... | ... | ... | ... | ... |

Example PDE convergence table:

| Spatial Steps | Time Steps | PDE Price | Black–Scholes Price | Absolute Error |
|---:|---:|---:|---:|---:|
| 50 | 50 | ... | ... | ... |
| 100 | 100 | ... | ... | ... |
| 200 | 200 | ... | ... | ... |
| 400 | 400 | ... | ... | ... |

---

## Project Structure

```text
european-option-pricing/
│
├── README.md
├── requirements.txt
├── pyproject.toml
│
├── src/
│   ├── __init__.py
│   ├── black_scholes.py
│   ├── monte_carlo.py
│   └── parameter_estimation.py
│
├── tests/
│   ├── test_black_scholes.py
│   ├── test_monte_carlo.py
│   └── test_crank_nicolson.py
│
├── notebooks/
│   └── option_pricing_experiments.ipynb
│
├── results/
│   ├── monte_carlo_convergence.png
│   ├── pde_grid_convergence.png
│   └── method_comparison.png
│
└── LICENSE
```

| Module | Responsibility |
|---|---|
| `black_scholes.py` | Analytical and Numerical Black–Scholes pricing and Greeks |
| `monte_carlo.py` | Risk-neutral terminal-price simulation and confidence intervals |
| `utils.py` | Shared validation, plotting, and parameter utilities |
| `tests/` | Automated unit and numerical-validation tests |
| `notebooks/` | Reproducible experiments and visualizations |

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd european-option-pricing
```

Create and activate a virtual environment.

**Linux/macOS**

```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

If the repository uses `pyproject.toml`, install it in editable mode:

```bash
pip install -e .
```

---

## Usage

Run a Monte Carlo pricing experiment:

```bash
python -m src.monte_carlo
```

Run the analytical Black–Scholes benchmark:

```bash
python -m src.black_scholes
```

Launch the notebook environment:

```bash
jupyter notebook
```

Then open:

```text
notebooks/eda.ipynb
```

---

## Model Parameters

| Parameter | Symbol | Description |
|---|:---:|---|
| Initial asset price | \(S_0\) | Current underlying asset price |
| Strike price | \(K\) | Option exercise price |
| Maturity | \(T\) | Time to expiration in years |
| Risk-free rate | \(r\) | Continuously compounded annual rate |
| Volatility | \(\sigma\) | Annualized asset volatility |
| Simulations | \(N\) | Number of Monte Carlo paths |
| Spatial steps | \(M\) | Number of PDE asset-price grid intervals |
| Time steps | \(L\) | Number of PDE time intervals |
| Maximum asset price | \(S_{\max}\) | Upper boundary of the PDE domain |

Example configuration:

```python
S0 = 100.0
K = 100.0
T = 1.0
r = 0.05
sigma = 0.20

n_simulations = 1_000_000

s_max = 400.0
n_space_steps = 200
n_time_steps = 200
```

For these parameters, the Black–Scholes European-call benchmark is approximately:

```text
10.4506
```

---

## Numerical Considerations

### Exact GBM Simulation

For European options under Black–Scholes assumptions, simulate terminal prices directly:

\[
S_T
=
S_0
\exp\left[
\left(r-\frac{1}{2}\sigma^2\right)T
+
\sigma\sqrt{T}Z
\right].
\]

Avoid Euler–Maruyama unless the project requires full price paths, such as for Asian, barrier, or American-style options.

### Reproducibility

Use a fixed random seed for testing and repeatable experiments:

```python
rng = np.random.default_rng(42)
```

### Vectorization

Use NumPy array operations rather than Python loops for large simulations:

```python
z = rng.standard_normal(n_simulations)

terminal_prices = S0 * np.exp(
    (r - 0.5 * sigma**2) * T
    + sigma * np.sqrt(T) * z
)

payoffs = np.maximum(terminal_prices - K, 0.0)
price = np.exp(-r * T) * np.mean(payoffs)
```

### PDE Boundary Selection

Choose \(S_{\max}\) sufficiently above both \(S_0\) and \(K\). A poor upper boundary can dominate PDE error even when the numerical grid is fine.

A practical initial choice is often

\[
S_{\max}
\geq
3K
\]

or a larger value when volatility or maturity is high.

---

## Variance Reduction

The baseline Monte Carlo implementation uses independent samples. The following techniques can reduce variance and improve computational efficiency.

### Antithetic Variates

For each draw \(Z_i\), also evaluate \(-Z_i\). Average both discounted payoffs to reduce estimator variance.

### Control Variates

Under the risk-neutral measure,

\[
\mathbb{E}^{\mathbb{Q}}
\left[
e^{-rT}S_T
\right]
=
S_0.
\]

This known expectation makes the discounted terminal asset price a useful control variate.

### Quasi-Monte Carlo

Low-discrepancy sequences, such as Sobol sequences, may improve numerical integration efficiency relative to pseudorandom sampling.

### Importance Sampling

Importance sampling is particularly useful for rare-event payoffs, such as deep out-of-the-money options or credit-risk-style models.

---

## Testing

Recommended tests include:

- Verify the analytical Black–Scholes price against known benchmark values.
- Verify that Monte Carlo estimates fall within a selected number of standard errors of the Black–Scholes value.
- Verify that the Crank–Nicolson PDE solution approaches the analytical price as the grid is refined.
- Test in-the-money, at-the-money, and out-of-the-money calls.
- Test short maturities and high-volatility cases.
- Check no-arbitrage bounds:

\[
\max\left(S_0-Ke^{-rT},0\right)
\leq
C_0
\leq
S_0.
\]

- Verify call-price monotonicity:
  - Price increases as \(S_0\) increases.
  - Price increases as \(\sigma\) increases.
  - Price decreases as \(K\) increases.

Run the test suite with:

```bash
pytest
```

---

## Limitations

This project intentionally uses the standard Black–Scholes framework, which assumes:

- Constant volatility.
- Constant deterministic interest rates.
- Lognormal asset-price dynamics.
- Frictionless markets.
- Continuous trading and hedging.
- No jumps or heavy tails.
- No transaction costs, taxes, liquidity effects, or bid–ask spreads.
- No dividends in the base implementation.

These assumptions are useful for understanding pricing theory, but they do not fully describe real financial markets.

---

## Possible Extensions

- Add European put options and validate with put–call parity.
- Add a continuous dividend yield \(q\).
- Implement Greeks using analytical formulas, finite differences, and pathwise Monte Carlo estimators.
- Add antithetic and control-variate Monte Carlo estimators.
- Price path-dependent Asian and barrier options.
- Implement American options with Longstaff–Schwartz least-squares Monte Carlo.
- Extend the model to Heston stochastic volatility.
- Add Merton jump-diffusion dynamics.
- Add implied-volatility calibration.
- Parallelize Monte Carlo simulations with Numba, multiprocessing, or GPU tools.
- Compare finite-difference schemes: explicit Euler, implicit Euler, and Crank–Nicolson.

---

## References

1. Black, F., and Scholes, M. (1973). *The Pricing of Options and Corporate Liabilities*. Journal of Political Economy.
2. Merton, R. C. (1973). *Theory of Rational Option Pricing*. Bell Journal of Economics and Management Science.
3. Glasserman, P. *Monte Carlo Methods in Financial Engineering*.
4. Hull, J. C. *Options, Futures, and Other Derivatives*.
5. Shreve, S. E. *Stochastic Calculus for Finance II: Continuous-Time Models*.
6. Wilmott, P. *Paul Wilmott on Quantitative Finance*.

---

## Disclaimer

This repository is an educational numerical-finance project.

It is not investment advice, a trading strategy, market forecasting software, or a production-grade pricing and risk-management system.
