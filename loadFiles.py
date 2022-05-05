import pandas as pd

telemetry_df = pd.read_csv(f"data/pdm/PdM_telemetry.csv")
errors_df = pd.read_csv(f"data/pdm/PdM_errors.csv")
maint_df = pd.read_csv(f"data/pdm/PdM_maint.csv")
failures_df = pd.read_csv(f"data/pdm/PdM_failures.csv")
machines_df = pd.read_csv(f"data/pdm/PdM_machines.csv")

tables = [telemetry_df, maint_df, failures_df, errors_df]
for df in tables:
    df["datetime"] = pd.to_datetime(df["datetime"], format="%Y-%m-%d %H:%M:%S")
    df.sort_values(["datetime", "machineID"], inplace=True, ignore_index=True)