# 🔐 SECURITY GUIDE - MARKET MONTREZOR SYSTEM

## 📋 OVERVIEW

This is an **open-source project** for financial analysis and trading strategies. 
All sensitive data (API keys, credentials, personal data) is properly secured and **never committed** to version control.

---

## 🚨 CRITICAL SECURITY RULES

### ✅ **SAFE TO COMMIT**
- Source code (.py files)
- Documentation (.md files)
- Configuration templates
- Public data and examples
- Test files (without real credentials)

### ❌ **NEVER COMMIT**
- API keys and credentials
- Personal data
- Database connections
- Private certificates
- Environment files with secrets

---

## 🔑 API KEYS MANAGEMENT

### **📁 File Structure**
```
market_montrezor_system/
├── config/
│   ├── api_keys.py          # ⚠️  IN .gitignore - Your real keys
│   └── keys_template.py     # ✅  Template for reference
├── .env                     # ⚠️  IN .gitIGNORE - Environment vars
└── .gitignore              # ✅  Security rules
```

### **🔧 Setup Instructions**

#### **Option 1: Direct File (Development)**
1. Copy the template:
   ```bash
   cp config/keys_template.py config/api_keys.py
   ```

2. Edit `config/api_keys.py`:
   ```python
   # Add your actual API keys
   BINANCE_API_KEY = "your_real_api_key_here"
   GLASSNODE_API_KEY = "your_glassnode_key_here"
   ```

#### **Option 2: Environment Variables (Recommended)**
1. Create `.env` file:
   ```bash
   BINANCE_API_KEY=your_binance_api_key
   BINANCE_SECRET_KEY=your_binance_secret_key
   GLASSNODE_API_KEY=your_glassnode_api_key
   ```

2. Load in your code:
   ```python
   from config.api_keys import APIKeys
   APIKeys.load_from_env()
   ```

---

## 🛡️ .GITIGNORE CONFIGURATION

Your `.gitignore` includes comprehensive security patterns:

### **🔐 Protected Patterns:**
- `config/api_keys.py` - Your real API keys
- `*.key`, `*.pem`, `*.p12` - Certificate files
- `*api_key*`, `*secret*`, `*token*` - Any file with sensitive names
- `data/` - Data files with personal information
- `logs/` - Log files that might contain sensitive data

### **✅ What's Safe:**
- `config/keys_template.py` - Template without real keys
- Source code and documentation
- Test files with mock data

---

## 🔍 HOW TO USE IN YOUR CODE

### **Basic Usage:**
```python
from config.api_keys import APIKeys

# Check if key exists
if APIKeys.BINANCE_API_KEY:
    # Use the API
    print("✅ Binance API key available")
else:
    print("❌ Binance API key missing")

# Load from environment (recommended)
APIKeys.load_from_env()

# Validate required keys
required_keys = ['BINANCE_API_KEY', 'GLASSNODE_API_KEY']
if APIKeys.validate_required_keys(required_keys):
    print("✅ All required keys are set")
```

---

## 🌍 GITHUB & COLLABORATION

### **✅ Safe for Open Source:**
- All source code can be shared
- No sensitive data in repository
- Clear instructions for contributors
- Template files for easy setup

### **🤝 Contributing:**
1. Fork the repository
2. Set up your local `config/api_keys.py`
3. Never commit your keys
4. Submit pull requests with code only

---

## 🔧 ENVIRONMENT VARIABLES SETUP

### **Windows (PowerShell):**
```powershell
$env:BINANCE_API_KEY="your_api_key"
$env:GLASSNODE_API_KEY="your_glassnode_key"
```

### **Linux/MacOS:**
```bash
export BINANCE_API_KEY="your_api_key"
export GLASSNODE_API_KEY="your_glassnode_key"
```

### **.env File:**
```bash
# Create .env file (already in .gitignore)
BINANCE_API_KEY=your_binance_api_key
BINANCE_SECRET_KEY=your_binance_secret_key
GLASSNODE_API_KEY=your_glassnode_api_key
COINGECKO_API_KEY=your_coingecko_key
```

---

## 🚨 SECURITY BEST PRACTICES

### **🔑 API Keys:**
- Use different keys for development/production
- Rotate keys regularly
- Use testnet keys when available
- Never share keys in public forums

### **🌐 Network Security:**
- Use HTTPS endpoints only
- Validate SSL certificates
- Implement rate limiting
- Monitor API usage

### **💾 Data Protection:**
- Encrypt sensitive local data
- Use secure database connections
- Implement proper access controls
- Regular security audits

---

## 📞 SUPPORT & ISSUES

### **🐛 Security Issues:**
- Report security vulnerabilities privately
- Email: security@montrezor.com
- Do NOT open public issues for security problems

### **❓ General Questions:**
- GitHub Issues: Non-sensitive questions
- Documentation: Check this file first
- Setup: Follow the instructions above

---

## 🔍 VERIFICATION CHECKLIST

### **Before Committing:**
- [ ] No real API keys in code
- [ ] No credentials in configuration files
- [ ] No personal data in test files
- [ ] `.env` file exists and is in `.gitignore`
- [ ] `config/api_keys.py` is in `.gitignore`

### **After Setup:**
- [ ] API keys are working
- [ ] Environment variables loading correctly
- [ ] No sensitive data in repository
- [ ] All tests pass with mock data

---

**📝 Maintained by: Igor Montrezor**
**🔄 Last Updated: 2026-04-29**
**📧 Security: security@montrezor.com**

*Keep your keys safe, keep your code open!* 🔐🚀
