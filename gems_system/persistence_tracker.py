import json
import os
from datetime import datetime
from typing import Dict, List, Any

class PersistenceTracker:
    """Rastreador de persistência cumulativa"""
    
    def __init__(self):
        self.persistence_file = "data/persistence_tracker.json"
        self.load_persistence_data()
    
    def load_persistence_data(self):
        """Carrega dados acumulados de persistência"""
        if os.path.exists(self.persistence_file):
            with open(self.persistence_file, 'r') as f:
                self.persistence_data = json.load(f)
        else:
            self.persistence_data = {}
    
    def save_persistence_data(self):
        """Salva dados acumulados de persistência"""
        os.makedirs(os.path.dirname(self.persistence_file), exist_ok=True)
        with open(self.persistence_file, 'w') as f:
            json.dump(self.persistence_data, f, indent=2)
    
    def update_persistence_counts(self, gems: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Atualiza contadores de persistência para cada gem"""
        
        today = datetime.now().strftime('%Y%m%d')
        
        for gem in gems:
            symbol = gem['symbol']
            persistence_days = gem.get('persistence_days', 0)
            
            # Inicializar dados da gem se não existir
            if symbol not in self.persistence_data:
                self.persistence_data[symbol] = {
                    'count_3d': 0,
                    'count_7d': 0,
                    'count_14d': 0,
                    'first_seen': today,
                    'last_seen': today,
                    'max_persistence': 0
                }
            
            # Atualizar contadores com base na persistência atual
            gem_data = self.persistence_data[symbol]
            
            # Se atingiu 3+ dias, incrementa contador de 3 dias
            if persistence_days >= 3:
                if gem_data['max_persistence'] < 3:  # Primeira vez atingindo 3 dias
                    gem_data['count_3d'] += 1
            
            # Se atingiu 7+ dias, incrementa contador de 7 dias
            if persistence_days >= 7:
                if gem_data['max_persistence'] < 7:  # Primeira vez atingindo 7 dias
                    gem_data['count_7d'] += 1
            
            # Se atingiu 14+ dias, incrementa contador de 14 dias
            if persistence_days >= 14:
                if gem_data['max_persistence'] < 14:  # Primeira vez atingindo 14 dias
                    gem_data['count_14d'] += 1
            
            # Atualizar dados gerais
            gem_data['last_seen'] = today
            gem_data['max_persistence'] = max(gem_data['max_persistence'], persistence_days)
            
            # Adicionar colunas ao gem para CSV
            gem['persistence_count_3d'] = gem_data['count_3d']
            gem['persistence_count_7d'] = gem_data['count_7d']
            gem['persistence_count_14d'] = gem_data['count_14d']
            gem['first_seen'] = gem_data['first_seen']
            gem['max_persistence_ever'] = gem_data['max_persistence']
        
        # Salvar dados atualizados
        self.save_persistence_data()
        
        return gems
    
    def get_persistence_score(self, gem: Dict[str, Any]) -> float:
        """Calcula score de persistência cumulativa"""
        
        # Score baseado nos contadores cumulativos
        score_3d = gem.get('persistence_count_3d', 0) * 1.0   # 1 ponto por vez que atingiu 3 dias
        score_7d = gem.get('persistence_count_7d', 0) * 2.0   # 2 pontos por vez que atingiu 7 dias
        score_14d = gem.get('persistence_count_14d', 0) * 3.0 # 3 pontos por vez que atingiu 14 dias
        
        return score_3d + score_7d + score_14d
