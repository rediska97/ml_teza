import streamlit as st
import pandas as pd

from pages import neural_page,regres_page, desc_page

from navigator import Navigator

# from loadFiles import telemetry_df,errors_df,maint_df,failures_df,machines_df
from loadFiles import get_data



# data = {
#     "telemetry_df": telemetry_df,
#     "errors_df": errors_df,
#     "maint_df": maint_df,
#     "failures_df": failures_df,
#     "machines_df": machines_df
# }

with st.spinner('Încarcarea Datelor'):
    data = get_data()



app = Navigator()


st.title("UTM - Gestionarea stării tehnice utilizând metode de data mining")

app.add_page("Descriere", desc_page.app)
app.add_page("Regresie", regres_page.app)
app.add_page("Retele Neuronale", neural_page.app)


# The main app
app.run(data)


# telemetry_df['datetime'] = pd.to_datetime(telemetry_df["datetime"])
# telemetry_df['datetime'] = telemetry_df['datetime'].map(dt.datetime.toordinal)


# x = telemetry_df[['datetime']]
# x 
# y = telemetry_df[['vibration']]
# y






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




