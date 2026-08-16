import numpy as np

def estimate_gbm_parameters(prices, dt):
    """
    Estimates the drift (mu) and volatility (sigma) parameters of a 
    Geometric Brownian Motion (GBM) model using maximum likelihood estimation.
    """
    # Convert input to numpy array
    prices = np.asarray(prices)
    
    # 1. Compute consecutive log returns
    log_returns = np.log(prices[1:] / prices[:-1])
    
    # 2. Calculate sample mean and variance of log returns
    mean_log_return = np.mean(log_returns)
    var_log_return = np.var(log_returns, ddof=1) # Using sample variance (unbiased)
    
    # 3. Apply MLE formulas to scale parameters by time step dt
    sigma_hat = np.sqrt(var_log_return) / np.sqrt(dt)
    mu_hat = (mean_log_return / dt) + 0.5 * (sigma_hat ** 2)
    
    return mu_hat, sigma_hat

# --- Example Usage ---
if __name__ == "__main__":
    # Simulated daily price data (252 trading days in a year)
    np.random.seed(42)
    true_mu = 0.10       # 10% annual expected return
    true_sigma = 0.20    # 20% annual volatility
    daily_dt = 1 / 252   # Time step
    
    # Generate a realistic sample GBM path
    steps = 252
    shocks = np.random.normal(0, np.sqrt(daily_dt), steps)
    log_price_drifts = (true_mu - 0.5 * true_sigma**2) * daily_dt + true_sigma * shocks
    simulated_prices = 100 * np.exp(np.cumsum(np.insert(log_price_drifts, 0, 0)))

    # Estimate parameters back from the simulated data
    estimated_mu, estimated_sigma = estimate_gbm_parameters(simulated_prices, daily_dt)
    
    print(f"True Annual Drift (mu):      {true_mu:.4f}")
    print(f"Estimated Annual Drift:      {estimated_mu:.4f}")
    print(f"True Annual Volatility (sig): {true_sigma:.4f}")
    print(f"Estimated Annual Volatility: {estimated_sigma:.4f}")

