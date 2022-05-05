import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import regression as regr

from loadFiles import telemetry_df,errors_df,maint_df,failures_df,machines_df
from pages import neural_page,regres_page, desc_page

from navigator import Navigator


st.write("# UTM ")
st.title('Gestionarea stării tehnice utilizând metode de data mining')

st.header('Prepararea datelor pentru analiza')
st.write('''
Condițiile și utilizarea mașinii: *condițiile de funcționare ale unei mașini, de exemplu datele colectate de la senzori.*
\nIstoricul defecțiunilor: *Istoricul defecțiunilor unei mașini sau componente din interiorul mașinii.*
\nIstoricul întreținerii: *istoricul reparațiilor unei mașini, de exemplu coduri de eroare, activități de întreținere anterioare sau înlocuiri de componente.*
\nCaracteristicile mașinii: *caracteristicile unei mașini, de exemplu, dimensiunea motorului, marca și modelul, locația.*
''')



with st.expander(" Detalii despre date:"):
    st.write('Datele **Serie de timp** Telemetrie (_PdM_telemetry.csv_): se compune din media orară de tensiune, rotație, presiune, vibrații colectate de la 100 de mașini pentru anul 2015.')
    st.write('''Eroare (_PdM_errors.csv_): acestea sunt erori întâlnite de mașini în timp ce sunt în stare de funcționare. Deoarece, aceste erori nu închide mașinile, 
            acestea nu sunt considerate ca eșecuri. Data și orele de eroare sunt rotunjite la cea mai apropiată oră, deoarece datele de telemetrie sunt colectate la o rată orară.''')
    st.write('''Întreținere (_PdM_maint.csv_): dacă o componentă a unei mașini este înlocuită, aceasta este capturată ca o înregistrare în acest tabel. Componentele sunt înlocuite în două situații: 
        \n1. În timpul vizitei regulate programate, tehnicianul a înlocuit-o (întreținere proactivă) 
        \n2. O componentă se descompune și apoi tehnicianul face o întreținere neprogramată pentru a înlocui componenta (întreținere reactivă). 
        \nAcest lucru este considerat ca un eșec și datele corespunzătoare sunt capturate în eșecuri. Datele de întreținere au atât înregistrări din 2014, cât și din 2015. Aceste date sunt rotunjite la cea mai apropiată oră, deoarece datele de telemetrie sunt colectate la o rată orară.''') 
    st.write('Eșecuri (_PdM_failures.csv_): fiecare înregistrare reprezintă înlocuirea unei componente din cauza eșecului. Aceste date sunt un subset de date de întreținere. Aceste date sunt rotunjite la cea mai apropiată oră, deoarece datele de telemetrie sunt colectate la o rată orară.')
    st.write('Metadate de mașini (_PdM_Machines.csv_): Tipul modelului și vârsta mașinilor.')
    # if st.button('Arata tabelul (Machines)'):
    #     machines_df
    



st.write('**Tabelul (Telemetrie)**, numarul de înregistrări:' , telemetry_df.size)
telemetry_df
st.write('**Tabelul Errori**, numarul de înregistrări:', errors_df.size)
errors_df
st.write('**Tabelul Maintenance**, numarul de înregistrări:', maint_df.size)
maint_df
st.write('**Tabelul Esecuri**, numarul de înregistrări:', failures_df.size)
failures_df
st.write('**Tabelul Masini**, numarul de înregistrări:', machines_df.size)
machines_df




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




erros_across_machine
machines_errors_df

'errors'



# telemetry_df['datetime'] = pd.to_datetime(telemetry_df["datetime"])
# telemetry_df['datetime'] = telemetry_df['datetime'].map(dt.datetime.toordinal)


# x = telemetry_df[['datetime']]
# x 
# y = telemetry_df[['vibration']]
# y




plt.scatter(machines_errors_df['age'], machines_errors_df['num_errors'])
# plt.plot(x, y_pred, color='red')
plt.show()
st.pyplot(plt)

'tables'



print(f"Shape of the Telemetry Records: {telemetry_df.shape}")
print("\n")
telemetry_df.head()

# X = date[['temp', 'rpm', 'voltage']].values

# Y = date['starea'].values

# x=date[['temp']]
# y=date[['starea']]

# linear_regressor = LinearRegression()  # create object for the class
# linear_regressor.fit(x, y)  # perform linear regression
# Y_pred = linear_regressor.predict(x)  # make predictions


# plt.scatter(x, y)
# 
# plt.show()
# st.pyplot(plt)


# import streamlit as st
# import utils as utl
# from views import home,predict



# def navigation():
#     route = utl.get_current_route()
#     if route == "home":
#         home.load_view()
#     elif route == "predict":
#         predict.load_view()
#     elif route == "analysis":
#         analysis.load_view()
#     elif route == "options":
#         options.load_view()
#     elif route == "configuration":
#         configuration.load_view()
#     elif route == None:
#         home.load_view()
        
# navigation()

# PAGES = {
#     "Train": "app1",
#     "Predict": "app2"
# }

# st.sidebar.title('Navigation')
# st.sidebar.selectbox("Go To", list(PAGES.keys()))

# selection = st.sidebar.radio("Go to", list(PAGES.keys()))
# page = PAGES[selection]
# page.app()


# with st.sidebar:
#     selected = option_men

# pages = {'Descrierea Datelor':'about_data','Posting':'posting'}
# choice = st.sidebar.radio("Pagina: ",tuple(pages.keys()))

# 'choice>>>',choice
# # pages[choice]()

# if(choice == 'about_data'):
#     'page1'
# elif (choice == 'posting'):
#     'page2'
# else:
#     'error'




# Create an instance of the app 
app = Navigator()

# Title of the main page
st.title("Data Storyteller Application")

# Add all your applications (pages) here
app.add_page("Descriere", desc_page.app)
app.add_page("Upload Data", neural_page.app)
app.add_page("Change Metadata", regres_page.app)

# The main app
app.run()
