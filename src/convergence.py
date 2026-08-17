import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import qmc, norm

def bs_call_price(S0, K, T, r, sigma):
    """Calculates exact analytical Black-Scholes price for error reference."""
    d1 = (np.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

def run_multistep_qmc_experiment(steps, S0, K, T, r, sigma, N_paths=8192):
    """
    Simulates multi-step asset paths using a d-dimensional Sobol sequence.
    Holds the number of paths (N_paths) constant while varying the time steps.
    """
    exact_price = bs_call_price(S0, K, T, r, sigma)
    qmc_errors = []
    
    # Force N_paths strictly to the nearest integer power of 2 using a bitwise shift
    exponent = int(np.ceil(np.log2(N_paths)))
    safe_N_paths = int(1 << exponent)
    
    for num_steps in steps:
        if num_steps <= 0:
            qmc_errors.append(np.nan)
            continue
            
        m = int(num_steps)
        dt = T / m
        
        # 1. Initialize a multidimensional Sobol engine where dimension = number of time steps
        sampler = qmc.Sobol(d=m, scramble=True, seed=42)
        
        # 2. Explicitly cast n to an int type inside the sampler call
        u_samples = sampler.random(n=safe_N_paths) # Shape: (N_paths, m)
        
        # 3. Transform the uniform coordinates into independent standard normal increments
        Z = norm.ppf(u_samples) # Shape: (N_paths, m)
        
        # 4. Simulate the brownian paths sequentially across time steps
        log_drift = (r - 0.5 * sigma**2) * dt
        diffusion = sigma * np.sqrt(dt) * Z
        
        # Cumulative sum across the time steps axis to build the paths
        log_returns = log_drift + diffusion
        cumulative_log_returns = np.sum(log_returns, axis=1)
        
        ST = S0 * np.exp(cumulative_log_returns)
        
        # 5. Calculate payoff and discount to present value
        payoffs = np.maximum(ST - K, 0)
        qmc_price = np.exp(-r * T) * np.mean(payoffs)
        
        qmc_errors.append(abs(qmc_price - exact_price))
        
    return qmc_errors


def convergence(S0=100, K=100, T=1.0, r=0.05, sigma=0.2):
    # Load error CSV files
    mc_path = r'C:\Users\Troy\Downloads\tchin-european-mc-option-pricing-model\src\monte_carlo_errors.csv'
    pde_path = r'C:\Users\Troy\Downloads\tchin-european-mc-option-pricing-model\src\black_scholes_errors.csv'
    
    df_mc = pd.read_csv(mc_path)
    df_pde = pd.read_csv(pde_path)
    
    # Extract the time step array from your CSV data
    steps = df_mc['Time Step'].values
    
    # Run the multidimensional multi-step QMC experiment (using a fixed path budget)
    # Adjust N_paths higher (e.g., 16384) if your original MC paths use a massive path budget
    qmc_errors = run_multistep_qmc_experiment(steps, S0, K, T, r, sigma, N_paths=8192)
    
    # Create log-log plot
    plt.figure(figsize=(10, 7))
    
    # Existing MC and PDE Plots
    plt.loglog(df_mc['Time Step'], df_mc['Left Scheme Error'], marker='o', alpha=0.6, label='Monte Carlo (Left Scheme)')
    plt.loglog(df_mc['Time Step'], df_mc['Right Scheme Error'], marker='o', alpha=0.6, label='Monte Carlo (Right Scheme)')
    plt.loglog(df_mc['Time Step'], df_mc['Midpoint Scheme Error'], marker='o', alpha=0.6, label='Monte Carlo (Midpoint Scheme)')
    plt.loglog(df_pde['Time Step'], df_pde['Absolute Error'], marker='s', alpha=0.8, label='Crank-Nicolson PDE')
    
    # New True Multi-Step Quasi-Monte Carlo Plot
    plt.loglog(steps, qmc_errors, marker='^', color='black', linewidth=2, label='Quasi-Monte Carlo (Multi-step Sobol)')
    
    plt.xlabel('Number of Time Steps [log scale]')
    plt.ylabel('Absolute Error [log scale]')
    plt.title('Log-Log Convergence Curves for Option Pricing (Varying Time Steps)')
    plt.legend()
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    convergence()
