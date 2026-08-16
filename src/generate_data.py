import numpy as np
import pandas as pd
import yfinance as yf

data = yf.download("AAPI", period='max')
data.to_csv("aapi_stock_data.csv")

print('Dataset generated!')