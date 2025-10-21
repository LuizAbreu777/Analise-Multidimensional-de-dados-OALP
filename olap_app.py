# olap_app.py

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime

# Importa os módulos externos (Certifique-se de que data_model.py e visualizer.py estão na mesma pasta)
from data_model import OLAPModel
from visualizer import visualize_result 

class OLAPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Análise Multidimensional de Vendas (OLAP)")
        self.root.geometry("1400x850") 
        
        # Configuração de Estilo
        style = ttk.Style()
        style.theme_use('clam') 
        style.configure('TFrame', background='#e0e0e0')
        style.configure('TLabelFrame', background='#e0e0e0', font=('Arial', 11, 'bold'))
        style.configure('TButton', font=('Arial', 10, 'bold'), padding=5)
        
        style.configure('Accent.TButton', foreground='white', background='#2c3e50', font=('Arial', 10, 'bold'))
        style.map('Accent.TButton', 
                  foreground=[('active', 'white'), ('!disabled', 'white')],
                  background=[('active', '#3498db'), ('!disabled', '#2c3e50')])
        
        self.root.configure(bg="#e0e0e0")

        # Variáveis de Estado (AGORA FINALMENTE SEM MIN/MAX)
        self.dimensions = {} 
        self.facts = [] 
        self.filters = {} 
        
        # Inicializa o Modelo de Dados (Chamada simplificada, conforme data_model.py)
        self.model = OLAPModel(self.dimensions, self.facts, self.filters) 

        self.create_widgets()

    def create_widgets(self):
        # Título Principal
        tk.Label(self.root, text="Análise Multidimensional de Vendas (OLAP)", 
                 font=("Arial", 24, "bold"), bg="#e0e0e0", fg="#2c3e50").pack(pady=10)

        # 1. Notebook (Abas) para Organização Principal
        notebook = ttk.Notebook(self.root)
        notebook.pack(pady=5, padx=10, fill="both", expand=True)

        # ----------------------------------------------------------------------
        # --- A. Aba de ENTRADA DE DADOS (Configuração e Fatos) ---
        # ----------------------------------------------------------------------
        tab_data_entry = ttk.Frame(notebook, padding="15 15 15 15")
        notebook.add(tab_data_entry, text='❶ Dados e Cubo', padding=10)
        tab_data_entry.columnconfigure(0, weight=1)

        # Agrupamento: Dimensões (Passo 1)
        frame_dim = ttk.LabelFrame(tab_data_entry, text="1. Definição de Dimensões", padding=15)
        frame_dim.grid(row=0, column=0, sticky="ew", pady=10)
        frame_dim.columnconfigure(1, weight=1) 
        
        ttk.Label(frame_dim, text="Nome da Dimensão:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.entry_dim = ttk.Entry(frame_dim, width=20)
        self.entry_dim.grid(row=0, column=1, padx=5, sticky="we")
        
        ttk.Label(frame_dim, text="Valores (vírgula):").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.entry_values = ttk.Entry(frame_dim)
        self.entry_values.grid(row=1, column=1, padx=5, sticky="we")
        
        ttk.Button(frame_dim, text="➕ Adicionar Dimensão", command=self.add_dimension, style='Accent.TButton').grid(row=2, column=0, columnspan=2, pady=10, sticky="we")

        # Agrupamento: Fatos (Passo 2)
        self.frame_facts = ttk.LabelFrame(tab_data_entry, text="2. Inserção de Fatos (Registros de Vendas)", padding=15)
        self.frame_facts.grid(row=1, column=0, sticky="ew", pady=10)
        self.frame_facts.columnconfigure(1, weight=1)
        self.fact_entries = {}
        self.refresh_fact_inputs() 

        ttk.Label(self.frame_facts, text="Valor da Venda (Medida):").grid(row=99, column=0, sticky="w", pady=5, padx=5)
        self.entry_value = ttk.Entry(self.frame_facts)
        self.entry_value.grid(row=99, column=1, padx=5, sticky="we")
        
        ttk.Button(self.frame_facts, text="➕ Adicionar Fato", command=self.add_fact, style='Accent.TButton').grid(row=100, column=0, columnspan=2, pady=10, sticky="we")

        # Agrupamento: Gestão do Cubo e Seed (Passo 3 - SIMPLIFICADO)
        frame_io = ttk.LabelFrame(tab_data_entry, text="3. Gestão e Geração de Dados", padding=15)
        frame_io.grid(row=2, column=0, sticky="ew", pady=10)
        
        # Configuração de 3 colunas
        frame_io.columnconfigure(0, weight=1)
        frame_io.columnconfigure(1, weight=1)
        frame_io.columnconfigure(2, weight=1) 

        # Linha de Botões (3 botões principais na linha 0)
        ttk.Button(frame_io, text="💾 Salvar Cubo", command=self.save_cube).grid(row=0, column=0, padx=5, pady=5, sticky="we")
        ttk.Button(frame_io, text="📂 Carregar Cubo", command=self.load_cube).grid(row=0, column=1, padx=5, pady=5, sticky="we")
        
        # Botão de Seed (com destaque)
        ttk.Button(frame_io, text="🌱 Gerar Dados de Exemplo (Seed)", command=self.generate_sample_data, style='Accent.TButton').grid(row=0, column=2, padx=5, pady=5, sticky="we") 

        # ----------------------------------------------------------------------
        # --- B. Aba de ANÁLISE (Filtros, Agregação e Log) ---
        # ----------------------------------------------------------------------
        tab_analysis = ttk.Frame(notebook, padding="15 15 15 15")
        notebook.add(tab_analysis, text='❷ Análise e Relatório', padding=10)
        tab_analysis.columnconfigure(0, weight=1)
        tab_analysis.columnconfigure(1, weight=3) # Coluna de resultados mais larga
        tab_analysis.rowconfigure(0, weight=1) 

        # Coluna 0: Filtro e Agregação (Controles)
        control_frame = ttk.Frame(tab_analysis)
        control_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
        control_frame.columnconfigure(0, weight=1)

        # Agrupamento: Filtro (Slice & Dice - Passo 4)
        self.frame_filter = ttk.LabelFrame(control_frame, text="4. Filtro (Slice & Dice)", padding=15)
        # O pack() foi mantido aqui pois está no frame_control e não conflita com o grid interno.
        self.frame_filter.pack(fill="x", pady=10) 
        self.frame_filter.columnconfigure(1, weight=1)
        self.filter_combos = {} 
        self.refresh_filter_inputs() 

        # CORREÇÃO CRÍTICA DO LAYOUT: Usar grid no botão de filtro para evitar conflito com os combos
        ttk.Button(self.frame_filter, text="🔄 Aplicar Filtros", command=self.update_filters, style='Accent.TButton').grid(row=99, column=0, columnspan=2, pady=10, padx=5, sticky="we")

        # Agrupamento: Agregação (Roll-up / Drill-down - Passo 5)
        frame_agg = ttk.LabelFrame(control_frame, text="5. Agregação e Visualização", padding=15)
        frame_agg.pack(fill="x", pady=10)
        frame_agg.columnconfigure(1, weight=1)

        # NOTA DE MELHORIA: Dimensões (1 a 3, vírgula) deve ser entendido como NOME_DA_DIMENSÃO
        ttk.Label(frame_agg, text="Dimensões (NOMES, vírgula):").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.entry_agg_dims = ttk.Entry(frame_agg)
        self.entry_agg_dims.grid(row=0, column=1, padx=5, sticky="we")
        
        ttk.Label(frame_agg, text="Medida:").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.combo_measure = ttk.Combobox(frame_agg, values=["sum","avg","count"], state="readonly", width=10)
        self.combo_measure.current(0)
        self.combo_measure.grid(row=1, column=1, padx=5, sticky="we")
        
        ttk.Button(frame_agg, text="📊 Agregar e Plotar", command=self.aggregate, style='Accent.TButton').grid(row=2, column=0, columnspan=2, pady=10, sticky="we")


        # Coluna 1: Resultados / Log
        frame_result = ttk.LabelFrame(tab_analysis, text="Log e Resultados da Agregação", padding=10)
        frame_result.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)
        frame_result.columnconfigure(0, weight=1)
        frame_result.rowconfigure(0, weight=1)
        
        # Área de Texto com Scrollbar
        scrollbar = ttk.Scrollbar(frame_result)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_result = tk.Text(frame_result, wrap="word", font=("Consolas", 10), 
                                   yscrollcommand=scrollbar.set, bg="#f9f9f9", fg="#333", height=30)
        self.text_result.pack(fill="both", expand=True)
        scrollbar.config(command=self.text_result.yview)

    # ----------------------------------------------------
    # ---------- Métodos do Controller (Controller) ----------
    # ----------------------------------------------------

    def add_dimension(self):
        name = self.entry_dim.get().strip()
        values = [v.strip() for v in self.entry_values.get().split(",") if v.strip()]
        if not name or not values:
            messagebox.showerror("Erro", "Informe nome e valores da dimensão.")
            return
        
        if name in self.dimensions:
             messagebox.showwarning("Aviso", f"Dimensão '{name}' já existe. Valores serão mesclados/substituídos.")
        
        self.dimensions[name] = values
        self.refresh_fact_inputs()
        self.refresh_filter_inputs()
        self.entry_dim.delete(0, tk.END) 
        self.entry_values.delete(0, tk.END)
        self.log(f"Dimensão adicionada: **{name}** = {values}")

    def add_fact(self):
        if not self.dimensions:
            messagebox.showerror("Erro", "Crie dimensões primeiro.")
            return
        try:
            value = float(self.entry_value.get())
        except:
            messagebox.showerror("Erro", "Valor numérico inválido.")
            return
        
        fact = {dim: cb.get() for dim, cb in self.fact_entries.items()}
        
        if not all(fact.values()):
            messagebox.showerror("Erro", "Selecione valores para todas as dimensões.")
            return
        
        fact["valor"] = value
        self.facts.append(fact)
        self.log(f"Fato adicionado: {fact}")
        self.entry_value.delete(0, tk.END) 

    def aggregate(self):
        dims = [d.strip() for d in self.entry_agg_dims.get().split(",") if d.strip()]
        measure = self.combo_measure.get()
        
        if not (1 <= len(dims) <= 3) or not measure:
            messagebox.showerror("Erro", "Escolha 1-3 dimensões e a medida (sum, avg, count).")
            return
        for d in dims:
            if d not in self.dimensions:
                # O Erro de "Dimensão inexistente: 1" ocorre aqui. O usuário deve inserir NOMES de dimensão, não números.
                messagebox.showerror("Erro", f"Dimensão inexistente: {d}. Use NOMES de dimensão como PRODUTO, REGIÃO, MÊS.")
                return
        
        result, error = self.model.aggregate_data(dims, measure)

        if error:
            messagebox.showerror("Erro de Agregação", error)
            return

        txt = f"--- RESULTADO DA AGREGAÇÃO: {measure.upper()} por {', '.join(dims)} ---\n"
        if self.filters:
            txt += f"--- FILTROS ATIVOS: {', '.join([f'{d}={v}' for d,v in self.filters.items()])} ---\n"
        
        max_key_len = max(len(str(k)) for k in result) if result else 0
        for k,v in result.items():
            key_str = str(k) if len(dims) > 1 else k[0] 
            txt += f"{key_str.ljust(max_key_len)}: {v:,.2f}\n" 

        self.text_result.delete(1.0, tk.END)
        self.text_result.insert(tk.END, txt)
        self.log("\n" + txt)

        # CORREÇÃO: Passando o dicionário de filtros para o visualizer
        visualize_result(dims, result, measure, filters=self.filters)


    def generate_sample_data(self):
        """Invoca a geração de dados do modelo e atualiza a UI."""
        try:
            num_facts = self.model.generate_sample_data()

            self.refresh_fact_inputs()
            self.refresh_filter_inputs()

            self.log(f"Seed de dados criado: {len(self.dimensions)} dimensões e {num_facts} fatos gerados.")
            messagebox.showinfo("Seed Criado", f"{num_facts} fatos de vendas gerados e prontos para análise.")

        except Exception as e:
             messagebox.showerror("Erro de Geração", f"Não foi possível gerar dados de exemplo.\nDetalhe: {e}")


    # ----------------------------------------------------
    # ---------- Funções Auxiliares (View/Refresh) ----------
    # ----------------------------------------------------

    def refresh_fact_inputs(self):
        for widget in self.frame_facts.winfo_children():
            if int(widget.grid_info().get('row', 101)) < 99:
                widget.destroy()
        
        self.fact_entries.clear()
        
        for i, dim in enumerate(self.dimensions):
            ttk.Label(self.frame_facts, text=f"{dim}:").grid(row=i, column=0, sticky="w", pady=2, padx=5)
            cb = ttk.Combobox(self.frame_facts, values=self.dimensions[dim], state="readonly")
            cb.grid(row=i, column=1, padx=5, sticky="we")
            cb.set(self.dimensions[dim][0] if self.dimensions[dim] else '') 
            self.fact_entries[dim] = cb

    def refresh_filter_inputs(self):
        # NOTA: O botão "Aplicar Filtros" agora está fixado na row 99 no create_widgets.
        for widget in self.frame_filter.winfo_children():
            # Apenas destrói os combos dinâmicos (aqueles com row < 99)
            if int(widget.grid_info().get('row', 100)) < 99:
                 widget.destroy()
        
        self.filter_combos.clear()
        
        for i, dim in enumerate(self.dimensions):
            ttk.Label(self.frame_filter, text=f"{dim}:").grid(row=i, column=0, sticky="w", pady=2, padx=5)
            
            filter_values = ["TODOS"] + self.dimensions[dim]
            cb = ttk.Combobox(self.frame_filter, values=filter_values, state="readonly")
            cb.set(self.filters.get(dim, "TODOS")) 
            cb.grid(row=i, column=1, padx=5, sticky="we")
            self.filter_combos[dim] = cb

    def update_filters(self):
        self.filters.clear()
        log_msg = ["Filtros Ativos:"]
        
        for dim, cb in self.filter_combos.items():
            value = cb.get()
            if value != "TODOS":
                self.filters[dim] = value
                log_msg.append(f" {dim} = '{value}'")
        
        if not self.filters:
            self.log("Nenhum filtro aplicado. Analisando todos os fatos.")
        else:
            self.log(" ".join(log_msg))
            
        messagebox.showinfo("Filtro", "Filtros atualizados. Agora execute a Agregação.")

    # ----------------------------------------------------
    # ---------- Salvar/Carregar & Log (I/O) ----------
    # ----------------------------------------------------

    def save_cube(self):
        if not self.dimensions or not self.facts:
            messagebox.showwarning("Aviso", "Nenhum cubo disponível para salvar.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON","*.json")])
        if not path: return
        data = {"dimensions": self.dimensions, "facts": self.facts}
        try:
            with open(path,"w",encoding="utf-8") as f:
                json.dump(data,f,indent=4)
            self.log(f"Cubo salvo com sucesso: **{os.path.basename(path)}**")
        except Exception as e:
            messagebox.showerror("Erro ao Salvar", f"Não foi possível salvar: {e}")

    def load_cube(self):
        path = filedialog.askopenfilename(filetypes=[("JSON","*.json")])
        if not path: return
        try:
            with open(path,"r",encoding="utf-8") as f:
                data = json.load(f)
            self.dimensions.clear()
            self.dimensions.update(data.get("dimensions",{}))
            self.facts = data.get("facts",[])
            self.filters = {} 
            self.model = OLAPModel(self.dimensions, self.facts, self.filters) 

            self.refresh_fact_inputs()
            self.refresh_filter_inputs()
            self.log(f"Cubo carregado com sucesso: **{os.path.basename(path)}**. Fatos: {len(self.facts)}")
        except Exception as e:
            messagebox.showerror("Erro ao Carregar", f"Não foi possível carregar o arquivo: {e}")

    def log(self, msg):
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        self.text_result.insert(tk.END, f"{timestamp} {msg.replace('**', '').replace('\n', ' ')}\n")
        self.text_result.see(tk.END)

if __name__=="__main__":
    root = tk.Tk()
    app = OLAPApp(root)
    root.mainloop()