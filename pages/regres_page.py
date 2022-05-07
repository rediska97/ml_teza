import streamlit as st
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

from helpers import regression as regr


def app(params):
    errors_df = params["errors_df"]
    machines_df = params["machines_df"]
    maint_df = params["maint_df"]
    failures_df = params["failures_df"]
    telemetry_df = params["telemetry_df"]


    st.subheader("Analiza datelor utilizand metoda regresiei")

    erros_across_machine = errors_df.groupby("machineID").size()

    erros_across_machine = pd.DataFrame(erros_across_machine, columns=["num_errors"]).reset_index()

    machines_errors_df = pd.merge(machines_df, erros_across_machine, how='left', on="machineID")

    # Create a DF consisting of number of maintenance records across Machines
    maint_across_machine = maint_df.groupby("machineID").size()
    maint_across_machine = pd.DataFrame(maint_across_machine, columns=["num_maint"]).reset_index()

    machines_errors_df = pd.merge(machines_errors_df, maint_across_machine, how='left', on="machineID")

    # Create a DF consisting of number of failure records across Machines
    failure_across_machine = failures_df.groupby("machineID").size()
    failure_across_machine = pd.DataFrame(failure_across_machine, columns=["num_failure"]).reset_index()

    machines_errors_df = pd.merge(machines_errors_df, failure_across_machine, how='left', on="machineID")


    # querry_data = telemetry_df.join(failures_df.set_index(['datetime','machineID']), on=['datetime','machineID'])
    # querry_data = querry_data.groupby(querry_data['failure'])

    def drawRegressChart(x,y,title = "Titlul grafic"):
        y_pred = regr.lin_regress(x,y)
        plt.scatter(x,y)
        plt.title(title)
        plt.plot(x, y_pred, color='red')
        st.pyplot(plt)
        



    plot1 = plt.figure()
    x=machines_errors_df[['age']]
    y=machines_errors_df[['num_errors']]
    titlu = "Aparitiie erorilor in dependenta de ani"
    drawRegressChart(x,y,titlu)




    plot2 = plt.figure()
    x = machines_errors_df[['age']]
    y = machines_errors_df[['num_maint']]
    drawRegressChart(x,y)


    # plot3 = plt.figure()
    # x=querry_data[['volt']]
    # y=machines_errors_df[['num_errors']]
    # titlu = "Aparitiie erorilor in dependenta de ani"
    # drawRegressChart(x,y,titlu)


