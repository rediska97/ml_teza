import streamlit as st

def app(params):
    errors_df = params["errors_df"]
    machines_df = params["machines_df"]
    maint_df = params["maint_df"]
    failures_df = params["failures_df"]
    telemetry_df = params["telemetry_df"]


    st.write("Abc analiza ")