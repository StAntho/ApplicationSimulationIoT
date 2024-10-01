import streamlit as st
import pandas as pd
from functions import *
import matplotlib.pyplot as plt
import numpy as np
import altair as alt
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

# onglet de la page
st.set_page_config(
    page_icon='🚑',
    page_title='Sport Prevention Injuries',
    layout='wide'
)

st.title("Simulation de d'analyse de données par capteur")

# Afficher les données à intervalles réguliers
state = True
ages = [22, 25, 31, 24, 35]
heights = [182, 177, 181, 179, 190]
weights = [85, 80, 79, 77, 95]
age_1 = 22
age_2 = 25
age_3 = 31
age_4 = 24
age_5 = 35
height_1 = 182
height_2 = 177
height_3 = 181
height_4 = 179
height_5 = 190
weight_1 = 85
weight_2 = 80
weight_3 = 79
weight_4 = 77
weight_5 = 95

df = pd.read_csv('./datas/random_data.csv')

for i in range(5):
    df_player = df[df['device'] == f'device-{i+1}']
    st.write(df_player)
    st.write(f"Age: {ages[i]} ans, Taille: {heights[i]} cm, Poids: {weights[i]} kg, imc: {imc(weights[i], heights[i])} kg/m²")
    fM = get_heart_rate_max(ages[i])
    fm = get_heart_rate_min(ages[i])
    st.write(f"FC Max: {fM} bpm, FC min: {fm} bpm, FC moyenne: {round(df_player['heart_rate'].mean(), 2)} bpm")
    if df_player['heart_rate'].mean() > fM:
        st.write(f":red[Attention]: la fréquence cardiaque moyenne est supérieure à la fréquence cardiaque maximale ({fM} bpm).")
    elif df_player['heart_rate'].mean() < fm:
        st.write(f":red[Attention]: la fréquence cardiaque moyenne est inférieure à la fréquence cardiaque minimale ({fm} bpm).")

    st.write(f"Distance parcourue: {round(df_player['distance'].sum(), 3)} km, Calories brûlées: {round(caloric_expenditure(ages[i], weights[i], df_player['heart_rate'].mean(), 15), 2)} kcal")
    st.write(f"VO2 Max: {round(get_vo2_max(ages[i], weights[i], df_player['heart_rate'].mean()), 2)} ml/kg/min")
    st.write(f"Intensité de l'entraînement: {round(training_intensity(df_player['heart_rate'].mean(), fM), 2)} %, Charge d'entraînement: {round(training_load(df_player['heart_rate'].mean(), fM, 15), 2)}")
    st.write(f"Pic de débit expiratoire: {round(peak_expiratory_flow(ages[i], heights[i], weights[i]), 2)} l/min")
    st.write(f"Volume courant des poumons: {round(tidal_volume(weights[i]), 2)} l")
    st.write(f"Indice de fatigue: {round(fatigue_index(df_player['value'].mean(), 15), 2)} %")
    st.write(f"TSS: {round(get_tss(15, df_player['value']), 2)}")

    data_hr = df_player['heart_rate']
    st.write(data_hr)
    arr = np.random.normal(1, 1, size=50)
    fig, ax = plt.subplots()
    # ax.hist(arr, bins=20)

    # st.pyplot(fig)
    # # Create a histogram
    # st.hist(data, bins=20, color='skyblue', edgecolor='black')
    # # Add title and labels
    # st.title('Interactive Histogram with Streamlit')
    # st.xlabel('X-axis Label')
    # st.ylabel('Y-axis Label')
    # st.show()
    # test = df_player, columns=['heart_rate', 'time']
    # st.write(test)
    # Create a line chart
    # st.line_chart(df_player, x=df_player['time'], y=df_player['heart_rate'])

    # Add title and labels
    # st.title('Interactive Line Chart with Streamlit')
    # st.xlabel('X-axis Label')
    # st.ylabel('Y-axis Label')
    # st.show()

    # Create a bar chart
    df_player['time'] = pd.to_datetime(df_player['time'])
    df_player['date'] = df_player['time'].dt.date
    st.write(df_player)
    daily_values = df_player.groupby('date')['distance'].sum().reset_index()
    st.write(daily_values)
    # Afficher l'histogramme avec Streamlit
    st.title("Histogramme des valeurs par jour")

    # Utiliser st.bar_chart pour afficher l'histogramme
    st.bar_chart(daily_values.set_index('date'))

    # Seuils
    threshold_low = 5
    threshold_high = 10

    # Créer le bar chart avec Altair
    bars = alt.Chart(daily_values).mark_bar().encode(
        x='date:T',
        y='value:Q'
    ).properties(
        title='Histogramme des valeurs par jour'
    )

    # Ajouter des labels sur les barres
    text = bars.mark_text(
        align='center',
        baseline='bottom',
        dy=-10  # Décalage des labels
    ).encode(
        text='value:Q'
    )

    # Ajouter les seuils
    threshold_low_line = alt.Chart(pd.DataFrame({'threshold': [threshold_low]})).mark_rule(color='red').encode(
        y='threshold:Q'
    )
    threshold_high_line = alt.Chart(pd.DataFrame({'threshold': [threshold_high]})).mark_rule(color='green').encode(
        y='threshold:Q'
    )

    # Combiner les barres, les labels et les seuils
    chart = bars + text + threshold_low_line + threshold_high_line

    # Afficher le bar chart avec Streamlit
    st.title("Histogramme des valeurs par jour avec seuils et labels")
    st.altair_chart(chart, use_container_width=True)

    # Ajouter des explications pour les axes
    st.write("""
    ### Détails des valeurs par jour
    - **Axe des X** : Dates
    - **Axe des Y** : Somme des valeurs
    - **Ligne rouge** : Seuil bas (5)
    - **Ligne verte** : Seuil haut (10)
    """)
    
    # st.bar_chart(None, df_player['date'], df_player['distance'])
    # daily_values = df_player.groupby('date')['distance'].sum()
    # # Créer l'histogramme
    # plt.figure(figsize=(10, 6))
    # daily_values.plot(kind='bar')
    # plt.title('Histogramme des valeurs par jour')
    # plt.xlabel('Date')
    # plt.ylabel('Somme des valeurs')
    # plt.xticks(rotation=45)
    # plt.grid(axis='y')
    # plt.show()
    st.title("Histogramme des valeurs par jour HR")
    df_new = df_player[['time', 'heart_rate']]
    # df_new.reset_index()
    # Définir les seuils
    min_threshold = 60
    max_threshold = 200

    # Calculer la moyenne des fréquences cardiaques
    mean_heart_rate = df_new['heart_rate'].mean()

    # Ajouter des colonnes pour indiquer les dépassements de seuils
    df_new['below_min'] = df_new['heart_rate'] < min_threshold
    df_new['above_max'] = df_new['heart_rate'] > max_threshold

    # Calculer une moyenne glissante pour représenter la courbe de fatigue
    window_size = 5  # Taille de la fenêtre pour la moyenne glissante
    df_new['fatigue_curve'] = df_new['heart_rate'].rolling(window=window_size).mean()

    # Sélection de la période de temps
    time_options = ['Dernière heure', 'Aujourd\'hui', '7 derniers jours', 'Ce mois-ci', 'Cette année']
    time_selection = st.selectbox('Sélectionner la période de temps', time_options)

    # Filtrer les données en fonction de la période sélectionnée
    now = datetime.now()

    if time_selection == 'Dernière heure':
        start_time = now - timedelta(hours=1)
    elif time_selection == 'Aujourd\'hui':
        start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif time_selection == '7 derniers jours':
        start_time = now - timedelta(days=7)
    elif time_selection == 'Ce mois-ci':
        start_time = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    elif time_selection == 'Cette année':
        start_time = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        start_time = df_new['time'].min()

    filtered_df = df_new[df_new['time'] >= start_time]

    # Afficher les données
    st.write(f"Voici les données de fréquence cardiaque pour la période : {time_selection}")
    st.write(filtered_df)

    # Option d'affichage de la courbe de fatigue
    show_fatigue_curve = st.radio('Afficher la courbe de fatigue ?', ('Oui', 'Non'))
    
    # Créer un graphique Plotly
    fig = go.Figure()

    # Ajouter les données de fréquence cardiaque
    fig.add_trace(go.Scatter(x=filtered_df['time'], y=filtered_df['heart_rate'], mode='lines+markers', name='Heart Rate'))

    # Marquer les points en dessous du seuil minimum
    fig.add_trace(go.Scatter(x=filtered_df[filtered_df['below_min']]['time'], y=filtered_df[filtered_df['below_min']]['heart_rate'],
                            mode='markers', marker=dict(color='red'), name='Below Min Threshold'))

    # Marquer les points au-dessus du seuil maximum
    fig.add_trace(go.Scatter(x=filtered_df[filtered_df['above_max']]['time'], y=filtered_df[filtered_df['above_max']]['heart_rate'],
                            mode='markers', marker=dict(color='orange'), name='Above Max Threshold'))

    # Ajouter des lignes de seuils
    fig.add_hline(y=min_threshold, line=dict(color='blue', dash='dash'), name='Min Threshold')
    fig.add_hline(y=max_threshold, line=dict(color='green', dash='dash'), name='Max Threshold')

    # Ajouter une ligne pour la moyenne des fréquences cardiaques
    fig.add_hline(y=mean_heart_rate, line=dict(color='purple', dash='solid'), name=f'Mean Heart Rate ({mean_heart_rate:.2f})')

    # Ajouter la courbe de fatigue
    if show_fatigue_curve == 'Oui':
        fig.add_trace(go.Scatter(x=filtered_df['time'], y=filtered_df['fatigue_curve'], mode='lines', line=dict(color='cyan'), name='Fatigue Curve'))

    # Configurer les axes et le titre
    fig.update_layout(title='Heart Rate Monitoring and Fatigue Curve',
                    xaxis_title='Time',
                    yaxis_title='Heart Rate',
                    legend_title='Legend')

    # Afficher le graphique dans Streamlit
    st.plotly_chart(fig)



    # st.write('---------------------------------------')



    # # Définir les seuils
    # min_threshold = 60
    # max_threshold = 200
    # mean_heart_rate = df_new['heart_rate'].mean()
    # # Ajouter des colonnes pour indiquer les dépassements de seuils
    # df_new['below_min'] = df_new['heart_rate'] < min_threshold
    # df_new['above_max'] = df_new['heart_rate'] > max_threshold
    # window_size = 5  # Taille de la fenêtre pour la moyenne glissante
    # df_new['fatigue_curve'] = df_new['heart_rate'].rolling(window=window_size).mean()
    # st.write(df_new)

    # # Sélection de la période de temps
    # time_opt = ['Dernière heure', 'Aujourd\'hui', '7 derniers jours', 'Ce mois-ci', 'Cette année']
    # time_selection2 = st.selectbox('Sélectionner la durée', time_opt)

    # # Filtrer les données en fonction de la période sélectionnée
    # now = datetime.now()

    # if time_selection2 == 'Dernière heure':
    #     start_time = now - timedelta(hours=1)
    # elif time_selection2 == 'Aujourd\'hui':
    #     start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
    # elif time_selection2 == '7 derniers jours':
    #     start_time = now - timedelta(days=7)
    # elif time_selection2 == 'Ce mois-ci':
    #     start_time = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    # elif time_selection2 == 'Cette année':
    #     start_time = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    # else:
    #     start_time = df_new['time'].min()

    # filtered_df = df_new[df_new['time'] >= start_time]

    # # Afficher les données
    # st.write(f"Voici les données de fréquence cardiaque pour la période : {time_selection2}")
    # st.write(filtered_df)

    # # Tracer les fréquences cardiaques
    # fig, ax = plt.subplots(figsize=(12, 6))
    # ax.plot(filtered_df['time'], filtered_df['heart_rate'], label='Heart Rate', marker='o')

    # # Marquer les points en dessous du seuil minimum
    # ax.scatter(filtered_df[filtered_df['below_min']]['time'], filtered_df[filtered_df['below_min']]['heart_rate'], color='red', label='Below Min Threshold')

    # # Marquer les points au-dessus du seuil maximum
    # ax.scatter(filtered_df[filtered_df['above_max']]['time'], filtered_df[filtered_df['above_max']]['heart_rate'], color='orange', label='Above Max Threshold')

    # # Ajouter des lignes de seuils
    # ax.axhline(y=min_threshold, color='blue', linestyle='--', label='Min Threshold')
    # ax.axhline(y=max_threshold, color='green', linestyle='--', label='Max Threshold')

    # # Ajouter une ligne pour la moyenne des fréquences cardiaques
    # ax.axhline(y=mean_heart_rate, color='purple', linestyle='-', label=f'Mean Heart Rate ({mean_heart_rate:.2f})')
    
    # # Ajouter la courbe de fatigue
    # ax.plot(filtered_df['time'], filtered_df['fatigue_curve'], color='cyan', linestyle='-', label='Fatigue Curve')

    # # Ajouter des légendes et des titres
    # ax.set_xlabel('Time')
    # ax.set_ylabel('Heart Rate')
    # ax.set_title('Heart Rate Monitoring')
    # ax.legend()

    # # Afficher le graphique dans Streamlit
    # st.pyplot(fig)