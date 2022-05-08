import streamlit as st
import pandas as pd

from pages import neural_page,regres_page, desc_page, abc_page

from navigator import Navigator

# from loadFiles import telemetry_df,errors_df,maint_df,failures_df,machines_df
from loadFiles import get_data

appstate = st.session_state


with st.spinner('Încarcarea Datelor'):
    x = get_data()
    appstate.telemetry_df = x["telemetry_df"]
    appstate.errors_df = x["errors_df"]
    appstate.maint_df = x["maint_df"]
    appstate.failures_df = x["failures_df"]
    appstate.machines_df = x["machines_df"]


st.sidebar.caption("Elaborat de: Boronciuc Andrei masterand MAI-201M")
st.sidebar.caption("Cu suportul: Perebinos Mihail dr.conf.univ")
st.sidebar.title("Navigare")

app = Navigator()
app.add_page("Analiza ABC", abc_page.app)
app.add_page("Descriere", desc_page.app)
app.add_page("Regresie", regres_page.app)
app.add_page("Retele Neuronale", neural_page.app)


# The main app
app.run()
