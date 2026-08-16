import numpy as np
import matplotlib.pyplot as plt
from black_scholes import BlackScholesAnalytical, BlackScholesPDE

def monte_carlo_gbm(S0=100.0, r=0.05, sigma=0.2, T=1.0, N=252, M=10):
    dt = T / N
    t = np.linspace(0, T, N + 1)
    Z = np.random.normal(0, 1, (N, M))
    
    # Calculate daily drift and shocks
    drift = (r - 0.5 * sigma**2) * dt
    shock = sigma * np.sqrt(dt) * Z
    
    # Initialize price matrix with starting stock price S0
    price_paths = np.zeros((N + 1, M))
    price_paths[0] = S0
    
    # Compute price paths by vectorizing the cumulative sum of logs
    price_paths[1:] = S0 * np.exp(np.cumsum(drift + shock, axis=0))
    return t, price_paths

def analyze_and_plot_paths(t, price_paths, r, T, K=100.0):
    """
    Calculates expected final values, European option prices, 
    and plots the simulated asset trajectories.
    """
    # 1. Extract final prices at expiration (last row)
    final_prices = price_paths[-1]
    
    # 2. Calculate financial metrics
    expected_final_value = np.mean(final_prices)
    
    # Calculate payoffs at expiration
    call_payoffs = np.maximum(final_prices - K, 0)
    put_payoffs = np.maximum(K - final_prices, 0)
    
    # Discount payoffs back to present value using risk-free rate
    call_price = np.exp(-r * T) * np.mean(call_payoffs)
    
    # Print metrics neatly
    print(f"European Call Price: ${call_price:.2f}")
    
    # 3. Plotting function
    plt.figure(figsize=(10, 6))
    plt.plot(t, price_paths, linewidth=1.5)
    plt.axhline(K, color='red', linestyle='--', label=f'Strike Price (K={K})')
    plt.title(f'Monte Carlo Geometric Brownian Motion - {price_paths.shape[1]} Paths')
    plt.xlabel('Time (Years)')
    plt.ylabel('Asset Price ($)')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend()
    plt.show()

# --- Execution Example ---
t, paths = monte_carlo_gbm(S0=100.0, r=0.05, sigma=0.20, T=1.0, N=252, M=1000)
analyze_and_plot_paths(t, paths, r=0.05, T=1.0, K=100.0)




