import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Lista dei tipi di dati da elaborare (Java e Python)
data_types = ['matlab', 'java', 'python', 'r']

# Definisci i tipi di dati e il sistema operativo
os_names = ['windows', 'linux']

for data_type in data_types:
    # Carica i dati dai file CSV
    data_windows = pd.read_csv(f'dati_{data_type}_windows.csv')
    data_linux = pd.read_csv(f'dati_{data_type}_linux.csv')

    # Ordina i dati per il nome della matrice
    data_windows = data_windows.sort_values(by='Size').reset_index(drop=True)
    data_linux = data_linux.sort_values(by='Size').reset_index(drop=True)

    # Combinazione delle colonne MatrixName e Size in una nuova lista di nomi delle matrici
    matrix_names = [f"{name} \n({size / (1024 * 1024):.2f} MB)" for name, size in
                    zip(data_windows['MatrixName'], data_windows['Size'])]

    # Grafico per il tempo
    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_ylabel('Time (s)', color=color)
    ax1.bar(matrix_names, data_windows['Time'], color=color, width=-0.2, align='edge', label='Windows')
    ax1.bar(matrix_names, data_linux['Time'], color='tab:orange', width=0.2, align='edge', label='Linux')
    ax1.set_yscale('log')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.legend(loc='upper left')
    ax1.set_title(f"Time Comparison - {data_type.capitalize()}")

    plt.xticks(rotation=45, ha='right', fontsize=10)

    # Calcola il valore massimo della memoria tra i due set di dati
    max_time = max(data_windows['Time'].max(), data_linux['Time'].max())

    # Aggiungi le etichette della memoria sopra ogni barra
    for i in range(len(matrix_names)):
        time_label_windows = "{:.2f} s".format(data_windows['Time'][i])
        time_label_linux = "{:.2f} s".format(data_linux['Time'][i])

        # Aggiungi un offset orizzontale diverso per ciascuna etichetta
        offset_windows = -0.05
        offset_linux = 0.05

        label_height = max(data_windows['Time'][i], data_linux['Time'][i]) + 0.05 * max_time
        ax1.text(i + offset_windows, label_height, time_label_windows, ha='right', va='center', fontsize=10)
        ax1.text(i + offset_linux, label_height, time_label_linux, ha='left', va='center', fontsize=10)

    # plt.tight_layout()  # Aggiunge spazio sufficiente per visualizzare le etichette sotto NON PIU' NECESSARIO 
    plt.show()  # Visualizza la figura

    # Grafico per la memoria
    fig, ax2 = plt.subplots()
    color = 'tab:blue'
    ax2.set_ylabel('Memory (MB)', color=color)
    ax2.bar(matrix_names, data_windows['MemoryDiff'] / (1024 * 1024), color=color, width=-0.2, align='edge', alpha=0.5,
            label='Windows')
    ax2.bar(matrix_names, data_linux['MemoryDiff'] / (1024 * 1024), color='tab:cyan', width=0.2, align='edge',
            alpha=0.5, label='Linux')
    ax2.set_yscale('log')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.legend(loc='upper left')
    ax2.set_title(f"Memory Comparison - {data_type.capitalize()}")

    plt.xticks(rotation=45, ha='right', fontsize=10)

    # Calcola il valore massimo della memoria tra i due set di dati
    max_memory = max(data_windows['MemoryDiff'].max() / (1024 * 1024), data_linux['MemoryDiff'].max() / (1024 * 1024))

    # Aggiungi le etichette della memoria sopra ogni barra
    for i in range(len(matrix_names)):
        memory_label_windows = "{:.2f} MB".format(data_windows['MemoryDiff'][i] / (1024 * 1024))
        memory_label_linux = "{:.2f} MB".format(data_linux['MemoryDiff'][i] / (1024 * 1024))

        # Aggiungi un offset orizzontale diverso per ciascuna etichetta
        offset_windows = -0.05
        offset_linux = 0.05

        label_height = max(data_windows['MemoryDiff'][i] / (1024 * 1024),
                           data_linux['MemoryDiff'][i] / (1024 * 1024)) + 0.05 * max_memory
        ax2.text(i + offset_windows, label_height, memory_label_windows, ha='right', va='center', fontsize=10)
        ax2.text(i + offset_linux, label_height, memory_label_linux, ha='left', va='center', fontsize=10)

    # plt.tight_layout()  # Aggiunge spazio sufficiente per visualizzare le etichette sotto NON PIU' NECESSARIO 
    plt.show()  # Visualizza la figura

    # Grafico per l'errore relativo
    fig, ax3 = plt.subplots()
    ax3.bar(matrix_names, data_windows['Error'], color='green', width=-0.2, align='edge', label='Windows')
    ax3.bar(matrix_names, data_linux['Error'], color='lightgreen', width=0.2, align='edge', label='Linux')
    ax3.set_yscale('log')
    ax3.set_ylabel('Error')
    ax3.legend(loc='upper right')
    ax3.set_title(f"Error Comparison - {data_type.capitalize()}")

    # Imposta l'asse x con i nomi delle matrici
    plt.xticks(rotation=45, ha='right', fontsize=10)

    # Calcola l'altezza massima dell'errore relativo tra i due set di dati
    max_error = max(data_windows['Error'].max(), data_linux['Error'].max())

    for i in range(len(matrix_names)):
        error_label_windows = "{:.4e}".format(data_windows['Error'][i])
        error_label_linux = "{:.4e}".format(data_linux['Error'][i])

        # Calcola l'altezza verticale per le etichette
        offset_windows = -0.05
        offset_linux = 0.05

        label_height = max(data_windows['Error'][i], data_linux['Error'][i]) + 0.05 * max_error
        ax3.text(i + offset_windows, label_height, error_label_windows, ha='right', fontsize=10)
        ax3.text(i + offset_linux, label_height, error_label_linux, ha='left', fontsize=10)

    # Mostra i grafici
    # plt.tight_layout()
    plt.show()

def create_comparison_plot(data, data_types, os_name, value_column, ylabel, title):
    # Estrai tutti i nomi delle matrici da uno dei dataframes
    matrix_names = data[data_types[2]]['MatrixName']

    # Calcola la larghezza di ogni barra
    bar_width = 0.2

    # Crea il grafico
    fig, ax = plt.subplots()

    # Ordina le matrici in base alla loro dimensione
    sorted_matrix_names = sorted(matrix_names, key=lambda x: data[data_types[2]][data[data_types[2]]['MatrixName'] == x]['Size'].values[0])

    # Loop attraverso ciascun linguaggio di programmazione
    for i, data_type in enumerate(data_types):
        value_values = []

        # Estrai i valori corrispondenti (errore, tempo o memoria) per le matrici presenti nel dataframe corrente
        for matrix_name in sorted_matrix_names:
            if matrix_name in data[data_type]['MatrixName'].values:
                value_values.append(data[data_type][data[data_type]['MatrixName'] == matrix_name][value_column].values[0])
            else:
                value_values.append(0)  # Imposta il valore corrispondente a 0 per le matrici mancanti

        # Calcola la posizione delle barre per il linguaggio di programmazione corrente
        x_indices = np.arange(len(sorted_matrix_names)) + i * bar_width - (len(data_types) - 1) * bar_width / 2

        # Crea le barre per i valori corrispondenti (errore, tempo o memoria) di ciascun linguaggio di programmazione
        bars = ax.bar(x_indices, value_values, bar_width, label=f'{data_type} {ylabel}')

        max_label_height = ax.get_ylim()[1] * 0.9

        # Aggiungi il valore corrispondente al formato corretto all'interno di ogni barra
        for bar, value in zip(bars, value_values):
            if value_column == 'Time':
                formatted_value = f'{value:.3f} s'  # Formattazione in secondi per il tempo
            elif value_column == 'MemoryDiff':
                formatted_value = f'{value / (1024 * 1024):.1f} MB'  # Formattazione in MB per la memoria
            else:
                formatted_value = f'{value:.2e}'  # Notazione scientifica per l'errore
            bar_height = bar.get_height()
            if bar_height < max_label_height:
                ax.text(bar.get_x() + bar.get_width() / 2, bar_height, formatted_value, ha='center', va='bottom', rotation='horizontal', fontsize=8)
            else:
                ax.text(bar.get_x() + bar.get_width() / 2, max_label_height, formatted_value, ha='center', va='bottom', rotation='horizontal', fontsize=8)


    ax.set_yscale('log')  # Scala logaritmica sull'asse y
    ax.set_xticks(np.arange(len(sorted_matrix_names)))
    ax.set_xticklabels(sorted_matrix_names, rotation=45, ha='right', fontsize=10)
    ax.set_xlabel('Matrices')
    ax.set_ylabel(ylabel)
    ax.legend()
    ax.set_title(f'{title} - {os_name.capitalize()}')

    plt.tight_layout()
    plt.show()

# Leggi i dati e crea i grafici per entrambi i sistemi operativi
for os_name in os_names:
    data = {}
    for data_type in data_types:
        data[data_type] = pd.read_csv(f'dati_{data_type}_{os_name}.csv')
    
    create_comparison_plot(data, data_types, os_name, 'Error', 'Relative Error', 'Relative Error Comparison')
    create_comparison_plot(data, data_types, os_name, 'Time', 'Time', 'Time Comparison')
    create_comparison_plot(data, data_types, os_name, 'MemoryDiff', 'Memory', 'Memory Comparison')












 