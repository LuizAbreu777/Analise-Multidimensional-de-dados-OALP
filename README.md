# 📊 Análise Multidimensional de Dados (multidim-OLAP)

Aplicação desktop para análise multidimensional de vendas usando conceitos OLAP (On-Line Analytical Processing).

## 🎨 Novo Visual

Interface moderna com paleta de cores **Preto + Amarelo**, layout dinâmico e visualizações interativas.

## 📋 Requisitos

### Sistema Operacional
- **macOS** ✅ (já está usando)
- **Windows** ✅
- **Linux**

### Python
- **Python 3.6+** ✅ (você tem Python 3.9.6)

### Dependências
- `tkinter` (já vem com Python) ✅
- `matplotlib` (para gráficos 2D e 3D)
- `numpy` (para cálculos numéricos)

## 🚀 Como Instalar e Rodar

### 1️⃣ Instalar as Dependências

Abra o terminal no diretório do projeto e execute:

```bash
pip3 install -r requirements.txt
```

Ou instale manualmente:

```bash
pip3 install matplotlib numpy
```

### 2️⃣ Executar a Aplicação

```bash
python3 olap_app.py
```

## 📖 Como Usar

### Passo 1: Definição de Dimensões
- Crie dimensões (ex: PRODUTO, REGIÃO, MÊS)
- Insira valores separados por vírgula

### Passo 2: Inserção de Fatos
- Adicione registros de vendas
- Selecione valores para cada dimensão
- Informe o valor da venda

### Passo 3: Gestão de Dados
- **💾 Salvar Cubo**: Salve seus dados em arquivo JSON
- **📂 Carregar Cubo**: Carregue dados salvos anteriormente
- **🌱 Gerar Dados de Exemplo**: Crie dados de demonstração automaticamente

### Passo 4: Análise
- **🔍 Filtros**: Aplique filtros nas dimensões (Slice & Dice)
- **📊 Agregação**: Escolha 1-3 dimensões e visualize os resultados

## 📈 Visualizações

A aplicação gera gráficos automáticos:
- **1D**: Gráfico de barras
- **2D**: Mapa de calor (heatmap)
- **3D**: Visualização 3D interativa

## 🎨 Características da Interface

- **Header** preto com título amarelo
- **Status bar** com contadores em tempo real
- **Cards** com design moderno
- **Paleta** preto/amarelo profissional
- **Layout** responsivo e dinâmico

## 🛠️ Arquivos do Projeto

- `olap_app.py` - Interface principal (Tkinter)
- `data_model.py` - Modelo de dados e lógica OLAP
- `visualizer.py` - Geração de gráficos (Matplotlib)
- `theme_config.py` - Configuração de tema e cores
- `requirements.txt` - Dependências do projeto

## 📝 Exemplo de Uso

1. Clique em **🌱 Gerar Dados de Exemplo**
2. Vá para a aba **❷ Análise e Relatório**
3. Escolha dimensões: `PRODUTO, REGIÃO`
4. Selecione a medida: `sum`
5. Clique em **📈 Agregar e Plotar**
6. Veja o gráfico 2D ser gerado automaticamente!

## ⚡ Dicas

- Use os filtros para analisar subconjuntos específicos
- Tente diferentes combinações de medidas (sum, avg, count)
- Salve seus cubos para análise posterior
- Explore visualizações 1D, 2D e 3D

---

Desenvolvido com ❤️ usando Python + Tkinter + Matplotlib

