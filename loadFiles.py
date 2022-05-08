import streamlit as st
import pandas as pd


@st.cache
def get_data():
    telemetry_df = pd.read_csv(f"data/pdm/PdM_telemetry.csv")
    # telemetry_df.to_csv('telemetry.csv.gz', compression='gzip', index=False)
    # telemetry_df = pd.read_csv(f"data/pdm/telemetry.csv.gz")
    errors_df = pd.read_csv(f"data/pdm/PdM_errors.csv")
    maint_df = pd.read_csv(f"data/pdm/PdM_maint.csv")
    failures_df = pd.read_csv(f"data/pdm/PdM_failures.csv")
    tables = [telemetry_df, maint_df, failures_df, errors_df]

    for df in tables:
        df["datetime"] = pd.to_datetime(df["datetime"], format="%Y-%m-%d %H:%M:%S")
        df.sort_values(["datetime", "machineID"], inplace=True, ignore_index=True)
     
    st.session_state.telemetry_df = telemetry_df
    st.session_state.errors_df = errors_df 
    st.session_state.maint_df = maint_df
    st.session_state.failures_df = failures_df
    st.session_state.machines_df = pd.read_csv(f"data/pdm/PdM_machines.csv")
    st.session_state.loadFromFiles = True

