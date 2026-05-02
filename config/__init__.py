"""
Configuration module for Market Montrezor System
"""

try:
    from .api_keys import APIKeys
except ImportError:
    from .keys_template import APIKeys

__all__ = ['APIKeys']
