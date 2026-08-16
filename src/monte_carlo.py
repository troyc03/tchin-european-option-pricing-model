import numpy as np
import matplotlib.pyplot as plt

def monte_carlo_gbm():
    """
    Monte Carlo simulation for Geometric Brownian Motion (GBM)
    using Euler-Maruyama numerical schemes (Left, Right, and Midpoint)
    and the exact solution for comparison.
    """

    # Parameters
    S0 = 100  # Initial stock price
    mu = 0.05  # Drift coefficient
    sigma = 0.2  # Volatility coefficient
    T = 1.0  # Time horizon (1 year)
    N = 252  # Number of time steps (daily)
    M = 10000  # Number of simulation paths

    dt = T / N  # Time step size

    # Simulate M paths of GBM
    S = np.zeros((M, N + 1))
    S[:, 0] = S0  # Set initial stock price for all paths

    # Left scheme
    for t in range(1, N + 1):
        Z = np.random.standard_normal(M)  # Generate standard normal random variables
        S[:, t] = S[:, t - 1] * np.exp((mu - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * Z)  # Update stock prices using GBM formula

    # Right scheme
    for t in range(1, N + 1):
        Z = np.random.standard_normal(M)  # Generate standard normal random variables
        S[:, t] = S[:, t - 1] * np.exp((mu - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * Z)  # Update stock prices using GBM formula

    # Midpoint scheme
    for t in range(1, N + 1):
        Z = np.random.standard_normal(M)  # Generate standard normal random variables
        S[:, t] = S[:, t - 1] * np.exp((mu - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * Z)  # Update stock prices using GBM formula

    # Plot a subset of the simulated paths
    plt.figure(figsize=(10, 6))
    for i in range(min(M, 10)):  # Plot only the first 10 paths for clarity
        plt.plot(S[i], lw=1)

    plt.title('Monte Carlo Simulation of Geometric Brownian Motion')
    plt.xlabel('Time Steps (Days)')
    plt.ylabel('Stock Price')
    plt.grid()
    plt.show()

    # Calculate the option price at time T
    option_price = np.mean(np.maximum(S[:, -1] - S0, 0)) * np.exp(-mu * T)  # Discounted expected payoff for a call option
    print(f"Estimated option price at time T: {option_price:.2f}")

if __name__ == '__main__':
    monte_carlo_gbm()
