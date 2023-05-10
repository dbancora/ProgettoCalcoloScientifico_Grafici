import pandas as pd
import matplotlib.pyplot as plt

# Carica i dati dal file CSV
data = pd.read_csv('dati_matlab.csv')
data = data.sort_values(by='Size')

# Combinazione delle colonne MatrixName e Size in una nuova lista di nomi delle matrici
matrix_names = [f"{name} ({size/(1024*1024):.2f} MB)" for name, size in zip(data['MatrixName'], data['Size'])]


# Crea il grafico a barre con doppio asse y
fig, ax1 = plt.subplots()

# Barre per la memoria
color = 'tab:red'
ax1.set_ylabel('Memory (MB)', color=color)
ax1.bar(matrix_names, data['MemoryDiff']/(1024*1024), color=color, width=-0.2, align='edge')
ax1.tick_params(axis='y', labelcolor=color)

for i, v in enumerate(data['MemoryDiff']):
    ax1.annotate(f'{v/(1024*1024):.2f} MB', xy=(i-0.2, v/(1024*1024)), ha='center', va='bottom', color=color)

# Crea l'asse y per i tempi
ax2 = ax1.twinx()

# Barre per i tempi
color = 'tab:blue'
ax2.set_ylabel('Time (s)', color=color)
ax2.bar(matrix_names, data['Time'], color=color, width=0.2, align='edge')
ax2.tick_params(axis='y', labelcolor=color)

# Aggiungi le etichette di testo per i tempi utilizzando il metodo annotate di Matplotlib
for i, v in enumerate(data['Time']):
    ax2.annotate(f'{v:.2f} s', xy=(i+0.2, v), ha='center', va='bottom', color=color)

# Aggiungi l'etichetta sull'asse x, inclinazione e titolo
plt.xticks(rotation=45, ha='right')
plt.xlabel('matrix_names')
plt.title('Memory and Time for Solving Linear Systems')

# Visualizza il grafico
plt.show()

