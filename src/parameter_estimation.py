import numpy as np

def parameter_estimation_mle(prices, dt):
    """
    Parameter estimation of Black-Scholes model
    using Maximum Likelihood Estimation.
    """

    # Convert the stock prices to log returns
    S = np.log(prices[1:] / prices[:-1])

    # Estimate the drift (mu) and volatility (sigma)
    mu = np.mean(S) / dt
    sigma = np.std(S) / np.sqrt(dt)

    # Calculate the log-likelihood of the observed data given the estimated parameters
    log_likelihood = -0.5 * len(S) * np.log(2 * np.pi * sigma**2) - np.sum((S - mu * dt)**2) / (2 * sigma**2)

    # Return the estimated parameters and log-likelihood
    return mu, sigma, log_likelihood

if __name__ == '__main__':
    # Define true parameters for simulation
    true_mu = 0.05
    true_sigma = 0.2
    S0 = 100  # Initial stock price
    T = 1.0  # Time horizon (1 year)
    N = 252  # Number of time steps (daily)

    # Calculate path returns using Geometric Brownian Motion
    dt = T / N
    np.random.seed(42)  # For reproducibility
    Z = np.random.standard_normal(N)  # Generate standard normal random variables

    prices = S0 * np.exp(np.cumsum((true_mu - 0.5 * true_sigma**2) * dt + true_sigma * np.sqrt(dt) * Z))

    # Estimate parameters using MLE
    estimated_mu, estimated_sigma, log_likelihood = parameter_estimation_mle(prices, dt)

    # Print the results
    print(f"True mu: {true_mu}, Estimated mu: {estimated_mu:.3f}")
    print(f"True sigma: {true_sigma}, Estimated sigma: {estimated_sigma:.3f}")
    print(f"Log-likelihood: {log_likelihood:.4f}")


