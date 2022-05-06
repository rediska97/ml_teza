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
    return tables

all_tables = get_data()

telemetry_df = all_tables[0]
maint_df = all_tables[1]
failures_df = all_tables[2]
errors_df = all_tables[3]
machines_df = pd.read_csv(f"data/pdm/PdM_machines.csv")