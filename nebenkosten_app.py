import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import toml

st.set_page_config(layout='wide')
st.title('Mein Nebenkosten-App')

preisliste = toml.load("data/energieanbieter.toml")
select_anbieter = st.sidebar.selectbox('Ihr Energieanbieter:', ['TWL'])
select_stadt = st.sidebar.selectbox('Ihr Stadt:', ['Ludwigshafen'])
if select_anbieter == "TWL":
    anbieter = "twl"

if select_stadt == "Ludwigshafen":
    stadt = "ludwigshafen"


arbeitspreis_cent_pro_kWh = preisliste[anbieter]["arbeitspreis_cent_pro_kWh"]
grundpreis_euro_pro_jahr = preisliste[anbieter]["grundpreis_euro_pro_jahr"]

st.sidebar.markdown('-'* 10)
st.sidebar.markdown('**Strompreis**')


st.sidebar.write(f"Grundpreis: {grundpreis_euro_pro_jahr} EUR/Jahr")
st.sidebar.write("Arbeitspreis pro kWh: "
    + f"{arbeitspreis_cent_pro_kWh} Cent/kWh")

gas_arbeitspreis_cent_pro_kwh = (preisliste
    [anbieter]["gas_arbeitspreis_cent_pro_kwh"])
gas_grundpreis_euro_pro_jahr = (preisliste
    [anbieter]["gas_grundpreis_euro_pro_jahr"])
st.sidebar.markdown('-'* 10)
st.sidebar.markdown('**Gaspreis**')


st.sidebar.write(f"Grundpreis: {gas_grundpreis_euro_pro_jahr} EUR/Jahr")
st.sidebar.write("Arbeitspreis pro kWh: "
    + f"{gas_arbeitspreis_cent_pro_kwh} Cent/kWh")
st.sidebar.markdown('-'* 10)

gesamt_wasser_grundpreis = preisliste[anbieter]["gesamt_wasser_grundpreis"]
arbeitspreis_trinkwasser_eur_m3 = (preisliste
    [anbieter]["arbeitspreis_trinkwasser_eur_m3"])

st.sidebar.markdown("**Trinkwasserpreis**")
st.sidebar.write(f"Grundpreis: {gesamt_wasser_grundpreis} EUR/Jahr")
st.sidebar.write("Arbeitspreis: "
    + f"{arbeitspreis_trinkwasser_eur_m3} EUR/m3")

st.sidebar.markdown("**Abwasserpreis**")
abwasser_preis_pro_m3 = preisliste[stadt]["abwasser_preis_pro_m3"]

st.sidebar.write(f"Grundpreis: {abwasser_preis_pro_m3} EUR/Jahr")

st.sidebar.markdown('-'* 10)

tab1, tab2 = st.tabs(["Energiekosten", "Charts"])

with tab1:
    st.header("Nebenkosten abschätzen")

    col1, col2 = st.columns((1,1))


    with col1:
        st.subheader('Stromkosten abschätzen:')

        verbrauch_kwh_pro_jahr = st.number_input(
            label='Ihr Stromverbrauch in kWh pro Jahr:',
            min_value = 0.0,
            value = 800.0,)

        gesamt_arbeitspreis_cent = (verbrauch_kwh_pro_jahr
            * arbeitspreis_cent_pro_kWh)

        gesamt_arbeitspreis_euro = np.round(gesamt_arbeitspreis_cent/100, 2)
        st.write(f"Strom Arbeitspreis: {gesamt_arbeitspreis_euro} EUR/Jahr")

        gesamt_strompreis = grundpreis_euro_pro_jahr + gesamt_arbeitspreis_euro
        st.write("Strom Bruttopreis: "
            + f"{np.round(gesamt_strompreis, 2)} EUR/Jahr")


        strompreis_monat = np.round(gesamt_strompreis/12,2)
        st.write("Durchschnittlicher Strompreis: "
            + f"{strompreis_monat} EUR/Monat")

    with col2:
        st.subheader('Wärmekosten abschätzen:')
        gas_verbrauch_kwh_pro_jahr = st.number_input(
            label='Ihr Gasverbrauch in kWh pro Jahr:',
            min_value = 0.0,
            value = 1000.0,)


        gas_arbeitspreis_cent_pro_jahr = (gas_verbrauch_kwh_pro_jahr *
            gas_arbeitspreis_cent_pro_kwh)
        gas_arbeitspreis_eur_pro_jahr = np.round(
            (gas_arbeitspreis_cent_pro_jahr/100), 2)

        gas_gesamtbrutto_preis =  np.round(
            (gas_arbeitspreis_eur_pro_jahr + gas_grundpreis_euro_pro_jahr), 2)

        st.write(f"Gas Arbeitspreis: {gas_arbeitspreis_eur_pro_jahr} EUR/Jahr")
        st.write(f"Gas Bruttopreis: {gas_gesamtbrutto_preis} EUR/Jahr")

        gaspreis_monat = np.round(gas_gesamtbrutto_preis/12,2)
        st.write(f"Durchschnittlicher Gaspreis: {gaspreis_monat} EUR/Monat")

    with col1:
        st.subheader('Trinkwasserkosten abschätzen:')

        trinkwasser_m3_pro_jahr = st.number_input(
            label='Ihr Trinkwasserverbrauch in m3 pro Jahr:',
            min_value = 0.0,
            value = 20.0,)

        gesamt_trinkwasser_pro_jahr = np.round(
            (trinkwasser_m3_pro_jahr * arbeitspreis_trinkwasser_eur_m3), 2)
        st.write("Trinkwasser Arbeitspreis: "
            + f"{gesamt_trinkwasser_pro_jahr} EUR/Jahr")

        gesamtkosten_trinkwasser = np.round(
            (gesamt_wasser_grundpreis + gesamt_trinkwasser_pro_jahr), 2)
        st.write("Trinkwasser Bruttopreis: "
            + f"{gesamtkosten_trinkwasser} EUR/Jahr")

        trinkwasserpreis_monat = np.round(gesamtkosten_trinkwasser/12, 2)
        st.write("Durchschnittlicher Trinkwasserpreis: "
            + f"{trinkwasserpreis_monat} EUR/Monat")

    with col2:
        st.subheader('Abwasserkosten abschätzen:')
        abwasser_m3_pro_jahr = st.number_input(
            label='Ihr Abwasserverbrauch in m3 pro Jahr:',
            min_value = 0.0,
            value = 20.0,)

        gesamtabwasser_kosten = np.round(
            (abwasser_m3_pro_jahr * abwasser_preis_pro_m3), 2)
        st.write(f"Gesamtpreis Abwasser: {gesamtabwasser_kosten}")

        abwasserpreis_monat = np.round(gesamtabwasser_kosten/12, 2)
        st.write("Durchschnittlicher Abwasserpreis: "
            + f"{abwasserpreis_monat} EUR/Monat")

    gesamtnebenkosten_pro_jahr = np.round((
        gesamtabwasser_kosten
        + gesamtkosten_trinkwasser
        + gas_gesamtbrutto_preis
        + gesamt_strompreis), 2)

    gesamtnebenkosten_pro_monat = np.round(gesamtnebenkosten_pro_jahr/12,2)

    col3, col4 = st.columns((1,1))

    with col3:
        st.subheader("Gesamtnebenkosten: ")

    with col4:
        st.subheader(f"{gesamtnebenkosten_pro_jahr} EUR/Jahr")
        st.subheader(f"{gesamtnebenkosten_pro_monat} EUR/Monat")

df_abschlag = pd.read_csv("data/abschlag.csv")

with tab2:
    st.header("Energiekosten visualisieren")

    stromabschlag_monat = st.number_input(
        label='Ihr Stromabschlag im Monat:',
        min_value = 0.0,
        value = 88.0,)

    wärmeabschlag_monat = st.number_input(
        label='Ihr Wärmeabschlag im Monat:',
        min_value = 0.0,
        value = 29.0,)

    wasserabschlag_monat = st.number_input(
        label='Ihr Trinkwasserabschlag im Monat:',
        min_value = 0.0,
        value = 25.0,)

    abwasserabschlag_monat = st.number_input(
        label='Ihr Abwasserabschlag im Monat:',
        min_value = 0.0,
        value = 13.0,)


    col1, col2 = st.columns((1,1))

    with col1:
        df_chart_monat = df_abschlag.copy().set_index("Kategorie")

        df_chart_monat["Kosten"] = df_chart_monat["Abschlag"]

        df_chart_monat["Abschlag"]["Strom"] = stromabschlag_monat
        df_chart_monat["Abschlag"]["Wärme"] = wärmeabschlag_monat
        df_chart_monat["Abschlag"]["Trinkwasser"] = wasserabschlag_monat
        df_chart_monat["Abschlag"]["Abwasser"] = abwasserabschlag_monat

        df_chart_monat["Kosten"]["Strom"] = strompreis_monat
        df_chart_monat["Kosten"]["Wärme"] = gaspreis_monat
        df_chart_monat["Kosten"]["Trinkwasser"] = trinkwasserpreis_monat
        df_chart_monat["Kosten"]["Abwasser"] = abwasserpreis_monat

        df_chart_monat["Differenz"] = (df_chart_monat["Abschlag"]
        - df_chart_monat["Kosten"])

        # Colorscale: px.colors.sequential.Magma[2::]

        fig = go.Figure()

        fig.add_trace(
            go.Bar(name='Abschlag',
                x=df_chart_monat.index,
                y=df_chart_monat.Abschlag,
                marker_color='#440f76'))
        fig.add_trace(
            go.Bar(name='Kosten',
                x=df_chart_monat.index,
                y=df_chart_monat.Kosten,
                marker_color='#9e2f7f'))

        fig.add_trace(
            go.Bar(name='Differenz',
                x=df_chart_monat.index,
                y=df_chart_monat.Differenz,
                marker_color='#fd9668'))

        # Change the bar mode
        fig.update_layout(barmode='group')

        fig.update_layout(
            title = 'Nebenkostenabschätzung im Monat',
            xaxis_title = "Kategorien",
            yaxis_title = "Summe [EUR]",
        )

        fig.update_xaxes(tickangle = 45)

        st.plotly_chart(fig)

    with col2:
        df_chart_jahr = df_abschlag.copy().set_index("Kategorie")

        df_chart_jahr["Abschlag"] = df_chart_jahr["Abschlag"] * 12
        df_chart_jahr["Kosten"] = df_chart_jahr["Abschlag"]

        df_chart_jahr["Abschlag"]["Strom"] = stromabschlag_monat * 12
        df_chart_jahr["Abschlag"]["Wärme"] = wärmeabschlag_monat * 12
        df_chart_jahr["Abschlag"]["Trinkwasser"] = wasserabschlag_monat * 12
        df_chart_jahr["Abschlag"]["Abwasser"] = abwasserabschlag_monat * 12

        df_chart_jahr["Kosten"]["Strom"] = gesamt_strompreis
        df_chart_jahr["Kosten"]["Wärme"] = gas_gesamtbrutto_preis
        df_chart_jahr["Kosten"]["Trinkwasser"] = gesamtkosten_trinkwasser
        df_chart_jahr["Kosten"]["Abwasser"] = gesamtabwasser_kosten

        df_chart_jahr["Differenz"] = (df_chart_jahr["Abschlag"]
            - df_chart_jahr["Kosten"])

        fig = go.Figure()

        fig.add_trace(
            go.Bar(name='Abschlag',
                x=df_chart_jahr.index,
                y=df_chart_jahr.Abschlag,
                marker_color='#440f76'))
        fig.add_trace(
            go.Bar(name='Kosten',
                x=df_chart_jahr.index,
                y=df_chart_jahr.Kosten,
                marker_color='#9e2f7f'))

        fig.add_trace(
            go.Bar(name='Differenz',
                x=df_chart_jahr.index,
                y=df_chart_jahr.Differenz,
                marker_color='#fd9668'))

        fig.update_layout(barmode='group')

        fig.update_layout(
            title = 'Nebenkostenabschätzung im Jahr',
            xaxis_title = "Kategorien",
            yaxis_title = "Summe [EUR]",
        )

        fig.update_xaxes(tickangle = 45)

        st.plotly_chart(fig)

    col3, col4 = st.columns((1,1))

    with col3:
        st.subheader("Gesamtdifferenz: ")

    with col4:

        gesamt_diff_monat = np.round(df_chart_monat["Differenz"].sum(), 2)
        gesamt_diff_jahr = np.round(df_chart_jahr["Differenz"].sum(), 2)
        st.subheader(f"{gesamt_diff_monat} EUR/Monat")
        st.subheader(f"{gesamt_diff_jahr} EUR/Jahr")
