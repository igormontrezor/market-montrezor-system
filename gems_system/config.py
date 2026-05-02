#!/usr/bin/env python3
"""
🔧 Configuração Local - GEMS FINDER
Importa API keys do sistema central
"""

import os
import sys
from typing import Optional

# Adicionar path do sistema central
if '__file__' in globals():
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
else:
    sys.path.append('..')
sys.path.append('../config')

# Importar API keys do arquivo central
try:
    import api_keys
    # Carregar API keys diretamente (já está no arquivo)
    YOUTUBE_API_KEY = api_keys.APIKeys.YOUTUBE_API_KEY
except ImportError:
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY', '')
except Exception as e:
    print(f"Erro ao importar API keys: {e}")
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY', '')

# Configurações do sistema
SOCIAL_CACHE_HOURS = 1
SOCIAL_ANALYSIS_MIN_RATIO = 0.7
SOCIAL_ANALYSIS_MIN_DAYS = 2
