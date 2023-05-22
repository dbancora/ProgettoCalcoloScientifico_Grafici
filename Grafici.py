import pandas as pd
import matplotlib.pyplot as plt

"""

###########################PRIMA VERSIONE###########################

# Carica i dati dal file CSV
data = pd.read_csv('dati_java.csv')
data = data.sort_values(by='Size').reset_index(drop=True)

print(data)

# Combinazione delle colonne MatrixName e Size in una nuova lista di nomi delle matrici
matrix_names = [f"{name} ({size/(1024*1024):.2f} MB)" for name, size in zip(data['MatrixName'], data['Size'])]


# Crea il grafico a barre con doppio asse y
fig, ax1 = plt.subplots()

# Barre per i tempi
color = 'tab:red'
ax1.set_ylabel('Time (s)', color=color)
ax1.bar(matrix_names, data['Time'], color=color, width=-0.2, align='edge')
ax1.tick_params(axis='y', labelcolor=color)

for i, v in enumerate(data['Time']):
    ax1.annotate(f'{v:.2f} s', xy=(i-0.2, v), ha='center', va='bottom', color=color)

# Crea l'asse y per i tempi
ax2 = ax1.twinx()

# Barre per la memoria
color = 'tab:blue'
ax2.set_ylabel('Memory (MB)', color=color)
ax2.bar(matrix_names, data['MemoryDiff']/(1024*1024), color=color, width=0.2, align='edge', alpha=0.5)
ax2.tick_params(axis='y', labelcolor=color)

# Aggiungi le etichette di testo per la memoria utilizzando il metodo annotate di Matplotlib
for i, v in enumerate(data['MemoryDiff']):
    ax2.annotate(f'{v/(1024*1024):.2f} MB', xy=(i+0.2, v/(1024*1024)), ha='center', va='bottom', color=color)



# Crea l'asse y per la memoria
ax2.tick_params(axis='y', labelcolor=color)

# Aggiungi l'etichetta sull'asse x, inclinazione e titolo
plt.xticks(rotation=45, ha='right')
plt.xlabel('matrix_names')
plt.title('Memory and Time for Solving Linear Systems')

# Visualizza il grafico
plt.show()


#---------GRAFICO ERRORE RELATIVO----------#


# Normalizza l'errore relativo
max_error = data['Error'].max()
data['NormalizedError'] = data['Error'] / max_error


# Crea un grafico a barre dell'errore relativo normalizzato per ogni matrice
plt.bar(matrix_names, data['NormalizedError'], color='green')

# Aggiungi le etichette sull'asse x e y
plt.xlabel('Matrice')
plt.ylabel('Errore Relativo Normalizzato')

# Imposta la scala logaritmica sull'asse y
plt.yscale('log')

# Aggiungi le etichette dell'errore relativo sopra ogni barra
for i in range(len(matrix_names)):
    error_label = "{:.4e}".format(data['Error'][i])
    plt.text(i, data['NormalizedError'][i]+0.05, error_label, ha='center')



# Ruota le etichette sull'asse x di 90 gradi per renderle leggibili
# plt.xticks(rotation=90)

# Mostra il grafico
plt.show()

"""

##################################SECONDA VERSIONE################################

import pandas as pd
import matplotlib.pyplot as plt

# Carica i dati dai file CSV
data_windows = pd.read_csv('dati_java_windows.csv')
data_linux = pd.read_csv('dati_java_linux.csv')

# Ordina i dati per il nome della matrice
data_windows = data_windows.sort_values(by='Size').reset_index(drop=True)
data_linux = data_linux.sort_values(by='Size').reset_index(drop=True)

# Combinazione delle colonne MatrixName e Size in una nuova lista di nomi delle matrici
matrix_names = [f"{name} ({size/(1024*1024):.2f} MB)" for name, size in zip(data_windows['MatrixName'], data_windows['Size'])]

# Grafico per il tempo
fig, ax1 = plt.subplots()
color = 'tab:red'
ax1.set_ylabel('Time (s)', color=color)
ax1.bar(matrix_names, data_windows['Time'], color=color, width=-0.2, align='edge', label='Windows')
ax1.bar(matrix_names, data_linux['Time'], color='tab:orange', width=0.2, align='edge', label='Linux')
ax1.set_yscale('log')
ax1.tick_params(axis='y', labelcolor=color)
ax1.legend(loc='upper left')

plt.xticks(rotation=45, ha='right', fontsize=6)

# Grafico per la memoria
fig, ax2 = plt.subplots()
color = 'tab:blue'
ax2.set_ylabel('Memory (MB)', color=color)
ax2.bar(matrix_names, data_windows['MemoryDiff']/(1024*1024), color=color, width=-0.2, align='edge', alpha=0.5, label='Windows')
ax2.bar(matrix_names, data_linux['MemoryDiff']/(1024*1024), color='tab:cyan', width=0.2, align='edge', alpha=0.5, label='Linux')
ax2.set_yscale('log')
ax2.tick_params(axis='y', labelcolor=color)
ax2.legend(loc='upper left')

plt.xticks(rotation=45, ha='right', fontsize=6)

# Calcola il valore massimo della memoria tra i due set di dati
max_memory = max(data_windows['MemoryDiff'].max(), data_linux['MemoryDiff'].max())

# Aggiungi le etichette della memoria sopra ogni barra
for i in range(len(matrix_names)):
    memory_label_windows = "{:.2f} MB".format(data_windows['MemoryDiff'][i] / (1024*1024))
    memory_label_linux = "{:.2f} MB".format(data_linux['MemoryDiff'][i] / (1024*1024))
    # Calcola l'altezza verticale per le etichette
    label_height = max(data_windows['MemoryDiff'][i], data_linux['MemoryDiff'][i]) + 0.05 * max_memory
    # Aggiungi un offset orizzontale diverso per ciascuna etichetta
    offset_windows = -0.15
    offset_linux = 0.15
    ax2.text(i + offset_windows, label_height, memory_label_windows, ha='center', fontsize=6)
    ax2.text(i + offset_linux, label_height, memory_label_linux, ha='center', fontsize=6)

# Grafico per l'errore relativo
fig, ax3 = plt.subplots()
ax3.bar(matrix_names, data_windows['Error'], color='green', width=-0.2, align='edge', label='Windows')
ax3.bar(matrix_names, data_linux['Error'], color='lightgreen', width=0.2, align='edge', label='Linux')
ax3.set_yscale('log')
ax3.set_ylabel('Normalized Relative Error')
ax3.legend(loc='upper left')

# Imposta l'asse x con i nomi delle matrici
plt.xticks(rotation=45, ha='right', fontsize=6)

# Calcola l'altezza massima dell'errore relativo tra i due set di dati
max_error = max(data_windows['Error'].max(), data_linux['Error'].max())

for i in range(len(matrix_names)):
    error_label_windows = "{:.4e}".format(data_windows['Error'][i])
    error_label_linux = "{:.4e}".format(data_linux['Error'][i])
    # Calcola l'altezza verticale per le etichette
    offset_windows = -0.10
    offset_linux = 0.10
    label_height = max(data_windows['Error'][i], data_linux['Error'][i]) + 0.05 * max_error
    ax3.text(i + offset_windows, label_height, error_label_windows, ha='right', fontsize=6)
    ax3.text(i + offset_linux, label_height, error_label_linux, ha='left', fontsize=6)

# Mostra i grafici
plt.show()


