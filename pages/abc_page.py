import streamlit as st

def app():
    appstate = st.session_state
    
    errors_df = appstate.errors_df
    machines_df = appstate.machines_df
    maint_df = appstate.maint_df
    failures_df = appstate.failures_df
    telemetry_df = appstate.telemetry_df


    st.write("Abc analiza ")