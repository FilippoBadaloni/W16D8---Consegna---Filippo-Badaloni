"""
Questo modulo analizza i dati di diffusione del COVID-19 nel mondo,
includendo casi e vaccinazioni in diverse aree del mondo.
"""

import pandas as pd
import matplotlib.pyplot as plt

# Caricare il dataset
# Assicurati che il percorso e il nome del file siano corretti
FILE_PATH = 'C:/Users/fbadaloni/Downloads/owid-covid-data.xlsx'
df = pd.read_excel(FILE_PATH)


def print_dataset_info(dataframe):
    """Verifica le dimensioni del dataset e i relativi metadati."""
    print("Dimensioni del dataset:", dataframe.shape)
    print("Metadati del dataset:")
    print(dataframe.info())


print_dataset_info(df)

# Filtrare il dataset per continenti
continents_df = df.dropna(subset=['continent'])


def total_cases_by_continent(dataframe):
    """Calcola il numero di casi totali per continente."""
    return dataframe.groupby('continent')['total_cases'].sum()


cases_by_continent = total_cases_by_continent(continents_df)
print("Casi totali per continente:")
print(cases_by_continent)


def compare_continents(dataframe, continent1, continent2):
    """Confronta due continenti sui descrittori statistici dei casi totali."""
    data_a = dataframe[dataframe['continent']
                       == continent1]['total_cases'].dropna()
    data_b = dataframe[dataframe['continent']
                       == continent2]['total_cases'].dropna()

    comparison = pd.DataFrame({
        'Statistic': ['Max', 'Mean', 'Percentage of World Total'],
        continent1: [data_a.max(), data_a.mean(), data_a.sum() / df['total_cases'].sum() * 100],
        continent2: [data_b.max(), data_b.mean(), data_b.sum() /
                     df['total_cases'].sum() * 100]
    })

    return comparison


CONTINENT_A = 'Europe'
CONTINENT_B = 'Asia'
comparison_df = compare_continents(continents_df, CONTINENT_A, CONTINENT_B)
print(f"Confronto tra {CONTINENT_A} e {CONTINENT_B}:")
print(comparison_df)


def plot_italy_2022(dataframe):
    """Grafici per l'Italia nel 2022."""
    italy_2022 = dataframe[(dataframe['location'] == 'Italy') & (
        dataframe['date'].between('2022-01-01', '2022-12-31'))]

    # Evoluzione dei casi totali rispetto alla data
    plt.figure(figsize=(10, 5))
    plt.plot(italy_2022['date'], italy_2022['total_cases'],
             label='Casi Totali')
    plt.title('Evoluzione dei casi totali in Italia nel 2022')
    plt.xlabel('Data')
    plt.ylabel('Casi Totali')
    plt.legend()
    plt.show()

    # Numero di nuovi casi rispetto alla data
    plt.figure(figsize=(10, 5))
    plt.plot(italy_2022['date'], italy_2022['new_cases'],
             label='Nuovi Casi', color='orange')
    plt.title('Nuovi casi giornalieri in Italia nel 2022')
    plt.xlabel('Data')
    plt.ylabel('Nuovi Casi')
    plt.legend()
    plt.show()

    # Andamento della somma cumulativa nuovi casi del 2022
    italy_2022['cumulative_new_cases'] = italy_2022['new_cases'].cumsum()

    plt.figure(figsize=(10, 5))
    plt.plot(italy_2022['date'], italy_2022['cumulative_new_cases'],
             label='Cumulativo Nuovi Casi', color='green')
    plt.title('Andamento della somma cumulativa nuovi casi in Italia nel 2022')
    plt.xlabel('Data')
    plt.ylabel('Cumulativo Nuovi Casi')
    plt.legend()
    plt.show()


plot_italy_2022(df)


def plot_icu_boxplot(dataframe):
    """Boxplot per Italia, Germania e Francia riguardo il numero di pazienti in terapia intensiva."""
    countries = ['Italy', 'Germany', 'France']
    icu_data = dataframe[(dataframe['location'].isin(countries)) & (
        dataframe['date'].between('2022-05-01', '2023-04-30'))]

    plt.figure(figsize=(10, 5))
    icu_data.boxplot(column='icu_patients', by='location', grid=False)
    plt.title(
        'Numero di pazienti in terapia intensiva (ICU) da maggio 2022 ad aprile 2023')
    plt.suptitle('')
    plt.xlabel('Paese')
    plt.ylabel('Pazienti in Terapia Intensiva')
    plt.show()


plot_icu_boxplot(df)


def hospitalizations_2023(dataframe):
    """Somma dei pazienti ospitalizzati per Italia, Germania, Francia e Spagna nel 2023."""
    countries_2023 = ['Italy', 'Germany', 'France', 'Spain']
    hospital_data_2023 = dataframe[(dataframe['location'].isin(countries_2023)) & (
        dataframe['date'].between('2023-01-01', '2023-12-31'))]

    hospital_sum = hospital_data_2023.groupby(
        'location')['hosp_patients'].sum().fillna(0)
    print("Somma dei pazienti ospitalizzati nel 2023:")
    print(hospital_sum)
    print("Suggerimento per la gestione dei dati nulli: se ci sono dati nulli, è possibile sostituirli con il valore medio o mediano del dataset per quella variabile.")


hospitalizations_2023(df)
