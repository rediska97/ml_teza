import streamlit as st
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

from helpers import regression as regr


def app():
    appstate = st.session_state
    
    errors_df = appstate.errors_df
    machines_df = appstate.machines_df
    maint_df = appstate.maint_df
    failures_df = appstate.failures_df
    telemetry_df = appstate.telemetry_df

    st.subheader("Analiza datelor utilizand metoda regresiei")

    erros_across_machine = errors_df.groupby("machineID").size()
    erros_across_machine = pd.DataFrame(erros_across_machine, columns=["num_errors"]).reset_index()

    

    # Create a DF consisting of number of maintenance records across Machines
    maint_across_machine = maint_df.groupby("machineID").size()
    maint_across_machine = pd.DataFrame(maint_across_machine, columns=["num_maint"]).reset_index()
    

    # Create a DF consisting of number of failure records across Machines
    failure_across_machine = failures_df.groupby("machineID").size()
    failure_across_machine = pd.DataFrame(failure_across_machine, columns=["num_failure"]).reset_index()

    machines_errors_df = pd.merge(machines_df, erros_across_machine, how='left', on="machineID")
    machines_errors_df = pd.merge(machines_errors_df, maint_across_machine, how='left', on="machineID")
    machines_errors_df = pd.merge(machines_errors_df, failure_across_machine, how='left', on="machineID")

    st.write(machines_errors_df)


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
    titlu = "numarul de interventii(mentenanta) in dependenta de virsta auto"
    drawRegressChart(x,y,titlu)


    querry = maint_df.join(machines_df.set_index(['machineID']), on=['machineID'])
    querry_grouped = querry.groupby(['age'])['comp'].count().reset_index()

    plot3 = plt.figure()
    x = querry_grouped[['age']]
    y = querry_grouped[['comp']]
    titlu = "Numarul de componente schimbate, in dependenta de varsta masinii"
    drawRegressChart(x,y,titlu)
