import numpy as np 
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D 
from scipy.linalg import solve 
from scipy.stats import norm 
import pandas as pd

class BlackScholesAnalytical: 
    def __init__(self, S, K, T, r, sigma, option_type='call'): 
        self.S = S 
        self.K = K 
        self.T = T 
        self.r = r 
        self.sigma = sigma 
        self.option_type = option_type 
        
    def price(self): 
        d1 = (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T)) 
        d2 = d1 - self.sigma * np.sqrt(self.T) 
        if self.option_type == 'call': 
            return self.S * norm.cdf(d1) - self.K * np.exp(-self.r * self.T) * norm.cdf(d2) 
        else: 
            return self.K * np.exp(-self.r * self.T) * norm.cdf(-d2) - self.S * norm.cdf(-d1) 

class BlackScholesPDE: 
    def __init__(self, S_max, K, T, r, sigma, M, N, option_type='call'): 
        self.S_max = S_max 
        self.K = K 
        self.T = T 
        self.r = r 
        self.sigma = sigma 
        self.M = M 
        self.N = N 
        self.option_type = option_type 
        self.dt = T / N 
        self.dS = S_max / M 
        self.S_values = np.linspace(0, S_max, M + 1) 
        self.t_values = np.linspace(0, T, N + 1) 
        
    def price(self): 
        V_grid = np.zeros((self.M + 1, self.N + 1)) 
        
        if self.option_type == 'call': 
            V_grid[:, -1] = np.maximum(self.S_values - self.K, 0) 
        else: 
            V_grid[:, -1] = np.maximum(self.K - self.S_values, 0) 
            
        A = np.zeros((self.M - 1, self.M - 1)) 
        B = np.zeros((self.M - 1, self.M - 1)) 
        
        for i in range(1, self.M): 
            idx = i - 1 
            alpha = 0.25 * self.dt * (self.sigma**2 * i**2 - self.r * i) 
            beta = -0.5 * self.dt * (self.sigma**2 * i**2 + self.r) 
            gamma = 0.25 * self.dt * (self.sigma**2 * i**2 + self.r * i) 
            
            if idx > 0: 
                A[idx, idx - 1] = -alpha 
            A[idx, idx] = 1 - beta 
            if idx < self.M - 2: 
                A[idx, idx + 1] = -gamma 
                
            if idx > 0: 
                B[idx, idx - 1] = alpha 
            B[idx, idx] = 1 + beta 
            if idx < self.M - 2: 
                B[idx, idx + 1] = gamma 
                
        for n in range(self.N - 1, -1, -1): 
            t_curr = self.t_values[n] 
            if self.option_type == 'call': 
                bound_0_n = 0 
                bound_0_np1 = 0 
                bound_max_n = self.S_max - self.K * np.exp(-self.r * (self.T - t_curr)) 
                bound_max_np1 = self.S_max - self.K * np.exp(-self.r * (self.T - self.t_values[n + 1])) 
            else: 
                bound_0_n = self.K * np.exp(-self.r * (self.T - t_curr)) 
                bound_0_np1 = self.K * np.exp(-self.r * (self.T - self.t_values[n + 1])) 
                bound_max_n = 0 
                bound_max_np1 = 0 
                
            V_grid[0, n] = bound_0_n 
            V_grid[-1, n] = bound_max_n 
            
            D = B @ V_grid[1:-1, n + 1] 
            alpha_first = 0.25 * self.dt * (self.sigma**2 * 1**2 - self.r * 1) 
            gamma_last = 0.25 * self.dt * (self.sigma**2 * (self.M - 1)**2 + self.r * (self.M - 1)) 
            D[0] += alpha_first * (bound_0_n + bound_0_np1) 
            D[-1] += gamma_last * (bound_max_n + bound_max_np1) 
            
            V_grid[1:-1, n] = solve(A, D) 
            
        fig = plt.figure(figsize=(10, 7)) 
        ax = fig.add_subplot(111, projection='3d') 
        T_mesh, S_mesh = np.meshgrid(self.t_values, self.S_values) 
        surf = ax.plot_surface(S_mesh, T_mesh, V_grid, cmap='viridis', edgecolor='none') 
        ax.set_title(f'Black-Scholes 3D Surface ({self.option_type.capitalize()} Option)') 
        ax.set_xlabel('Stock Price (S)') 
        ax.set_ylabel('Time (t)') 
        ax.set_zlabel('Option Value (V)') 
        fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5) 
        plt.show() 
        
        idx = np.argmin(np.abs(self.S_values - self.K)) 
        return V_grid[idx, 0] 

def main(): 
    S, K, T, r, sigma = 100.0, 100.0, 1.0, 0.05, 0.2 
    S_max = 300.0 
    M, N = 200, 10000 
    bs_analytical = BlackScholesAnalytical(S, K, T, r, sigma, 'call') 
    analytical_price = bs_analytical.price() 
    bs_pde = BlackScholesPDE(S_max, K, T, r, sigma, M, N, 'call') 
    numerical_price = bs_pde.price() 
    rel_error = np.abs(analytical_price - numerical_price) / analytical_price 
    print(f'Analytical European Option Price: {analytical_price:.6f}') 
    print(f'Numerical European Option Price: {numerical_price:.6f}') 
    print(f'Relative Error: {rel_error:.6f}') 
    
    error_df = pd.DataFrame({ 
        'Time Step': np.arange(N + 1), 
        'Numerical Price': [numerical_price] * (N + 1),
        'Analytical Price': [analytical_price] * (N + 1),
        'Absolute Error': [abs(analytical_price - numerical_price)] * (N + 1) 
    }) 

    # Save the error DataFrame to a CSV file for further analysis
    error_df.to_csv('black_scholes_errors.csv', index=False)
    print('Dataset saved for further analysis.')

if __name__ == '__main__': 
    main()
