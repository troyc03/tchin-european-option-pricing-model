import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def convergence(S0=100, K=100, T=1.0, r=0.05, sigma=0.2):
    # Load error CSV files (adjust paths as needed)
    df_mc = pd.read_csv(r'C:\Users\Troy\Downloads\tchin-european-mc-option-pricing-model\src\monte_carlo_errors.csv')
    df_pde = pd.read_csv(r'C:\Users\Troy\Downloads\tchin-european-mc-option-pricing-model\src\black_scholes_errors.csv')

    # Create log-log plot
    plt.figure(figsize=(8, 6))
    
    plt.loglog(df_mc['Time Step'], df_mc['Left Scheme Error'], marker='o', label='Monte Carlo (Left Scheme)')
    plt.loglog(df_mc['Time Step'], df_mc['Right Scheme Error'], marker='o', label='Monte Carlo (Right Scheme)')
    plt.loglog(df_mc['Time Step'], df_mc['Midpoint Scheme Error'], marker='o', label='Monte Carlo (Midpoint Scheme)')
    plt.loglog(df_pde['Time Step'], df_pde['Absolute Error'], marker='s', label='Crank-Nicolson PDE')

    plt.xlabel('Number of Steps / Paths (log scale)')
    plt.ylabel('Absolute Error (log scale)')
    plt.title('Log-Log Convergence Curves for Option Pricing')
    plt.legend()
    plt.grid(True, which="both", ls="--")
    plt.show()

if __name__ == '__main__':
    convergence()
