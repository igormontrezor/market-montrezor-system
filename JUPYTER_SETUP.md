# JUPYTER NOTEBOOK SETUP GUIDE

## Environment Ready! 

Your virtual environment is now configured with Jupyter support.

## Quick Start

### 1. Start Jupyter Notebook
```bash
# Activate environment and start Jupyter
.venv\Scripts\activate
jupyter notebook

# Or in one command (Windows)
cmd /c ".venv\Scripts\activate.bat && jupyter notebook"
```

### 2. Start Jupyter Lab (Recommended)
```bash
.venv\Scripts\activate
jupyter lab
```

### 3. Start with specific port
```bash
# Port 8888 (default)
jupyter notebook --port=8888

# No browser auto-open
jupyter notebook --no-browser

# Custom port
jupyter notebook --port=9999
```

## Available Kernels

Your system has these Jupyter kernels available:

1. **python3** (Project Virtual Environment)
   - Path: `C:\market_montrezor_system\.venv\share\jupyter\kernels\python3`
   - **USE THIS ONE** for your project!

2. **data_scientist_1** (Global Environment)
   - Path: `C:\Users\Montrezor-Note01\AppData\Roaming\jupyter\kernels\data_scientist_1`

## Using Your Project in Jupyter

### Option 1: Navigate to Project Directory
```bash
cd C:\market_montrezor_system
.venv\Scripts\activate
jupyter notebook
```

### Option 2: Create New Notebook
1. Open Jupyter
2. Select **"New"** > **"python3"** (your virtual environment)
3. Import your project:

```python
# Test if everything works
import sys
sys.path.append('./src')

from market_analyze import Crypto, YahooProvider, Rsi, ChartPlotter
import pandas as pd

print("Environment ready! All imports successful.")
```

### Option 3: Open Existing Notebooks
```bash
# Navigate to notebooks folder
cd notebooks
jupyter notebook

# Open your existing notebooks
# - market_analysis_oop.ipynb
# - market_analysis_month copy.ipynb
# - market_analysis_week.ipynb
```

## Testing Your Setup

### Quick Test Notebook
Create a new notebook and run:

```python
# Test imports
import sys
sys.path.append('./src')

from market_analyze import Crypto, YahooProvider, Rsi, ChartPlotter
import pandas as pd
import numpy as np
import plotly.graph_objects as go

print("All imports successful!")

# Quick test
provider = YahooProvider(period="1mo", interval="1d")
btc = Crypto("BTC-USD", provider=provider)
print(f"BTC data loaded: {len(btc.get_prices())} rows")

# Test plotting
rsi = Rsi(period=14)
rsi_values = rsi.calculate(btc)
print(f"RSI calculated: {rsi_values.iloc[-1]:.2f}")

print("Setup complete! Ready for analysis!")
```

## Kernel Configuration

### Create Custom Kernel Name (Optional)
```bash
# Create kernel with project name
python -m ipykernel install --user --name=market-montrezor --display-name="Market Montrezor"

# List kernels
jupyter kernelspec list

# Remove kernel if needed
jupyter kernelspec uninstall market-montrezor
```

## Troubleshooting

### Kernel Not Found
```bash
# Reinstall kernel
python -m ipykernel install --user --name=python3

# Check kernel list
jupyter kernelspec list
```

### Import Errors
```python
# Add src to path in notebook
import sys
sys.path.append('./src')

# Test individual imports
from market_analyze.assets import Crypto
from market_analyze.indicators import Rsi
from market_analyze.plotting import ChartPlotter
```

### Port Already in Use
```bash
# Find process using port
netstat -ano | findstr :8888

# Kill process (replace PID)
taskkill /PID <PID> /F

# Use different port
jupyter notebook --port=8889
```

## Advanced Usage

### Jupyter Lab (Modern Interface)
```bash
jupyter lab
```

### Jupyter Notebook Extensions
```bash
# Install extensions
pip install jupyter_contrib_nbextensions
jupyter contrib nbextension install --user

# Enable extensions
jupyter nbextension enable codefolding/main
jupyter nbextension enable execute_time/ExecuteTime
```

## Project Structure for Jupyter

```
market-montrezor-system/
|
|-- notebooks/                    # Your Jupyter notebooks
|   |-- analysis.ipynb            # New analysis notebooks
|   |-- backtesting.ipynb         # Strategy testing
|   |-- visualization.ipynb       # Chart experiments
|
|-- src/                          # Source code
|-- .venv/                        # Virtual environment
```

## Best Practices

1. **Always use the virtual environment kernel** (`python3`)
2. **Add `sys.path.append('./src')`** at the top of notebooks
3. **Save notebooks in the `notebooks/` folder**
4. **Use meaningful names** for analysis notebooks
5. **Document your analysis** with markdown cells

## Ready to Go!

Your environment is now fully configured for:
- **Data analysis** with pandas and numpy
- **Financial modeling** with yfinance
- **Interactive plotting** with plotly
- **Technical indicators** from your custom library
- **Trading signals** and strategy testing

**Start Jupyter and begin your analysis!**
