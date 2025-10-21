# visualizer.py

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.cm as cm 
import matplotlib.colors as colors 

def visualize_result(dims, result, measure, filters=None):
    """
    Cria e exibe o gráfico (1D, 2D ou 3D) a partir do resultado da agregação.
    
    Args:
        dims (list): Lista de nomes das dimensões usadas na agregação.
        result (dict): Dicionário com os resultados da agregação.
        measure (str): A medida calculada (e.g., 'sum', 'avg', 'count').
        filters (dict, optional): Dicionário de filtros ativos, para incluir no título.
    """

    plt.close('all') 

    # Base para o título, pode ser estendido com filtros
    title_base = f"{measure.upper()} por {', '.join(dims)}"
    if filters and any(filters.values()):
        filter_str = ', '.join([f"{d}: {v}" for d, v in filters.items() if v != "TODOS"])
        if filter_str:
            title_base += f"\n(Filtros: {filter_str})"

    # --- 1D Plot: Gráfico de Barras ---
    if len(dims) == 1:
        labels = [str(k) if isinstance(k, tuple) else k for k in result.keys()]
        values = list(result.values())

        fig, ax = plt.subplots(figsize=(10, 7))
        
        colors = plt.cm.viridis(np.linspace(0, 1, len(labels))) 
        bars = ax.bar(labels, values, color=colors)

        ax.set_title(title_base, fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel(dims[0], fontsize=13, labelpad=10)
        ax.set_ylabel(measure.upper(), fontsize=13, labelpad=10)
        
        ax.tick_params(axis='x', rotation=45, ha='right', labelsize=10)
        ax.tick_params(axis='y', labelsize=10)
        
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:,.2f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3), 
                        textcoords="offset points",
                        ha='center', va='bottom',
                        fontsize=9, color='gray')

        plt.grid(axis='y', linestyle='--', alpha=0.7) 
        plt.tight_layout()
        plt.show()
        
    # --- 2D Plot: Mapa de Calor (Heatmap) ---
    elif len(dims) == 2:
        dim0_values = sorted(list({k[0] for k in result.keys()}))
        dim1_values = sorted(list({k[1] for k in result.keys()}))
        
        data_matrix = np.zeros((len(dim0_values), len(dim1_values)))
        for i, val0 in enumerate(dim0_values):
            for j, val1 in enumerate(dim1_values):
                data_matrix[i, j] = result.get((val0, val1), 0) 

        fig, ax = plt.subplots(figsize=(12, 9)) 
        
        # ALTERAÇÃO PRINCIPAL: Trocado para 'magma'
        cmap = 'magma' 
        im = ax.imshow(data_matrix, cmap=cmap, aspect='auto', origin='lower') 
        
        # Rótulos dos eixos
        ax.set_xticks(np.arange(len(dim1_values)))
        ax.set_yticks(np.arange(len(dim0_values)))
        ax.set_xticklabels(dim1_values, rotation=45, ha='right', fontsize=10)
        ax.set_yticklabels(dim0_values, fontsize=10)
        
        ax.set_xlabel(dims[1], fontsize=13, labelpad=10)
        ax.set_ylabel(dims[0], fontsize=13, labelpad=10)
        ax.set_title(title_base, fontsize=16, fontweight='bold', pad=20)
        
        # Lógica de Contraste (Mantida, pois é essencial para UX)
        cmap_obj = cm.get_cmap(cmap)
        
        for i in range(len(dim0_values)):
            for j in range(len(dim1_values)):
                value = data_matrix[i, j]
                
                norm_value = (value - data_matrix.min()) / (data_matrix.max() - data_matrix.min() + 1e-9)
                
                rgb_color = cmap_obj(norm_value)[:3] 
                
                # Calcula a luminância para escolher a cor do texto
                luminance = np.dot(rgb_color, [0.299, 0.587, 0.114])
                
                text_color = "black" if luminance > 0.5 else "white" 
                
                # Adicionar valores nas células (negrito e contraste)
                ax.text(j, i, f'{value:,.0f}',
                        ha="center", va="center", color=text_color, fontsize=10, fontweight='bold')

        cbar = fig.colorbar(im, ax=ax, shrink=0.7, pad=0.02)
        cbar.set_label(f"{measure.upper()} da Medida", rotation=-90, labelpad=15, fontsize=12)
        
        plt.tight_layout()
        plt.show()
            
    # --- 3D Plot: Gráfico de Dispersão 3D ---
    elif len(dims) == 3:
        fig = plt.figure(figsize=(14, 10)) 
        ax = fig.add_subplot(111, projection='3d')
        
        dim1_values = sorted(list({k[0] for k in result.keys()}))
        dim2_values = sorted(list({k[1] for k in result.keys()}))
        dim3_values = sorted(list({k[2] for k in result.keys()}))

        dim1_map = {v: i for i, v in enumerate(dim1_values)}
        dim2_map = {v: i for i, v in enumerate(dim2_values)}
        dim3_map = {v: i for i, v in enumerate(dim3_values)}

        xs, ys, zs, vals = [], [], [], []
        for (a,b,c), v in result.items():
            xs.append(dim1_map[a])
            ys.append(dim2_map[b])
            zs.append(dim3_map[c])
            vals.append(v)
        
        vals_array = np.array(vals)
        
        if vals:
            norm_vals = (vals_array - vals_array.min()) / (vals_array.max() - vals_array.min() + 1e-9)
            point_sizes = 100 + norm_vals * 400 
            
            scatter = ax.scatter(xs, ys, zs, 
                                 s=point_sizes,       
                                 c=vals_array,        
                                 cmap='plasma',       
                                 alpha=0.8,           
                                 marker='o',          
                                 edgecolors='w',      
                                 linewidth=0.5)

            cbar = fig.colorbar(scatter, shrink=0.6, aspect=20, pad=0.08) 
            cbar.set_label(f"{measure.upper()} da Medida", rotation=-90, labelpad=18, fontsize=12)

        ax.set_title(title_base, fontsize=16, fontweight='bold', pad=30) 
        
        ax.set_xlabel(f"{dims[0]}", fontsize=13, labelpad=15)
        ax.set_ylabel(f"{dims[1]}", fontsize=13, labelpad=15)
        ax.set_zlabel(f"{dims[2]}", fontsize=13, labelpad=15) 
        
        ax.set_xticks(list(dim1_map.values()))
        ax.set_xticklabels(dim1_values, rotation=20, ha='right', fontsize=9) 
        
        ax.set_yticks(list(dim2_map.values()))
        ax.set_yticklabels(dim2_values, rotation=-20, ha='left', fontsize=9) 
        
        ax.set_zticks(list(dim3_map.values()))
        ax.set_zticklabels(dim3_values, rotation=90, va='center', fontsize=9)

        if vals:
            for x, y, z, v in zip(xs, ys, zs, vals):
                ax.text(x, y, z + 0.1, f'{v:,.0f}', color='black', size=8, ha='center', va='bottom', weight='bold') 
        
        ax.view_init(elev=20, azim=-60) 
        
        plt.tight_layout()
        plt.show()