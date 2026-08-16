import numpy as np
import matplotlib.pyplot as plt

def monte_carlo_gbm():
    # Parameters
    S0 = 100       # Initial stock price
    mu = 0.05      # Drift coefficient
    sigma = 0.2    # Volatility coefficient
    T = 1.0        # Time horizon (1 year)
    N = 252        # Number of time steps (daily)
    M = 10000      # Number of simulation paths
    dt = T / N     # Time step size

    # Initialize path arrays for each scheme
    S_exact = np.zeros((M, N + 1))
    S_left  = np.zeros((M, N + 1))
    S_right = np.zeros((M, N + 1))
    S_mid   = np.zeros((M, N + 1))

    # Set initial prices
    S_exact[:, 0] = S_left[:, 0] = S_right[:, 0] = S_mid[:, 0] = S0

    # Common random increments for consistent comparison across schemes
    # Shape: (M, N) -> rows are paths, columns are time steps
    Z = np.random.standard_normal((M, N))
    dW = Z * np.sqrt(dt)

    # Time-stepping loop
    for t in range(1, N + 1):
        dw_t = dW[:, t - 1]
        
        # 1. Exact Analytical Solution
        S_exact[:, t] = S_exact[:, t - 1] * np.exp((mu - 0.5 * sigma ** 2) * dt + sigma * dw_t)
        
        # 2. Left Euler-Maruyama Scheme (Standard Forward Euler)
        # Evaluates drift and diffusion coefficients at the start of the interval (t-1)
        S_left[:, t] = S_left[:, t - 1] + mu * S_left[:, t - 1] * dt + sigma * S_left[:, t - 1] * dw_t
        
        # 3. Right Euler-Maruyama Scheme (Implicit Backward Euler)
        # Evaluates drift at the end of the interval (t), diffusion stays at the start (t-1) for Ito calculus
        S_right[:, t] = (S_right[:, t - 1] + sigma * S_right[:, t - 1] * dw_t) / (1 - mu * dt)
        
        # 4. Midpoint Euler-Maruyama Scheme (Stratonovich-like structure)
        # Evaluates the deterministic drift at the average of the step boundaries
        S_mid_predict = S_mid[:, t - 1] + 0.5 * mu * S_mid[:, t - 1] * dt + 0.5 * sigma * S_mid[:, t - 1] * dw_t
        S_mid[:, t] = S_mid[:, t - 1] + mu * S_mid_predict * dt + sigma * S_mid[:, t - 1] * dw_t

    # Plotting first 5 paths of the exact solution
    plt.figure(figsize=(10, 6))
    for i in range(5): 
        plt.plot(S_exact[i], lw=1, label=f'Path {i+1}' if i==0 else "")
    plt.title("Monte Carlo Simulation of Geometric Brownian Motion (Exact Paths)")
    plt.xlabel("Time Steps (Days)")
    plt.ylabel("Stock Price")
    plt.grid(True)
    plt.show()

    # Calculate and print European Call Option Prices
    # Discount factor uses the risk-free rate (assumed to be mu here)
    discount = np.exp(-mu * T)
    
    price_exact = np.mean(np.maximum(S_exact[:, -1] - S0, 0)) * discount
    price_left  = np.mean(np.maximum(S_left[:, -1] - S0, 0)) * discount
    price_right = np.mean(np.maximum(S_right[:, -1] - S0, 0)) * discount
    price_mid   = np.mean(np.maximum(S_mid[:, -1] - S0, 0)) * discount

    print(f"Estimated Call Option Prices (M={M}, N={N}):")
    print(f"  Exact Solution:  {price_exact:.4f}")
    print(f"  Left Scheme:     {price_left:.4f}")
    print(f"  Right Scheme:    {price_right:.4f}")
    print(f"  Midpoint Scheme: {price_mid:.4f}")

    # Calculate and print a table of errors between the schemes and the exact solution
    errors_left = []
    errors_right = []
    errors_mid = []

    for t in range(N + 1):
        error_left = np.mean(np.abs(S_left[:, t] - S_exact[:, t]))
        error_right = np.mean(np.abs(S_right[:, t] - S_exact[:, t]))
        error_mid = np.mean(np.abs(S_mid[:, t] - S_exact[:, t]))

        errors_left.append(error_left)
        errors_right.append(error_right)
        errors_mid.append(error_mid)

    # Print the error table
    print("\nAverage Absolute Errors at Each Time Step:")
    print(f"{'Time Step':<10} {'Left Scheme':<15} {'Right Scheme':<15} {'Midpoint Scheme':<15}")
    for t in range(N + 1):
        print(f"{t:<10} {errors_left[t]:<15.6f} {errors_right[t]:<15.6f} {errors_mid[t]:<15.6f}")

    # Save as a CSV file for further analysis
    import pandas as pd

    error_df = pd.DataFrame({
        'Time Step': np.arange(N + 1),
        'Left Scheme Error': errors_left,
        'Right Scheme Error': errors_right,
        'Midpoint Scheme Error': errors_mid
    })


    error_df.to_csv('monte_carlo_errors.csv', index=False)

    print('Saved MC error dataset for analysis.')

if __name__ == "__main__":
    monte_carlo_gbm()
