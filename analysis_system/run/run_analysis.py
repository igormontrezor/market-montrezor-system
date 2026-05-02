"""
ANALYSIS SYSTEM - Main Runner
Sistema de análise de mercado
"""

import sys
import os

# Adicionar path para importar config (compartilhado)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main import main

if __name__ == "__main__":
    print("🔍 ANALYSIS SYSTEM - Iniciando...")
    main()
