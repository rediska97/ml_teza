from distutils.log import error
from matplotlib.pyplot import axis
import streamlit as st

def app():
    appstate = st.session_state
    
    errors_df = appstate.errors_df
    machines_df = appstate.machines_df
    maint_df = appstate.maint_df
    failures_df = appstate.failures_df
    telemetry_df = appstate.telemetry_df


    st.title("Utilizarea metodei de analiza ABC")

    st.subheader("Despre analiza ABC")
    st.write('''
        Clasificarea ABC se bazează pe principiul Pareto, sau **regula 80/20**, care spune că **80%** din 
        vânzări vor proveni din **20%** din produse. Acesta împarte produsele în trei clase - **A**, **B** și 
        **C** - în funcție de criterii specifice, cum ar fi volumul vânzărilor sau "utilizarea anuală 
        a dolarului" pe baza veniturilor din vânzări din ultimele 12 luni. Clasificarea 
        fiecărui produs este apoi utilizată pentru a controla inventarul produsului și pentru a 
        determina politica de comandă pentru fiecare articol.
    ''')

    st.subheader("Efectuarea Analizei")
    st.write('''
        Pentru rezolvarea problemei de mentenanta, vom adapta metoda ABC la esantionul de date al nostru.
        \nIn datele care sunt analizate este descrisă starea de lucru a automobilului și prezența defectului
        caruiva component.
        \nVom analiza care component implica cele mai multe defectiuni, iar care mai putin.
    ''')

    abc_df = failures_df[['machineID','failure']]
    abc_size = abc_df.shape[0]

    
    # st.write(list(abc_df))

    st.write("numarul total de inregistrari este", abc_size, abc_df)

    # df.Color.value_counts().reset_index().rename(
        #    columns={'index': 'Color', 0: 'count'})
    
    abc_grouped = abc_df['failure'].value_counts().reset_index().rename(
        columns={'index':'component', 0: 'count'}
    )

    # abc_grouped = abc_df.groupby(['failure'])['failure'].count()

    # abc_grouped.rename(columns = {"failure": "defect_per_component"})

    st.write("* **Grupam datele dupa defectiuni, si numaram cate defectiuni are fiecare** *", abc_grouped)

    # st.write(list(abc_df))
    abc_grouped['percentage'] = abc_grouped.apply(lambda row : (row.failure * 100 / abc_size), axis=1)    
    
    st.write('''* **Apoi calculam procentajul de aparitie a fiecarei defectiuni față de numarul total:** *''',abc_grouped)


    st.subheader('Selectarea ponderii fiecarui grup (A, B, C)')

    slider_range = st.slider("Alegeti intervalul",value=[5,70], min_value=1, max_value=99)

    col1,col2,col3 = st.columns(3)
    with col1:
        st.write('**Intervalul clasei C:**',0 ,'%-', slider_range[0], "%")
    with col2:
        st.write('**Intervalul clasei B:**',slider_range[0] ,'%-', slider_range[1], "%")
    with col3:
        st.write('**Intervalul clasei A:**',slider_range[1] ,'%-', 100, "%")
    

    def clasify_component1(row):
        if row > 0 and row <= slider_range[0]:
            return 'C'
        elif row > slider_range[0] and row <=slider_range[1]:
            return 'B'
        else:
            return 'A'

    abc_grouped['abc_class'] = abc_grouped.apply(lambda row : clasify_component1(row['percentage']), axis=1) 
    

    st.write("* **atribuim fiecarei component clasa ABC** *", abc_grouped)  
