# European Option Pricing Model

A basic Monte Carlo framework for pricing **European call options**, with numerical results validated against both the **Black–Scholes closed-form solution** and the **Black–Scholes partial differential equation (PDE)**.

The project is intended as a computational demonstration of how stochastic simulation can be used to estimate derivative prices and how the resulting Monte Carlo estimator relates to the classical analytical and PDE formulations of the Black–Scholes model.

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
  * [Black–Scholes Closed-Form Solution](#black-scholes-closed-form-solution)
  * [Black–Scholes PDE](#black-scholes-pde)
* [Monte Carlo Algorithm](#monte-carlo-algorithm)
* [Validation Methodology](#validation-methodology)
* [Convergence and Statistical Error](#convergence-and-statistical-error)
* [Project Structure](#project-structure)
* [Installation](#installation)
* [Usage](#usage)
* [Model Parameters](#model-parameters)
* [Example Workflow](#example-workflow)
* [Interpreting the Results](#interpreting-the-results)
* [Numerical Considerations](#numerical-considerations)
* [Limitations](#limitations)
* [Possible Extensions](#possible-extensions)
* [Theoretical Background](#theoretical-background)
* [References](#references)
* [License](#license)

---

## Overview

This project implements a **Monte Carlo option pricing model** for a European call option under the standard Black–Scholes assumptions.

The central idea is straightforward:

1. Model the evolution of the underlying asset using **geometric Brownian motion**.
2. Simulate a large number of possible terminal asset prices.
3. Evaluate the option payoff for each simulated path.
4. Discount the average payoff back to the present under the risk-neutral measure.
5. Compare the Monte Carlo estimate against:

   * the **Black–Scholes analytical formula**, and
   * a numerical solution of the **Black–Scholes PDE**.

For a European call option with strike price (K) and maturity (T), the payoff is

[
C_T = \max(S_T-K,0),
]

where (S_T) is the underlying asset price at maturity.

The Monte Carlo estimator approximates the option price through

[
C_0 \approx e^{-rT}\frac{1}{N}
\sum_{i=1}^{N}
\max(S_T^{(i)}-K,0),
]

where:

* (S_0) is the current underlying price,
* (K) is the strike price,
* (T) is the time to maturity,
* (r) is the continuously compounded risk-free interest rate,
* (\sigma) is the volatility,
* (N) is the number of Monte Carlo simulations.

The analytical Black–Scholes price provides a deterministic benchmark against which the stochastic Monte Carlo approximation can be tested.

---

# Project Objectives

The project has several objectives.

### 1. Implement Monte Carlo option pricing

Generate risk-neutral samples of the underlying asset price and use those samples to estimate the discounted expected payoff.

### 2. Demonstrate stochastic convergence

Show that increasing the number of simulations causes the Monte Carlo estimator to converge toward the theoretical option price.

### 3. Validate against Black–Scholes

Use the closed-form Black–Scholes formula as a high-precision reference value.

### 4. Connect the probabilistic and PDE formulations

The Black–Scholes framework admits both:

* a probabilistic interpretation through risk-neutral expectations, and
* a deterministic interpretation through a parabolic PDE.

The project demonstrates the numerical consistency between these approaches.

### 5. Provide a computational foundation

The implementation can serve as a starting point for more advanced derivative-pricing techniques, including:

* variance reduction,
* path-dependent options,
* stochastic volatility,
* interest-rate models,
* American option pricing,
* finite-difference PDE solvers,
* quasi-Monte Carlo methods.

---

# Financial Background

## European Call Option

A European call option gives its holder the right, but not the obligation, to purchase an underlying asset for a fixed strike price (K) at a specified maturity date (T).

Its payoff at maturity is

[
\boxed{
\max(S_T-K,0)
}
]

where (S_T) is the asset price at maturity.

There are two possible cases.

### In-the-money

If

[
S_T>K,
]

the option has positive value:

[
C_T=S_T-K.
]

### Out-of-the-money

If

[
S_T\leq K,
]

the option expires worthless:

[
C_T=0.
]

Therefore,

[
C_T=(S_T-K)^+,
]

where

[
x^+=\max(x,0).
]

---

# Underlying Asset Model

The standard Black–Scholes model assumes that the underlying asset follows a **geometric Brownian motion**.

Under the physical probability measure,

[
dS_t=\mu S_t,dt+\sigma S_t,dW_t,
]

where:

* (S_t) is the underlying asset price,
* (\mu) is the expected return,
* (\sigma) is the volatility,
* (W_t) is a standard Brownian motion.

For option pricing, however, the relevant dynamics are expressed under the **risk-neutral measure**:

[
\boxed{
dS_t=rS_t,dt+\sigma S_t,dW_t^Q
}
]

where (r) is the risk-free rate.

The drift changes from (\mu) to (r) because derivative prices are obtained through risk-neutral valuation rather than by directly forecasting the expected physical return of the asset.

---

# Mathematical Formulation

## Geometric Brownian Motion

The stochastic differential equation

[
dS_t=rS_t,dt+\sigma S_t,dW_t
]

has the exact solution

[
\boxed{
S_T =
S_0
\exp
\left[
\left(r-\frac{1}{2}\sigma^2\right)T
+
\sigma W_T
\right]
}
]

and since

[
W_T\sim N(0,T),
]

we can write

[
W_T=\sqrt{T}Z,
\qquad
Z\sim N(0,1).
]

Therefore,

[
\boxed{
S_T =
S_0
\exp
\left[
\left(r-\frac{1}{2}\sigma^2\right)T
+
\sigma\sqrt{T}Z
\right]
}
]

This expression is particularly useful for Monte Carlo pricing because terminal asset prices can be generated directly without numerically discretizing the stochastic differential equation.

---

# Monte Carlo Pricing

Under risk-neutral valuation, the present value of a European call is

[
C_0=
e^{-rT}
\mathbb{E}^Q
\left[
(S_T-K)^+
\right].
]

Monte Carlo replaces the expectation with a sample average.

Generate (N) independent standard normal random variables

[
Z_1,\ldots,Z_N\sim N(0,1).
]

For each sample, calculate

[
S_T^{(i)}
=========

S_0
\exp
\left[
\left(r-\frac12\sigma^2\right)T
+
\sigma\sqrt{T}Z_i
\right].
]

Then calculate the corresponding payoff

[
P_i=
\max(S_T^{(i)}-K,0).
]

The Monte Carlo estimator is

[
\boxed{
\hat C_N
========

e^{-rT}
\frac{1}{N}
\sum_{i=1}^{N}P_i
}
]

As (N\rightarrow\infty),

[
\hat C_N\rightarrow C_0
]

under the law of large numbers.

---

# Black–Scholes Closed-Form Solution

For a European call option paying no dividends, the Black–Scholes price is

[
\boxed{
C_0=S_0N(d_1)-Ke^{-rT}N(d_2)
}
]

where (N(\cdot)) is the cumulative distribution function of the standard normal distribution.

The terms (d_1) and (d_2) are

[
\boxed{
d_1=
\frac{
\ln(S_0/K)
+
(r+\frac12\sigma^2)T
}{
\sigma\sqrt{T}
}
}
]

and

[
\boxed{
d_2=d_1-\sigma\sqrt{T}
}
]

The Black–Scholes price serves as the analytical benchmark for the Monte Carlo implementation.

---

# Black–Scholes PDE

The same option price can also be obtained from the Black–Scholes partial differential equation.

Let

[
C=C(S,t)
]

denote the value of the European call option at time (t) when the underlying asset has price (S).

The Black–Scholes PDE is

[
\boxed{
\frac{\partial C}{\partial t}
+
\frac12\sigma^2S^2
\frac{\partial^2C}{\partial S^2}
+
rS\frac{\partial C}{\partial S}
-rC
=0
}
]

with terminal condition

[
\boxed{
C(S,T)=\max(S-K,0)
}
]

and appropriate boundary conditions.

For a European call, the asymptotic boundary behavior is approximately

[
C(0,t)=0
]

and, for sufficiently large (S),

[
C(S,t)\sim S-Ke^{-r(T-t)}.
]

A numerical PDE solver can discretize the spatial and temporal domains and solve backward from the terminal payoff.

---

# Relationship Between Monte Carlo, Black–Scholes, and the PDE

These three approaches are different numerical representations of the same mathematical pricing problem.

### Monte Carlo

Computes the expectation

[
C_0=
e^{-rT}\mathbb E^Q[(S_T-K)^+]
]

using random samples.

### Black–Scholes formula

Evaluates the same expectation analytically:

[
C_0=S_0N(d_1)-Ke^{-rT}N(d_2).
]

### Black–Scholes PDE

Solves the deterministic PDE

[
C_t+\frac12\sigma^2S^2C_{SS}+rSC_S-rC=0
]

with terminal payoff

[
C(S,T)=(S-K)^+.
]

The equivalence between the risk-neutral expectation and the PDE formulation follows from the **Feynman–Kac framework**.

Consequently, agreement between the Monte Carlo estimate, the closed-form Black–Scholes price, and the PDE solution provides a useful validation of the numerical implementation.

---

# Monte Carlo Algorithm

The pricing procedure can be summarized as follows.

### Step 1 — Define model parameters

Specify

[
S_0,\quad K,\quad T,\quad r,\quad \sigma,\quad N.
]

### Step 2 — Generate random samples

Generate

[
Z_i\sim N(0,1).
]

### Step 3 — Simulate terminal asset prices

For each sample,

[
S_T^{(i)}
=========

S_0
\exp
\left[
(r-\frac12\sigma^2)T
+
\sigma\sqrt{T}Z_i
\right].
]

### Step 4 — Calculate option payoffs

[
P_i=\max(S_T^{(i)}-K,0).
]

### Step 5 — Average the payoffs

[
\bar P=
\frac1N\sum_{i=1}^{N}P_i.
]

### Step 6 — Discount to the present

[
\hat C_N=e^{-rT}\bar P.
]

### Step 7 — Compare with Black–Scholes

Calculate

[
C_{\mathrm{BS}}
===============

S_0N(d_1)-Ke^{-rT}N(d_2).
]

The Monte Carlo pricing error can then be measured as

[
\boxed{
\epsilon_{\mathrm{MC}}
======================

\hat C_N-C_{\mathrm{BS}}
}
]

or in absolute terms,

[
|\epsilon_{\mathrm{MC}}|.
]

---

# Validation Methodology

The primary validation strategy is to compare three independent calculations:

| Method        | Approach                       | Expected behavior              |
| ------------- | ------------------------------ | ------------------------------ |
| Monte Carlo   | Statistical simulation         | Converges with increasing (N)  |
| Black–Scholes | Analytical closed form         | Reference solution             |
| PDE           | Numerical deterministic solver | Converges with grid refinement |

The most important validation experiment is to increase the Monte Carlo sample size.

For example, one can evaluate

[
N=10^2,;10^3,;10^4,;10^5,;10^6
]

and observe how

[
\hat C_N
]

approaches the Black–Scholes value.

A useful convergence plot is:

[
\text{Monte Carlo Price}
\quad\text{vs.}\quad
\text{Number of Simulations}.
]

The Black–Scholes price can be plotted as a horizontal reference line.

---

# Convergence and Statistical Error

Monte Carlo methods converge relatively slowly.

For an estimator with finite variance,

[
\operatorname{SE}(\hat C_N)
===========================

\frac{\sigma_P}{\sqrt{N}},
]

where (\sigma_P) is the standard deviation of the discounted payoff.

The key relationship is therefore

[
\boxed{
\text{Monte Carlo error}\sim O(N^{-1/2})
}
]

This has an important practical consequence.

To reduce the statistical error by a factor of 10, approximately 100 times as many simulations are required.

For example:

| Simulations | Approximate error scale |
| ----------: | ----------------------: |
|      (10^2) |               (10^{-1}) |
|      (10^4) |               (10^{-2}) |
|      (10^6) |               (10^{-3}) |
|      (10^8) |               (10^{-4}) |

These values describe the scaling behavior rather than guaranteed absolute errors.

---

## Monte Carlo Confidence Interval

Let

[
X_i=e^{-rT}(S_T^{(i)}-K)^+
]

be the discounted payoff.

The sample mean is

[
\hat C_N=\frac1N\sum_{i=1}^NX_i.
]

The sample variance is

[
s_X^2=
\frac{1}{N-1}
\sum_{i=1}^N
(X_i-\hat C_N)^2.
]

The estimated standard error is

[
\boxed{
\widehat{\operatorname{SE}}
===========================

\frac{s_X}{\sqrt N}
}
]

For sufficiently large (N), an approximate 95% confidence interval is

[
\boxed{
\hat C_N
\pm
1.96
\frac{s_X}{\sqrt N}
}
]

This is a much more informative validation metric than simply reporting the difference between Monte Carlo and Black–Scholes prices.

A Monte Carlo estimate that differs from the analytical solution by a small amount is not necessarily "wrong"; the relevant question is whether the discrepancy is consistent with the estimator's statistical uncertainty.

---

# Project Structure

A typical project organization is:

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

The exact structure depends on the implementation contained in the repository.

A sensible separation of responsibilities is:

* `monte_carlo.py` — stochastic simulation and pricing;
* `black_scholes.py` — analytical pricing formula;
* `pde.py` — numerical solution of the Black–Scholes PDE;
* `tests/` — numerical and regression tests;
* `notebooks/` — experiments and visualizations.

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

Install the dependencies:

```bash
pip install -r requirements.txt
```

If the project is packaged as a Python module, install it in editable mode:

```bash
pip install -e .
```

---

# Usage

The exact execution command depends on the repository implementation.

A typical command-line workflow might look like:

```bash
python src/monte_carlo.py
```

or, if the implementation exposes a Python module:

```bash
python -m src.monte_carlo
```

For notebook-based experimentation:

```bash
jupyter notebook
```

Then open the relevant notebook under `notebooks/`.

---

# Model Parameters

The pricing model is controlled by the following parameters.

| Parameter           |   Symbol | Description                            |
| ------------------- | -------: | -------------------------------------- |
| Initial asset price |    (S_0) | Current underlying price               |
| Strike price        |      (K) | Exercise price                         |
| Maturity            |      (T) | Time to expiration                     |
| Risk-free rate      |      (r) | Continuously compounded risk-free rate |
| Volatility          | (\sigma) | Annualized volatility                  |
| Simulations         |      (N) | Number of Monte Carlo samples          |

For example, a test configuration could use:

```text
S0      = 100
K       = 100
T       = 1
r       = 0.05
sigma   = 0.20
N       = 1,000,000
```

These values correspond to an at-the-money European call with one year to maturity.

They are illustrative parameters only; they are not market forecasts.

---

# Example Workflow

Consider a European call with

[
S_0=100,
]

[
K=100,
]

[
T=1,
]

[
r=0.05,
]

and

[
\sigma=0.20.
]

The Monte Carlo simulation generates independent samples

[
Z_i\sim N(0,1)
]

and transforms them into terminal prices:

[
S_T^{(i)}
=========

100
\exp
\left[
(0.05-\frac12(0.20)^2)
+
0.20Z_i
\right].
]

For every terminal price, the payoff is

[
P_i=\max(S_T^{(i)}-100,0).
]

The price estimate is then

[
\hat C_N
========

e^{-0.05}
\frac1N
\sum_{i=1}^NP_i.
]

The corresponding Black–Scholes benchmark is

[
C_{\mathrm{BS}}
===============

## 100N(d_1)

100e^{-0.05}N(d_2),
]

with

[
d_1=
\frac{
\ln(100/100)+(0.05+0.5(0.20)^2)
}{
0.20
}
]

and

[
d_2=d_1-0.20.
]

The Monte Carlo estimate should fluctuate around the analytical value, with the magnitude of the fluctuations decreasing as the number of simulations increases.

---

# Interpreting the Results

The primary output of the model is the estimated call price.

A typical validation table can be structured as follows:

| Number of simulations | Monte Carlo price | Black–Scholes price | Absolute error |
| --------------------: | ----------------: | ------------------: | -------------: |
|                 1,000 |               ... |                 ... |            ... |
|                10,000 |               ... |                 ... |            ... |
|               100,000 |               ... |                 ... |            ... |
|             1,000,000 |               ... |                 ... |            ... |

The exact values depend on the random seed and implementation.

A good implementation should demonstrate that:

1. The Monte Carlo estimator approaches the Black–Scholes value.
2. The error decreases approximately at the (N^{-1/2}) rate.
3. Independent simulations produce slightly different estimates.
4. The differences are consistent with Monte Carlo statistical error.
5. The PDE solution approaches the same price as its numerical grid is refined.

---

# Random Seeds and Reproducibility

Monte Carlo methods depend on pseudorandom number generation.

For reproducible experiments, explicitly specify a random seed.

For example:

```python
rng = np.random.default_rng(42)
```

Using a fixed seed ensures that repeated executions generate the same random sequence.

However, a fixed seed should primarily be used for:

* testing,
* debugging,
* reproducible demonstrations,
* regression experiments.

For statistical analysis, it is often useful to repeat the pricing experiment using multiple independent seeds.

This allows the distribution of the estimator itself to be studied.

---

# Numerical Considerations

## Exact Simulation of GBM

For European options under constant Black–Scholes parameters, the terminal asset price can be sampled exactly using

[
S_T =
S_0
\exp
\left[
(r-\frac12\sigma^2)T
+
\sigma\sqrt{T}Z
\right].
]

There is no need to use Euler–Maruyama for this particular problem.

This is important because Euler discretization introduces an additional numerical error that is unnecessary when only the terminal value is required.

---

## Floating-Point Precision

The implementation should use standard floating-point arithmetic carefully.

Potential numerical issues include:

* extremely large or small exponential arguments;
* very short maturities;
* extremely high volatility;
* deep in-the-money or out-of-the-money options;
* extreme values of (S_0/K).

For ordinary parameter ranges, double precision is more than adequate.

---

## Vectorization

Monte Carlo pricing is naturally vectorizable.

Rather than evaluating each simulation in a Python loop, a numerical computing library can generate a vector of normal random variables and operate on the entire array.

Conceptually:

```text
Z = [Z1, Z2, ..., ZN]

        ↓

ST = S0 * exp(... + sigma * sqrt(T) * Z)

        ↓

payoff = max(ST - K, 0)

        ↓

price = exp(-r*T) * mean(payoff)
```

Vectorization can provide a substantial performance improvement for large simulation counts.

---

# Monte Carlo Variance Reduction

The basic implementation uses ordinary Monte Carlo sampling.

For more demanding applications, the estimator can be improved through variance-reduction techniques.

## Antithetic Variates

For every sampled

[
Z_i,
]

also use

[
-Z_i.
]

This preserves the marginal distribution while introducing negative dependence between paired samples.

The paired estimator can reduce variance for many option-pricing problems.

---

## Control Variates

A control variate uses another random variable whose expectation is known analytically.

For example, the simulated underlying terminal price satisfies

[
\mathbb E^Q[S_T]=S_0e^{rT}.
]

Therefore,

[
e^{-rT}S_T
]

has known expectation (S_0).

This known expectation can be used to construct a control-variate estimator for the call price.

---

## Importance Sampling

For rare-event pricing problems, standard Monte Carlo may spend most of its simulations in regions contributing little to the payoff.

Importance sampling changes the sampling distribution so that more simulations occur in important regions, while correcting for the change of measure.

This can substantially improve efficiency for deep out-of-the-money options and other rare-event problems.

---

## Quasi-Monte Carlo

Instead of pseudorandom samples, quasi-Monte Carlo methods use low-discrepancy sequences such as:

* Sobol sequences,
* Halton sequences,
* Faure sequences.

These methods can provide significantly better convergence in some pricing problems.

---

# Why Monte Carlo Is Useful

The closed-form Black–Scholes formula is preferable when it is available because it is fast and accurate.

Monte Carlo becomes particularly useful when the derivative has features that make analytical solutions difficult or impossible.

Examples include:

* path-dependent payoffs;
* Asian options;
* barrier options;
* basket options;
* stochastic volatility;
* stochastic interest rates;
* multiple correlated assets;
* high-dimensional derivatives.

Therefore, this project is best viewed not as an attempt to replace Black–Scholes, but as an introduction to a much more general computational pricing methodology.

---

# Limitations

The model intentionally makes strong assumptions.

## Constant Volatility

The Black–Scholes model assumes

[
\sigma=\text{constant}.
]

Real markets exhibit volatility smiles and skews, meaning implied volatility depends on strike and maturity.

---

## Constant Interest Rate

The model assumes a deterministic constant risk-free rate.

Real interest rates evolve over time.

---

## Lognormal Asset Dynamics

The model assumes that the asset follows geometric Brownian motion.

This excludes effects such as:

* jumps,
* stochastic volatility,
* discontinuous price movements,
* heavy tails,
* volatility clustering.

---

## Frictionless Markets

The classical model assumes no:

* transaction costs,
* bid/ask spreads,
* liquidity constraints,
* taxes.

---

## Continuous Trading

The theoretical derivation assumes continuous rebalancing.

Real portfolios are rebalanced discretely.

---

## No Dividends

The basic formulation assumes the underlying does not pay dividends.

For a continuously compounded dividend yield (q), the Black–Scholes call price becomes

[
C_0
===

## S_0e^{-qT}N(d_1)

Ke^{-rT}N(d_2),
]

with

[
d_1=
\frac{
\ln(S_0/K)
+
(r-q+\frac12\sigma^2)T
}{
\sigma\sqrt T
}.
]

The risk-neutral asset dynamics also become

[
dS_t=(r-q)S_tdt+\sigma S_tdW_t.
]

---

# PDE Numerical Methods

A numerical PDE implementation typically discretizes

[
S\in[0,S_{\max}]
]

and

[
t\in[0,T].
]

The spatial dimension can be divided into (M) grid points and time into (L) time steps.

Common finite-difference schemes include:

### Explicit Euler

Simple to implement, but subject to stability restrictions.

### Implicit Euler

More stable, but requires solving a linear system at every time step.

### Crank–Nicolson

A commonly used scheme combining explicit and implicit discretization.

The numerical PDE price should converge toward the analytical Black–Scholes price as the grid is refined, assuming the boundary conditions and numerical scheme are implemented correctly.

---

# Recommended Validation Tests

A robust implementation should test more than one parameter configuration.

## Test 1 — At-the-money call

[
S_0=K.
]

This is a standard baseline case.

## Test 2 — In-the-money call

[
S_0>K.
]

The option should have substantial intrinsic value.

## Test 3 — Out-of-the-money call

[
S_0<K.
]

The price should be lower and the Monte Carlo estimator may require more simulations for a given relative precision.

## Test 4 — Short maturity

Use a small (T) to test numerical behavior close to expiration.

## Test 5 — High volatility

Increase (\sigma) to verify that the implementation behaves correctly under more dispersed terminal distributions.

## Test 6 — Monte Carlo convergence

Increase (N) systematically and verify the expected

[
O(N^{-1/2})
]

convergence rate.

## Test 7 — PDE grid convergence

Increase the number of spatial and temporal grid points and verify convergence toward Black–Scholes.

---

# Financial Sanity Checks

The implementation should satisfy basic option-pricing properties.

For a European call without dividends,

[
C\geq0.
]

Also,

[
C\geq\max(S_0-Ke^{-rT},0)
]

under standard no-arbitrage assumptions.

The call price should generally:

* increase with (S_0);
* increase with (\sigma);
* increase with (T) under standard conditions;
* decrease with (K);
* decrease as (r) increases for a non-dividend-paying call, subject to the usual interpretation of the model.

These relationships provide useful tests for detecting implementation errors.

---

# Greeks

Once an option-pricing engine exists, the next natural extension is calculating the option Greeks.

For a European call without dividends:

### Delta

[
\Delta=N(d_1)
]

### Gamma

[
\Gamma=
\frac{\phi(d_1)}
{S_0\sigma\sqrt T}
]

### Vega

[
\nu=
S_0\phi(d_1)\sqrt T
]

### Theta

[
\Theta
======

-\frac{
S_0\phi(d_1)\sigma
}{
2\sqrt T
}
-rKe^{-rT}N(d_2)
]

### Rho

[
\rho=
KTe^{-rT}N(d_2).
]

Here,

[
\phi(x)=
\frac{1}{\sqrt{2\pi}}
e^{-x^2/2}
]

is the standard normal probability density function.

For Monte Carlo, Greeks can be estimated using techniques such as:

* finite differences,
* pathwise derivatives,
* likelihood-ratio methods,
* automatic differentiation.

---

# Performance Considerations

Monte Carlo pricing is computationally simple but potentially expensive because accuracy improves slowly.

If

[
N=10^6,
]

then one million terminal asset prices must be generated and processed.

Performance can be improved through:

* vectorized numerical operations;
* efficient random-number generation;
* parallel execution;
* compiled numerical kernels;
* GPU acceleration;
* variance reduction;
* quasi-Monte Carlo sampling.

The primary bottleneck is generally the number of simulations rather than the complexity of each individual simulation.

---

# Reproducible Experiment Design

For meaningful numerical experiments, record:

* model parameters;
* number of simulations;
* random seed;
* Monte Carlo estimate;
* sample standard deviation;
* standard error;
* confidence interval;
* Black–Scholes benchmark;
* absolute error;
* relative error;
* execution time.

A useful experiment table is:

|       (N) | MC Price | BS Price | Error | Standard Error | Runtime |
| --------: | -------: | -------: | ----: | -------------: | ------: |
|     1,000 |      ... |      ... |   ... |            ... |     ... |
|    10,000 |      ... |      ... |   ... |            ... |     ... |
|   100,000 |      ... |      ... |   ... |            ... |     ... |
| 1,000,000 |      ... |      ... |   ... |            ... |     ... |

This makes the numerical behavior of the estimator directly observable.

---

# Mathematical Interpretation

The project illustrates an important connection between stochastic processes, numerical analysis, and mathematical finance.

Starting from the risk-neutral stochastic differential equation,

[
dS_t=rS_tdt+\sigma S_tdW_t,
]

the derivative value is

[
C(S,t)
======

\mathbb E^Q
\left[
e^{-r(T-t)}
\Phi(S_T)
\mid S_t=S
\right],
]

where

[
\Phi(S_T)=\max(S_T-K,0).
]

The Feynman–Kac theorem establishes that this conditional expectation corresponds to the solution of the Black–Scholes PDE.

Thus,

[
\boxed{
\text{SDE}
\longleftrightarrow
\text{Risk-Neutral Expectation}
\longleftrightarrow
\text{PDE}
}
]

The project numerically explores this equivalence from three directions:

```text
                 Geometric Brownian Motion
                          │
                          ▼
                 Risk-Neutral Distribution
                          │
                          ▼
                    Monte Carlo
                          │
                          ▼
                    Option Price
                          ▲
                          │
          ┌───────────────┴───────────────┐
          │                               │
          │                               │
  Black–Scholes Formula            Black–Scholes PDE
   Analytical Solution             Numerical Solution
```

Agreement among the three methods provides strong evidence that the implementation is mathematically consistent.

---

# Possible Extensions

The current model provides a natural foundation for substantially more sophisticated research and engineering work.

## 1. Dividend-paying assets

Add a continuous dividend yield (q).

---

## 2. Put options

Implement

[
P_T=\max(K-S_T,0).
]

The European put price can be obtained from

[
P_0=
Ke^{-rT}N(-d_2)
---------------

S_0N(-d_1).
]

The implementation can also be validated using put-call parity:

[
\boxed{
C-P=S_0-Ke^{-rT}
}
]

for a non-dividend-paying underlying.

---

## 3. Asian options

Asian options depend on the average asset price over the life of the option.

Monte Carlo becomes particularly useful because the payoff depends on the entire simulated path.

---

## 4. Barrier options

Examples include:

* up-and-out calls;
* down-and-out calls;
* up-and-in calls;
* down-and-in calls.

These require monitoring the simulated asset path rather than only its terminal value.

---

## 5. Stochastic volatility

Replace constant volatility with a stochastic process.

Examples include:

* Heston model;
* SABR model;
* local volatility models.

---

## 6. Jump-diffusion models

Introduce discontinuous price movements using models such as Merton's jump-diffusion model.

---

## 7. American options

American options can be exercised before maturity.

Monte Carlo pricing becomes substantially more complicated because the problem involves optimal stopping.

Methods such as:

* Longstaff–Schwartz regression,
* least-squares Monte Carlo,
* stochastic mesh methods

can be investigated.

---

## 8. Automatic differentiation

Automatic differentiation can be used to calculate sensitivities through the computational pricing graph.

---

## 9. GPU acceleration

Large Monte Carlo workloads are highly parallelizable and can be accelerated using GPU frameworks.

---

## 10. Calibration

Rather than assuming volatility, the model can be calibrated to observed market option prices or implied volatilities.

This would transform the project from a purely theoretical pricing exercise into a basic quantitative-finance calibration framework.

---

# Common Implementation Errors

Several mistakes are particularly common in Monte Carlo implementations.

### Using the physical drift (\mu)

For risk-neutral pricing, the simulation should use

[
r
]

rather than an estimated historical expected return (\mu).

---

### Forgetting the (-\frac12\sigma^2) term

The correct exact GBM expression is

[
S_T=
S_0
e^{
(r-\frac12\sigma^2)T
+
\sigma\sqrt{T}Z
}.
]

Leaving out the correction term produces an incorrect lognormal distribution.

---

### Forgetting discounting

The expected payoff is not itself the present option price.

The discounted estimator is

[
e^{-rT}\mathbb E^Q[\text{payoff}].
]

---

### Using (T) instead of (\sqrt T)

The stochastic component is

[
\sigma\sqrt T Z,
]

not

[
\sigma TZ.
]

---

### Confusing volatility and variance

The model parameter (\sigma) is volatility.

The variance is

[
\sigma^2.
]

---

### Treating Monte Carlo error as deterministic

Two runs with different random seeds will generally produce different estimates.

That is expected behavior.

The estimator should therefore be accompanied by a standard error or confidence interval.

---

# Testing Strategy

A production-quality implementation should include automated tests.

### Analytical tests

Verify the Black–Scholes implementation against known benchmark values.

### Monte Carlo tests

Use a fixed random seed and verify that the output falls within a reasonable numerical tolerance.

Because Monte Carlo is stochastic, tests should generally avoid unnecessarily strict equality checks.

### PDE tests

Verify convergence as the grid is refined.

### Property tests

Check financial relationships such as:

[
C\geq0
]

and monotonicity with respect to key parameters.

### Cross-method tests

For a given parameter set, verify that

[
C_{\mathrm{MC}}
\approx
C_{\mathrm{BS}}
\approx
C_{\mathrm{PDE}}.
]

The tolerance for the Monte Carlo comparison should be based on its estimated statistical uncertainty rather than an arbitrary deterministic threshold.

---

# Disclaimer

This repository is an **educational and computational project** demonstrating numerical option pricing techniques.

It should not be interpreted as:

* investment advice;
* a trading strategy;
* a production-grade pricing library;
* a source of market forecasts;
* a substitute for professional quantitative-risk infrastructure.

The Black–Scholes model is a deliberately simplified model of financial markets, and its assumptions do not fully describe real-world asset dynamics.

---

# References

The following topics provide the theoretical foundation for the project:

1. **Black, F. and Scholes, M.** — *The Pricing of Options and Corporate Liabilities*, Journal of Political Economy, 1973.

2. **Merton, R. C.** — *Theory of Rational Option Pricing*, Bell Journal of Economics and Management Science, 1973.

3. **Hull, J. C.** — *Options, Futures, and Other Derivatives*.

4. **Glasserman, P.** — *Monte Carlo Methods in Financial Engineering*.

5. **Shreve, S. E.** — *Stochastic Calculus for Finance II: Continuous-Time Models*.

6. **Wilmott, P.** — *Paul Wilmott on Quantitative Finance*.

These references cover the stochastic calculus, risk-neutral valuation, Monte Carlo methods, derivative pricing, and PDE formulations underlying the implementation.

---

# Summary

This project implements a fundamental quantitative-finance workflow:

[
\boxed{
\text{Model}
\rightarrow
\text{Simulate}
\rightarrow
\text{Price}
\rightarrow
\text{Validate}
}
]

The underlying asset is modeled using geometric Brownian motion under the risk-neutral measure:

[
dS_t=rS_tdt+\sigma S_tdW_t.
]

The European call price is estimated using Monte Carlo:

[
\boxed{
\hat C_N=
e^{-rT}
\frac1N
\sum_{i=1}^N
\max(S_T^{(i)}-K,0)
}
]

and validated against the analytical Black–Scholes formula:

[
\boxed{
C_0=S_0N(d_1)-Ke^{-rT}N(d_2)
}
]

as well as the Black–Scholes PDE:

[
\boxed{
C_t+
\frac12\sigma^2S^2C_{SS}
+rSC_S-rC=0.
}
]

The central numerical lesson is that Monte Carlo pricing is a **statistical estimation problem**. Its accuracy improves as the number of simulations increases, with the characteristic convergence rate

[
O(N^{-1/2}).
]

The central mathematical lesson is that the **stochastic, analytical, and PDE formulations are different representations of the same derivative-pricing problem**.

This makes the project a useful foundation for studying computational finance, stochastic differential equations, numerical PDEs, statistical estimation, and quantitative risk.
