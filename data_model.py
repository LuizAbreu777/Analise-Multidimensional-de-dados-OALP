# data_model.py

from collections import defaultdict
import random
import numpy as np

class OLAPModel:
    # 1. REMOVIDO: min_valor_seed e max_valor_seed do __init__
    def __init__(self, dimensions, facts, filters):
        self.dimensions = dimensions
        self.facts = facts
        self.filters = filters
    
    def generate_sample_data(self):
        """Gera dimensões e fatos de exemplo (seed) usando valores fixos internos."""
        
        # Valores Mínimo/Máximo fixos
        min_valor = 50.0  # Valor padrão fixo
        max_valor = 500.0 # Valor padrão fixo
        
        # 1. Dimensões de Exemplo
        self.dimensions.clear()
        self.dimensions.update({
            "PRODUTO": ["CAMISA", "CALÇA", "TENIS", "BERMUDA"],
            "REGIÃO": ["NORTE", "SUL", "LESTE", "OESTE", "CENTRO"],
            "MÊS": ["JAN", "FEV", "MAR", "ABR", "MAI"]
        })
        
        # 2. Fatos de Exemplo 
        self.facts.clear()
        num_facts = 75
        
        for i in range(num_facts):
            fact = {}
            for dim_name, dim_values in self.dimensions.items():
                fact[dim_name] = random.choice(dim_values)
                
            # Geração de valor usando os valores fixos internos
            fact["valor"] = round(random.uniform(min_valor, max_valor), 2)
            self.facts.append(fact)
            
        return len(self.facts)

    def aggregate_data(self, dims, measure):
        """Aplica filtro, agrupa e calcula a medida (sum, avg, count)."""
        
        # 1. Aplica o filtro (Slice)
        filtered_facts = [f for f in self.facts if all(f[dim] == val for dim, val in self.filters.items())]

        if not filtered_facts:
            return None, "Nenhum fato corresponde aos filtros e/ou dimensões selecionadas."

        # 2. Agrupar dados
        data = defaultdict(list)
        for f in filtered_facts:
            key = tuple(f[d] for d in dims)
            data[key].append(f["valor"])
            
        # 3. Calcular a Medida
        if measure == "sum":
            result = {k: sum(v) for k,v in data.items()}
        elif measure == "avg":
            result = {k: sum(v)/len(v) for k,v in data.items()}
        else: # count
            result = {k: len(v) for k,v in data.items()}
            
        return result, None