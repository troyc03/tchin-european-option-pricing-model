# Optimal European Option Pricing Model Using Monte Carlo and Crank-Nicolson Methods

A basic Monte Carlo framework for pricing **European call options**, with numerical results validated against both the **Black–Scholes closed-form solution** and the **Black–Scholes partial differential equation (PDE)**.

The project demonstrates how stochastic simulation can be used to estimate derivative prices and how the resulting Monte Carlo estimator relates to the classical analytical and PDE formulations of the Black–Scholes model.

---

## Table of Contents

* [Overview](#overview)
* [Project Objectives](#project-objectives)
* [Financial Background](#financial-background)

  * [European Call Option](#european-call-option)
  * [Underlying Asset Model](#underlying-asset-model)
  * [Risk-Neutral Valuation](#risk-neutral-valuation)
* [Mathematical Formulation](#mathematical-formulation)

  * [Geometric Brownian Motion](#geometric-brownian-motion)
  * [Monte Carlo Pricing](#monte-carlo-pricing)
  * [Black–Scholes Closed-Form Solution](#blackscholes-closed-form-solution)
  * [Black–Scholes PDE](#blackscholes-pde)
* [Monte Carlo Algorithm](#monte-carlo-algorithm)
* [Validation Methodology](#validation-methodology)
* [Convergence and Statistical Error](#convergence-and-statistical-error)
* [Project Structure](#project-structure)
* [Installation](#installation)
* [Usage](#usage)
* [Model Parameters](#model-parameters)
* [Example](#example)
* [Interpreting the Results](#interpreting-the-results)
* [Numerical Considerations](#numerical-considerations)
* [Variance Reduction](#variance-reduction)
* [Limitations](#limitations)
* [Possible Extensions](#possible-extensions)
* [Testing](#testing)
* [References](#references)
* [Disclaimer](#disclaimer)

---

# Overview

This project implements a **Monte Carlo option pricing model** for a European call option under the standard assumptions of the Black–Scholes framework.

The basic workflow is:

1. Model the underlying asset using geometric Brownian motion.
2. Simulate a large number of possible terminal asset prices.
3. Evaluate the European call payoff for each simulated price.
4. Discount the average payoff back to the present.
5. Compare the Monte Carlo estimate against:

   * the analytical Black–Scholes formula, and
   * a numerical solution of the Black–Scholes PDE.

For a European call option with strike price $K$ and maturity $T$, the payoff at maturity is

$$
C_T = \max(S_T-K,0),
$$

where $S_T$ is the underlying asset price at maturity.

The Monte Carlo estimator is

$$
\hat{C}_N
=========

e^{-rT}
\frac{1}{N}
\sum_{i=1}^{N}
\max\left(S_T^{(i)}-K,0\right),
$$

where:

* $S_0$ is the current underlying asset price,
* $K$ is the strike price,
* $T$ is the time to maturity,
* $r$ is the continuously compounded risk-free rate,
* $\sigma$ is the volatility,
* $N$ is the number of Monte Carlo simulations.

The Black–Scholes closed-form solution provides a deterministic benchmark against which the stochastic Monte Carlo estimate can be validated.

---

# Project Objectives

The main objectives of this project are:

### 1. Implement Monte Carlo option pricing

Generate risk-neutral samples of the underlying asset price and use those samples to estimate the discounted expected payoff.

### 2. Demonstrate Monte Carlo convergence

Show that increasing the number of simulations causes the Monte Carlo estimator to converge toward the theoretical option price.

### 3. Validate the implementation against Black–Scholes

Use the analytical Black–Scholes formula as a benchmark for the Monte Carlo estimator.

### 4. Connect probabilistic and PDE formulations

Demonstrate that the Monte Carlo, analytical, and PDE approaches produce consistent option prices.

### 5. Provide a foundation for further development

The implementation can serve as a starting point for more advanced computational-finance techniques, including:

* variance reduction,
* path-dependent options,
* stochastic volatility,
* finite-difference PDE methods,
* quasi-Monte Carlo,
* American option pricing,
* multi-asset derivatives.

---

# Financial Background

## European Call Option

A European call option gives its holder the right, but not the obligation, to purchase an underlying asset for a fixed strike price $K$ at maturity $T$.

Its payoff is

$$
C_T = \max(S_T-K,0).
$$

There are two possible cases.

### In the Money

If

$$
S_T > K,
$$

the option has positive value:

$$
C_T = S_T-K.
$$

### Out of the Money

If

$$
S_T \leq K,
$$

the option expires worthless:

$$
C_T = 0.
$$

Therefore, the payoff can be written compactly as

$$
C_T = (S_T-K)^+,
$$

where

$$
x^+ = \max(x,0).
$$

---

# Underlying Asset Model

The standard Black–Scholes model assumes that the underlying asset follows a **geometric Brownian motion**.

Under the physical probability measure, the asset follows

$$
dS_t = \mu S_t,dt + \sigma S_t,dW_t,
$$

where:

* $S_t$ is the underlying asset price,
* $\mu$ is the expected return,
* $\sigma$ is the volatility,
* $W_t$ is a standard Brownian motion.

For derivative pricing, however, the relevant dynamics are expressed under the **risk-neutral measure**:

$$
dS_t = rS_t,dt + \sigma S_t,dW_t^Q.
$$

The physical drift $\mu$ is replaced by the risk-free rate $r$ because arbitrage-free derivative pricing is performed under the risk-neutral measure.

---

# Risk-Neutral Valuation

Under the risk-neutral measure, the price of a derivative paying $\Phi(S_T)$ at maturity is

$$
V_0
===

e^{-rT}
\mathbb{E}^Q
\left[
\Phi(S_T)
\right].
$$

For a European call,

$$
\Phi(S_T)
=========

\max(S_T-K,0),
$$

so

$$
C_0
===

e^{-rT}
\mathbb{E}^Q
\left[
\max(S_T-K,0)
\right].
$$

This expectation is the fundamental quantity estimated by the Monte Carlo implementation.

---

# Mathematical Formulation

## Geometric Brownian Motion

Under the risk-neutral measure, the underlying asset satisfies

$$
dS_t
====

rS_t,dt
+
\sigma S_t,dW_t^Q.
$$

The exact solution is

$$
S_T
===

S_0
\exp
\left[
\left(
r-\frac{1}{2}\sigma^2
\right)T
+
\sigma W_T^Q
\right].
$$

Since

$$
W_T^Q \sim \mathcal{N}(0,T),
$$

we can write

$$
W_T^Q = \sqrt{T}Z,
\qquad
Z\sim\mathcal{N}(0,1).
$$

Therefore,

$$
\boxed{
S_T
===

S_0
\exp
\left[
\left(
r-\frac{1}{2}\sigma^2
\right)T
+
\sigma\sqrt{T}Z
\right]
}
$$

This closed-form expression for $S_T$ is particularly useful for Monte Carlo pricing because it allows the terminal asset price to be sampled directly without discretizing the stochastic differential equation.

---

# Monte Carlo Pricing

The risk-neutral value of a European call is

$$
C_0
===

e^{-rT}
\mathbb{E}^Q
\left[
(S_T-K)^+
\right].
$$

Monte Carlo simulation approximates this expectation using a finite number of independent samples.

Generate

$$
Z_1,Z_2,\ldots,Z_N
\sim
\mathcal{N}(0,1).
$$

For each sample, calculate

$$
S_T^{(i)}
=========

S_0
\exp
\left[
\left(
r-\frac{1}{2}\sigma^2
\right)T
+
\sigma\sqrt{T}Z_i
\right].
$$

The corresponding option payoff is

$$
P_i
===

\max
\left(
S_T^{(i)}-K,
0
\right).
$$

The Monte Carlo estimator is then

$$
\boxed{
\hat{C}_N
=========

e^{-rT}
\frac{1}{N}
\sum_{i=1}^{N}
P_i
}
$$

or equivalently,

$$
\boxed{
\hat{C}_N
=========

e^{-rT}
\frac{1}{N}
\sum_{i=1}^{N}
\max
\left(
S_T^{(i)}-K,
0
\right)
}
$$

As $N\rightarrow\infty$, the law of large numbers gives

$$
\hat{C}_N
\rightarrow
C_0.
$$

---

# Black–Scholes Closed-Form Solution

For a European call option on a non-dividend-paying underlying, the Black–Scholes price is

$$
\boxed{
C_0
===

## S_0N(d_1)

Ke^{-rT}N(d_2)
}
$$

where $N(\cdot)$ is the cumulative distribution function of the standard normal distribution.

The quantities $d_1$ and $d_2$ are defined as

$$
\boxed{
d_1
===

\frac{
\ln\left(\frac{S_0}{K}\right)
+
\left(
r+\frac{1}{2}\sigma^2
\right)T
}{
\sigma\sqrt{T}
}
}
$$

and

$$
\boxed{
d_2
===

d_1-\sigma\sqrt{T}
}
$$

The Black–Scholes price provides the analytical reference value used to validate the Monte Carlo implementation.

---

# Black–Scholes PDE

The same option-pricing problem can also be formulated as a deterministic partial differential equation.

Let

$$
C=C(S,t)
$$

denote the value of the European call when the underlying price is $S$ at time $t$.

The Black–Scholes PDE is

$$
\boxed{
\frac{\partial C}{\partial t}
+
\frac{1}{2}\sigma^2S^2
\frac{\partial^2 C}{\partial S^2}
+
rS\frac{\partial C}{\partial S}
-------------------------------

# rC

0
}
$$

with terminal condition

$$
\boxed{
C(S,T)
======

\max(S-K,0)
}
$$

For a European call, appropriate boundary conditions include

$$
C(0,t)=0
$$

and, as $S\rightarrow\infty$,

$$
C(S,t)
\sim
S-Ke^{-r(T-t)}.
$$

A numerical PDE solver discretizes the asset-price and time dimensions and solves the equation backward from the terminal payoff.

---

# Monte Carlo, Black–Scholes, and the PDE

The three approaches used in this project represent different formulations of the same pricing problem.

### Monte Carlo

The Monte Carlo approach evaluates

$$
C_0
===

e^{-rT}
\mathbb{E}^Q
\left[
(S_T-K)^+
\right]
$$

numerically using random samples.

### Black–Scholes Formula

The closed-form formula evaluates the same expectation analytically:

$$
C_0
===

## S_0N(d_1)

Ke^{-rT}N(d_2).
$$

### Black–Scholes PDE

The PDE solves

$$
\frac{\partial C}{\partial t}
+
\frac{1}{2}\sigma^2S^2
\frac{\partial^2 C}{\partial S^2}
+
rS\frac{\partial C}{\partial S}
-------------------------------

# rC

0.

$$

These formulations are connected through the **Feynman–Kac theorem**.

Conceptually,

$$
\boxed{
\text{Geometric Brownian Motion}
\longleftrightarrow
\text{Risk-Neutral Expectation}
\longleftrightarrow
\text{Black--Scholes PDE}
}
$$

The project numerically demonstrates this equivalence.

---

# Monte Carlo Algorithm

The complete pricing procedure is:

### Step 1 — Define Model Parameters

Specify

$$
S_0,\quad K,\quad T,\quad r,\quad \sigma,\quad N.
$$

### Step 2 — Generate Standard Normal Samples

Generate

$$
Z_i\sim\mathcal{N}(0,1),
\qquad
i=1,\ldots,N.
$$

### Step 3 — Simulate Terminal Asset Prices

For every sample,

$$
S_T^{(i)}
=========

S_0
\exp
\left[
\left(
r-\frac{1}{2}\sigma^2
\right)T
+
\sigma\sqrt{T}Z_i
\right].
$$

### Step 4 — Calculate Payoffs

Calculate

$$
P_i
===

\max
\left(
S_T^{(i)}-K,
0
\right).
$$

### Step 5 — Calculate the Mean Payoff

Compute

$$
\bar{P}
=======

\frac{1}{N}
\sum_{i=1}^{N}
P_i.
$$

### Step 6 — Discount to the Present

The Monte Carlo option price is

$$
\hat{C}_N
=========

e^{-rT}\bar{P}.
$$

### Step 7 — Compare Against Black–Scholes

Calculate

$$
\epsilon
========

\hat{C}*N-C*{\mathrm{BS}}.
$$

The absolute pricing error is

$$
|\epsilon|
==========

\left|
\hat{C}*N-C*{\mathrm{BS}}
\right|.
$$

---

# Validation Methodology

The project validates the Monte Carlo implementation using two independent references:

1. The analytical Black–Scholes formula.
2. A numerical solution of the Black–Scholes PDE.

A useful validation experiment is to increase the number of Monte Carlo simulations:

$$
N
=

10^2,;
10^3,;
10^4,;
10^5,;
10^6.
$$

For each value of $N$, calculate the Monte Carlo price and compare it with the Black–Scholes benchmark.

A convergence plot can then show:

$$
\text{Monte Carlo Price}
\quad\text{vs.}\quad
\text{Number of Simulations}.
$$

The analytical Black–Scholes price can be plotted as a horizontal reference line.

---

# Convergence and Statistical Error

Monte Carlo methods converge relatively slowly.

If the discounted payoff has finite variance, then the standard error of the estimator behaves approximately as

$$
\operatorname{SE}(\hat{C}_N)
============================

\frac{\sigma_P}{\sqrt{N}},
$$

where $\sigma_P$ is the standard deviation of the discounted payoff.

Therefore,

$$
\boxed{
\text{Monte Carlo error}
========================

O\left(N^{-1/2}\right)
}
$$

This is one of the most important characteristics of Monte Carlo methods.

To reduce the statistical error by a factor of $10$, approximately $100$ times as many simulations are required.

For example:

| Simulations | Approximate error scale |
| ----------: | ----------------------: |
|      $10^2$ |               $10^{-1}$ |
|      $10^4$ |               $10^{-2}$ |
|      $10^6$ |               $10^{-3}$ |
|      $10^8$ |               $10^{-4}$ |

These values describe the asymptotic scaling behavior and should not be interpreted as guaranteed absolute errors.

---

# Monte Carlo Confidence Interval

Define the discounted payoff for simulation $i$ as

$$
X_i
===

e^{-rT}
\max
\left(
S_T^{(i)}-K,
0
\right).
$$

The Monte Carlo estimate is

$$
\hat{C}_N
=========

\frac{1}{N}
\sum_{i=1}^{N}
X_i.
$$

The sample variance is

$$
s_X^2
=====

\frac{1}{N-1}
\sum_{i=1}^{N}
\left(
X_i-\hat{C}_N
\right)^2.
$$

The estimated standard error is

$$
\boxed{
\widehat{\operatorname{SE}}
===========================

\frac{s_X}{\sqrt{N}}
}
$$

For sufficiently large $N$, an approximate 95% confidence interval is

$$
\boxed{
\hat{C}_N
\pm
1.96
\frac{s_X}{\sqrt{N}}
}
$$

This is an important part of Monte Carlo validation.

A Monte Carlo estimate that differs from the analytical Black–Scholes price is not necessarily incorrect. The difference should be interpreted relative to the estimator's statistical uncertainty.

---

# Project Structure

A typical repository structure might look like:

```text
tchin-european-option-pricing-model/
│
├── README.md
├── requirements.txt
│
├── src/
│   ├── monte_carlo.py
│   ├── black_scholes.py
│   └── pde.py
│
├── tests/
│   ├── test_monte_carlo.py
│   ├── test_black_scholes.py
│   └── test_pde.py
│
├── notebooks/
│   └── option_pricing.ipynb
│
├── results/
│   ├── convergence.png
│   └── comparison.png
│
└── LICENSE
```

The exact structure depends on the implementation in the repository.

A reasonable separation of responsibilities is:

| Component          | Responsibility                          |
| ------------------ | --------------------------------------- |
| `monte_carlo.py`   | Monte Carlo simulation and pricing      |
| `black_scholes.py` | Analytical Black–Scholes pricing        |
| `pde.py`           | Numerical PDE solution                  |
| `tests/`           | Automated numerical tests               |
| `notebooks/`       | Experiments and visualizations          |
| `results/`         | Generated figures and numerical results |

---

# Installation

Clone the repository:

```bash
git clone <repository-url>
cd tchin-european-option-pricing-model
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Linux/macOS:

```bash
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

If the project is packaged as an installable Python module, it can also be installed in editable mode:

```bash
pip install -e .
```

---

# Usage

The exact execution command depends on the implementation.

A typical command-line workflow might be:

```bash
python src/monte_carlo.py
```

or:

```bash
python -m src.monte_carlo
```

For notebook-based experiments:

```bash
jupyter notebook
```

Then open the relevant notebook under `notebooks/`.

---

# Model Parameters

The model is controlled by the following parameters:

| Parameter           |  Symbol  | Description                            |
| ------------------- | :------: | -------------------------------------- |
| Initial asset price |   $S_0$  | Current underlying price               |
| Strike price        |    $K$   | Exercise price                         |
| Maturity            |    $T$   | Time to expiration                     |
| Risk-free rate      |    $r$   | Continuously compounded risk-free rate |
| Volatility          | $\sigma$ | Annualized volatility                  |
| Simulations         |    $N$   | Number of Monte Carlo simulations      |

An illustrative configuration is:

```text
S0     = 100
K      = 100
T      = 1
r      = 0.05
sigma  = 0.20
N      = 1000000
```

These values represent an at-the-money European call with one year to maturity.

They are illustrative model parameters and are not market forecasts.

---

# Example

Consider a European call with

$$
S_0=100,
\qquad
K=100,
\qquad
T=1,
$$

$$
r=0.05,
\qquad
\sigma=0.20.
$$

Generate

$$
Z_i\sim\mathcal{N}(0,1).
$$

For each sample, calculate

$$
S_T^{(i)}
=========

100
\exp
\left[
\left(
0.05-\frac{1}{2}(0.20)^2
\right)
+
0.20Z_i
\right].
$$

The payoff is

$$
P_i
===

\max
\left(
S_T^{(i)}-100,
0
\right).
$$

The Monte Carlo estimate is

$$
\hat{C}_N
=========

e^{-0.05}
\frac{1}{N}
\sum_{i=1}^{N}
P_i.
$$

The corresponding Black–Scholes benchmark is

$$
C_{\mathrm{BS}}
===============

## 100N(d_1)

100e^{-0.05}N(d_2),
$$

where

$$
d_1
===

\frac{
\ln(100/100)
+
\left(
0.05+\frac{1}{2}(0.20)^2
\right)
}{
0.20
}
$$

and

$$
d_2
===

d_1-0.20.
$$

The Monte Carlo estimate should fluctuate around the Black–Scholes value, with the magnitude of the fluctuations decreasing as $N$ increases.

---

# Interpreting the Results

A useful validation table is:

| Number of simulations | Monte Carlo price | Black–Scholes price | Absolute error |
| --------------------: | ----------------: | ------------------: | -------------: |
|               $1,000$ |               ... |                 ... |            ... |
|              $10,000$ |               ... |                 ... |            ... |
|             $100,000$ |               ... |                 ... |            ... |
|           $1,000,000$ |               ... |                 ... |            ... |

A correct implementation should demonstrate that:

1. The Monte Carlo estimate approaches the Black–Scholes value.
2. The statistical error decreases approximately as $N^{-1/2}$.
3. Different random seeds produce slightly different estimates.
4. Those differences are consistent with the estimated standard error.
5. The PDE solution converges toward the same price as the numerical grid is refined.

---

# Random Seeds and Reproducibility

Monte Carlo simulations depend on pseudorandom number generation.

For reproducible experiments, a random seed should be explicitly specified.

For example:

```python
rng = np.random.default_rng(42)
```

A fixed seed is useful for:

* debugging;
* automated testing;
* reproducible demonstrations;
* regression tests.

For statistical experiments, it can also be useful to run the simulation under multiple independent seeds and examine the resulting distribution of the estimator.

---

# Numerical Considerations

## Exact Simulation of Geometric Brownian Motion

For a European option under the standard Black–Scholes assumptions, the terminal asset price can be sampled exactly:

$$
S_T
===

S_0
\exp
\left[
\left(
r-\frac{1}{2}\sigma^2
\right)T
+
\sigma\sqrt{T}Z
\right].
$$

There is therefore no need to use an Euler–Maruyama discretization when only the terminal asset price is required.

This is advantageous because numerical time discretization would introduce an additional source of error.

---

## Vectorization

Monte Carlo simulation is highly amenable to vectorized computation.

Conceptually:

```text
Z
│
├── Z₁
├── Z₂
├── ...
└── Zₙ
     │
     ▼
Terminal asset prices
     │
     ▼
Option payoffs
     │
     ▼
Mean payoff
     │
     ▼
Discounted option price
```

A numerical library such as NumPy can process the entire simulation array without requiring an explicit Python-level loop over every path.

This becomes important when $N$ is large.

---

## Floating-Point Considerations

Extreme parameter values can cause numerical issues.

Potential problems include:

* very large exponential arguments;
* extremely small maturities;
* extremely large volatility;
* very deep in-the-money options;
* very deep out-of-the-money options;
* extreme values of $S_0/K$.

For ordinary financial parameter ranges, double-precision floating-point arithmetic is generally sufficient.

---

# Variance Reduction

The basic Monte Carlo implementation uses independent random samples.

For larger pricing problems, variance-reduction techniques can substantially improve efficiency.

## Antithetic Variates

For every sample

$$
Z_i,
$$

also use

$$
-Z_i.
$$

The two samples have the same marginal distribution but can reduce the variance of the estimator when used appropriately.

---

## Control Variates

A control variate uses a random quantity whose expectation is known analytically.

Under the risk-neutral measure,

$$
\mathbb{E}^Q[S_T]
=================

S_0e^{rT}.
$$

Therefore,

$$
\mathbb{E}^Q[e^{-rT}S_T]
========================

S_0.
$$

This known expectation can be used to construct a control-variate estimator.

---

## Importance Sampling

For rare-event problems, standard Monte Carlo can be inefficient because most simulations may contribute little to the payoff.

Importance sampling modifies the sampling distribution so that more simulations occur in relevant regions, while applying the appropriate likelihood correction.

---

## Quasi-Monte Carlo

Quasi-Monte Carlo replaces pseudorandom samples with low-discrepancy sequences.

Examples include:

* Sobol sequences;
* Halton sequences;
* Faure sequences.

These can improve convergence for certain classes of numerical integration problems.

---

# Why Monte Carlo Is Useful

The Black–Scholes formula is preferable when a closed-form solution exists because it is both fast and accurate.

Monte Carlo becomes substantially more useful when the payoff or underlying model becomes more complicated.

Examples include:

* Asian options;
* barrier options;
* basket options;
* multi-asset derivatives;
* stochastic volatility;
* stochastic interest rates;
* jump-diffusion models;
* high-dimensional derivatives.

The purpose of this project is therefore not to replace the Black–Scholes formula, but to demonstrate a computational technique that generalizes to situations where analytical formulas are unavailable.

---

# Limitations

The model deliberately makes strong assumptions.

## Constant Volatility

The Black–Scholes model assumes

$$
\sigma=\text{constant}.
$$

Real markets exhibit volatility smiles and skews, meaning that implied volatility varies across strike prices and maturities.

---

## Constant Interest Rate

The model assumes that the risk-free rate is deterministic and constant.

Real interest rates are stochastic.

---

## Lognormal Price Dynamics

The underlying is assumed to follow geometric Brownian motion.

This excludes:

* jumps;
* stochastic volatility;
* volatility clustering;
* heavy tails;
* discontinuous price movements.

---

## Frictionless Markets

The theoretical model assumes no:

* transaction costs;
* bid/ask spreads;
* liquidity constraints;
* taxes.

---

## Continuous Trading

The classical Black–Scholes derivation assumes continuous portfolio rebalancing.

Real trading occurs at discrete times and incurs market frictions.

---

## No Dividends

The basic formulation assumes that the underlying pays no dividends.

For a continuous dividend yield $q$, the Black–Scholes call price becomes

$$
C_0
===

## S_0e^{-qT}N(d_1)

Ke^{-rT}N(d_2),
$$

where

$$
d_1
===

\frac{
\ln\left(\frac{S_0}{K}\right)
+
\left(
r-q+\frac{1}{2}\sigma^2
\right)T
}{
\sigma\sqrt{T}
}.
$$

The risk-neutral asset dynamics become

$$
dS_t
====

(r-q)S_t,dt
+
\sigma S_t,dW_t^Q.
$$

---

# PDE Numerical Methods

A numerical PDE implementation typically defines a computational domain

$$
S\in[0,S_{\max}]
$$

and

$$
t\in[0,T].
$$

The asset-price dimension can be discretized into $M$ spatial grid points, while the time dimension can be divided into $L$ time steps.

Common finite-difference schemes include:

### Explicit Euler

Simple to implement, but subject to stability constraints.

### Implicit Euler

More stable, but requires solving a linear system at every time step.

### Crank–Nicolson

A commonly used scheme that combines explicit and implicit discretization and generally provides improved accuracy.

The PDE solution should converge toward the analytical Black–Scholes price as the numerical grid is refined, assuming the boundary conditions and numerical scheme are implemented correctly.

---

# Recommended Validation Tests

A robust implementation should test multiple parameter configurations.

## At-the-Money Call

Set

$$
S_0=K.
$$

This provides a standard baseline.

## In-the-Money Call

Set

$$
S_0>K.
$$

The option should have significant intrinsic value.

## Out-of-the-Money Call

Set

$$
S_0<K.
$$

The option price should be lower, and relative Monte Carlo error may become more significant.

## Short Maturity

Use a small $T$ to test behavior close to expiration.

## High Volatility

Increase $\sigma$ to verify behavior under a more dispersed terminal distribution.

## Monte Carlo Convergence

Increase $N$ systematically and verify approximately

$$
\text{error}\propto N^{-1/2}.
$$

## PDE Grid Convergence

Increase the spatial and temporal resolution and verify convergence toward the Black–Scholes benchmark.

---

# Financial Sanity Checks

The implementation should satisfy basic no-arbitrage properties.

For a European call without dividends,

$$
C_0\geq0.
$$

The standard lower bound is

$$
\boxed{
C_0
\geq
\max
\left(
S_0-Ke^{-rT},
0
\right)
}
$$

The call price should generally:

* increase as $S_0$ increases;
* increase as $\sigma$ increases;
* decrease as $K$ increases;
* generally increase with maturity under standard assumptions;
* decrease as the strike becomes more expensive relative to the underlying.

These properties provide useful diagnostic tests.

---

# Greeks

Once an option-pricing engine has been implemented, the next natural extension is the computation of the option Greeks.

For a European call without dividends:

### Delta

$$
\boxed{
\Delta=N(d_1)
}
$$

### Gamma

$$
\boxed{
\Gamma
======

\frac{
\phi(d_1)
}{
S_0\sigma\sqrt{T}
}
}
$$

### Vega

$$
\boxed{
\nu
===

S_0\phi(d_1)\sqrt{T}
}
$$

### Theta

$$
\boxed{
\Theta
======

-\frac{
S_0\phi(d_1)\sigma
}{
2\sqrt{T}
}
-

rKe^{-rT}N(d_2)
}
$$

### Rho

$$
\boxed{
\rho
====

KTe^{-rT}N(d_2)
}
$$

where $\phi(\cdot)$ is the standard normal probability density function:

$$
\phi(x)
=======

\frac{1}{\sqrt{2\pi}}
e^{-x^2/2}.
$$

Monte Carlo Greeks can be estimated using techniques such as:

* finite differences;
* pathwise derivatives;
* likelihood-ratio methods;
* automatic differentiation.

---

# Performance Considerations

Monte Carlo pricing is computationally simple but can become expensive because convergence is slow.

The key scaling relationship is

$$
\operatorname{SE}
\propto
\frac{1}{\sqrt{N}}.
$$

Consequently, increasing the number of simulations by a factor of $100$ only improves the statistical error by approximately a factor of $10$.

Performance can be improved through:

* vectorized numerical operations;
* efficient random-number generation;
* parallel execution;
* compiled numerical kernels;
* GPU acceleration;
* variance reduction;
* quasi-Monte Carlo.

---

# Common Implementation Errors

Several mistakes are particularly common in Monte Carlo implementations.

## Using the Physical Drift

The risk-neutral simulation should use $r$, not the historical expected return $\mu$:

$$
dS_t=rS_t,dt+\sigma S_t,dW_t^Q.
$$

---

## Omitting the Itô Correction

The exact GBM solution contains

$$
-\frac{1}{2}\sigma^2T.
$$

The correct expression is

$$
S_T
===

S_0
\exp
\left[
\left(
r-\frac12\sigma^2
\right)T
+
\sigma\sqrt{T}Z
\right].
$$

Omitting the $-\frac12\sigma^2$ term produces the wrong distribution.

---

## Forgetting Discounting

The expected payoff is not the current option price.

The price is

$$
C_0
===

e^{-rT}
\mathbb{E}^Q[\text{payoff}].
$$

---

## Using $T$ Instead of $\sqrt{T}$

The stochastic term is

$$
\sigma\sqrt{T}Z,
$$

not

$$
\sigma TZ.
$$

---

## Confusing Volatility and Variance

Volatility is

$$
\sigma,
$$

while variance is

$$
\sigma^2.
$$

---

## Treating Monte Carlo Error as Deterministic

Two Monte Carlo runs with different random seeds will generally produce different estimates.

This is expected.

The correct approach is to report an estimated standard error or confidence interval.

---

# Testing Strategy

A robust implementation should include automated tests.

## Analytical Tests

Verify the Black–Scholes implementation against known benchmark values.

## Monte Carlo Tests

Use a fixed seed and verify that the estimated price falls within a reasonable tolerance.

Because Monte Carlo is stochastic, exact floating-point equality should generally not be expected.

## PDE Tests

Verify convergence as the spatial and temporal grids are refined.

## Financial Property Tests

Verify properties such as:

$$
C_0\geq0
$$

and appropriate monotonicity with respect to model parameters.

## Cross-Method Tests

For a given parameter configuration, verify that

$$
C_{\mathrm{MC}}
\approx
C_{\mathrm{BS}}
\approx
C_{\mathrm{PDE}}.
$$

The tolerance for the Monte Carlo comparison should be based on its statistical uncertainty.

---

# Possible Extensions

The current implementation provides a foundation for more advanced quantitative-finance work.

## Dividend-Paying Assets

Extend the model to include a continuous dividend yield $q$.

## European Put Options

Implement the payoff

$$
P_T
===

\max(K-S_T,0).
$$

The analytical price is

$$
P_0
===

## Ke^{-rT}N(-d_2)

S_0N(-d_1).
$$

The implementation can also be validated using put-call parity:

$$
\boxed{
C_0-P_0
=======

S_0-Ke^{-rT}
}
$$

for a non-dividend-paying underlying.

## Asian Options

Asian options depend on the average underlying price over the life of the contract.

Monte Carlo becomes particularly useful because the payoff depends on the entire simulated path.

## Barrier Options

Examples include:

* up-and-out calls;
* down-and-out calls;
* up-and-in calls;
* down-and-in calls.

These require monitoring the simulated asset path rather than only its terminal value.

## Stochastic Volatility

Replace constant volatility with a stochastic process, such as the Heston model.

## Jump-Diffusion

Introduce discontinuous price movements using a jump-diffusion model such as Merton's model.

## American Options

American options can be exercised before maturity.

Monte Carlo pricing then becomes an optimal-stopping problem.

Methods such as Longstaff–Schwartz least-squares Monte Carlo can be investigated.

## Calibration

Instead of assuming a volatility value, calibrate the model to observed market option prices or implied volatilities.

This would turn the project into a more realistic quantitative-finance calibration framework.

## GPU Acceleration

Monte Carlo is highly parallelizable, making GPU implementations particularly attractive for large simulation workloads.

---

# Reproducible Experiment Design

For meaningful numerical experiments, record:

* model parameters;
* number of simulations;
* random seed;
* Monte Carlo price;
* sample standard deviation;
* standard error;
* confidence interval;
* Black–Scholes benchmark;
* absolute error;
* relative error;
* execution time.

A useful experiment table is:

|         $N$ | Monte Carlo Price | Black–Scholes Price | Absolute Error | Standard Error | Runtime |
| ----------: | ----------------: | ------------------: | -------------: | -------------: | ------: |
|     $1,000$ |               ... |                 ... |            ... |            ... |     ... |
|    $10,000$ |               ... |                 ... |            ... |            ... |     ... |
|   $100,000$ |               ... |                 ... |            ... |            ... |     ... |
| $1,000,000$ |               ... |                 ... |            ... |            ... |     ... |

This makes the convergence behavior of the estimator directly observable.

---

# Mathematical Interpretation

The project illustrates an important connection between stochastic processes, numerical analysis, and mathematical finance.

Starting from the risk-neutral stochastic differential equation,

$$
dS_t
====

rS_t,dt
+
\sigma S_t,dW_t^Q,
$$

the derivative value is

$$
C(S,t)
======

\mathbb{E}^Q
\left[
e^{-r(T-t)}
\Phi(S_T)
\mid S_t=S
\right],
$$

where

$$
\Phi(S_T)
=========

\max(S_T-K,0).
$$

The Feynman–Kac theorem establishes that this conditional expectation corresponds to the solution of the Black–Scholes PDE.

Thus,

$$
\boxed{
\text{SDE}
\quad
\longleftrightarrow
\quad
\text{Risk-Neutral Expectation}
\quad
\longleftrightarrow
\quad
\text{PDE}
}
$$

The three numerical approaches can therefore be viewed as different computational representations of the same mathematical problem.

---

# Computational Workflow

The complete workflow can be summarized as:

```text
Model Parameters
      │
      ├── S₀
      ├── K
      ├── T
      ├── r
      └── σ
      │
      ▼
Risk-Neutral GBM
      │
      ▼
Generate Z ~ N(0, 1)
      │
      ▼
Simulate S_T
      │
      ▼
Calculate Payoffs
      │
      ▼
Discount and Average
      │
      ▼
Monte Carlo Price
      │
      ├──────────────────┐
      │                  │
      ▼                  ▼
Black–Scholes       Black–Scholes
Closed Form             PDE
      │                  │
      └────────┬─────────┘
               ▼
          Validation
               │
               ▼
      Error / Convergence
```

---

# References

The theoretical foundation of this project comes from the following areas of mathematical finance:

1. **Black, F. and Scholes, M.**
   *The Pricing of Options and Corporate Liabilities*.
   Journal of Political Economy, 1973.

2. **Merton, R. C.**
   *Theory of Rational Option Pricing*.
   Bell Journal of Economics and Management Science, 1973.

3. **Hull, J. C.**
   *Options, Futures, and Other Derivatives*.

4. **Glasserman, P.**
   *Monte Carlo Methods in Financial Engineering*.

5. **Shreve, S. E.**
   *Stochastic Calculus for Finance II: Continuous-Time Models*.

6. **Wilmott, P.**
   *Paul Wilmott on Quantitative Finance*.

These references cover the stochastic calculus, risk-neutral valuation, Monte Carlo methods, derivative pricing, and PDE formulations used throughout the project.

---

# Disclaimer

This repository is an **educational and computational project** demonstrating numerical option-pricing techniques.

It should not be interpreted as:

* investment advice;
* a trading strategy;
* a production-grade pricing library;
* a source of market forecasts;
* a substitute for professional quantitative-risk infrastructure.

The Black–Scholes model is a deliberately simplified representation of financial markets, and its assumptions do not fully describe real-world asset dynamics.

---

# License

This project is released under the license specified in the repository.

If no license has yet been selected, consider adding an explicit open-source license such as the MIT License before distributing the project publicly.

---

# Summary

This project implements a fundamental quantitative-finance workflow:

$$
\boxed{
\text{Model}
\rightarrow
\text{Simulate}
\rightarrow
\text{Price}
\rightarrow
\text{Validate}
}
$$

The underlying asset is modeled using geometric Brownian motion under the risk-neutral measure:

$$
dS_t
====

rS_t,dt
+
\sigma S_t,dW_t^Q.
$$

The European call price is estimated using Monte Carlo:

$$
\boxed{
\hat{C}_N
=========

e^{-rT}
\frac{1}{N}
\sum_{i=1}^{N}
\max
\left(
S_T^{(i)}-K,
0
\right)
}
$$

and validated against the analytical Black–Scholes formula:

$$
\boxed{
C_0
===

## S_0N(d_1)

Ke^{-rT}N(d_2)
}
$$

as well as the Black–Scholes PDE:

$$
\boxed{
\frac{\partial C}{\partial t}
+
\frac{1}{2}\sigma^2S^2
\frac{\partial^2 C}{\partial S^2}
+
rS\frac{\partial C}{\partial S}
-------------------------------

# rC

0.

}
$$

The central numerical result is that Monte Carlo pricing is a **statistical estimation problem** whose standard error decreases at the rate

$$
O\left(N^{-1/2}\right).
$$

The central mathematical result is that the **stochastic, analytical, and PDE formulations are different representations of the same derivative-pricing problem**.

This makes the project a useful foundation for studying:

* computational finance;
* stochastic differential equations;
* Monte Carlo methods;
* numerical PDEs;
* statistical estimation;
* quantitative risk;
* derivative pricing.
