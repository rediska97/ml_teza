import streamlit as st


def app(params):
    errors_df = params["errors_df"]
    machines_df = params["machines_df"]
    maint_df = params["maint_df"]
    failures_df = params["failures_df"]
    telemetry_df = params["telemetry_df"]

    st.title("UTM - Gestionarea stării tehnice utilizând metode de data mining")
    st.write('''
    **Datele necesare pentru o mentenanță predictivă ar putea fi:**
    \nStarea automobilului - *Este descrisă starea de lucru a mașinei cu ajutorul datelor colectate de la senzori*
    \nIstoricul defecțiunilor - *Istoricul defecțiunilor unei mașini sau componente din cadrul mașinii.*
    \nIstoricul întreținerii - *Istoricul reparațiilor unei mașini, de exemplu coduri de eroare, activități de întreținere anterioare sau înlocuirea cărorva componente.*
    \nCaracteristicile mașinii: *caracteristicile unei mașini, de exemplu, dimensiunea motorului, marca și modelul, locația anul.*
    ''')

    st.subheader("Datele propuse spre analiză")
    with st.expander(" Detalii despre date:"):
        st.write('**Telemetrie** *(telemetry)* - Date înregistrate sub formă *Serie de timp*: se compune din media pentru fiecare oră a parametrilor de tensiune, rotație, presiune, vibrații colectate de la 100 de mașini pentru anul 2015.')
        st.write(''' **Erori** *(errors)* - acestea sunt erori întâlnite de mașini în timp ce sunt în stare de funcționare. Deoarece, aceste erori nu opresc funcționarea mașinii, 
                acestea nu sunt considerate ca defecțiuni. Data și orele de eroare sunt rotunjite la cea mai apropiată oră, deoarece datele de telemetrie se păstrează pe ore.''')
        st.write(''' **Mentenanța** *maintenance* - dacă o componentă a unei mașini este înlocuită, aceasta este înregistrată tabel. Componentele sunt înlocuite în două situații: 
            \n1. În timpul vizitei regulate programate, tehnicianul a înlocuit-o (întreținere proactivă) 
            \n2. Se defectează o componentă și tehnicianul face o întreținere neprogramată pentru a o înlocui (întreținere reactivă). 
            \nAcest lucru este considerat ca un eșec/defect și datele corespunzătoare sunt înregistrate în tabelul *defecțiuni*. 
            \nDatele de întreținere au atât înregistrări din 2014, cât și din 2015. Aceste date sunt rotunjite la cea mai apropiată oră, deoarece datele de telemetrie sunt colectate la o rată orară.''') 
        st.write('**Defecțiuni/Eșecuri** *(errors)* - fiecare înregistrare reprezintă înlocuirea unei componente din cauza eșecului. Aceste date sunt un subset de date de întreținere. Aceste date sunt rotunjite la cea mai apropiată oră, deoarece datele de telemetrie sunt colectate la o rată orară.')
        st.write('**Metadatele automobilelor** *machines* - Modelul și vârsta .')
        

    st.write('**Tabelul Errori**, numarul de înregistrări:', errors_df.shape[0])
    if st.button('Arata tabelul', key = 'errors'):
        st.write(errors_df.sample(100))
    

    st.download_button(
        label="Descarca tabelul",
        data=errors_df.to_csv(index=False).encode('utf-8'),
        file_name='errors.csv',
        mime='text/csv',
    )

    st.write('**Tabelul Maintenance**, numarul de înregistrări:', maint_df.shape[0])
    if st.button('Arata tabelul',key = 'maintenance'):
        st.write(maint_df.sample(100))
    

    st.download_button(
        label="Descarca tabelul",
        data=maint_df.to_csv(index=False).encode('utf-8'),
        file_name='maintenance.csv',
        mime='text/csv',
    )
    st.write('**Tabelul Esecuri**, numarul de înregistrări:', failures_df.shape[0])
    if st.button('Arata tabelul', key = 'failures'):
        st.write(failures_df.sample(100))


    st.download_button(
        label="Descarca tabelul",
        data=failures_df.to_csv(index=False).encode('utf-8'),
        file_name='failures.csv',
        mime='text/csv',
    )
    st.write('**Tabelul Masini**, numarul de înregistrări:', machines_df.shape[0])
    if st.button('Arata tabelul', key = 'machines'):
        st.write(machines_df.sample(100))


    st.download_button(
        label="Descarca tabelul",
        data=machines_df.to_csv(index=False).encode('utf-8'),
        file_name='machines.csv',
        mime='text/csv',
    )

    st.write('**Tabelul (Telemetrie)**, numarul de înregistrări:' , telemetry_df.shape[0])
    
    if st.button('Arata tabelul',key = 'telemetry'):
        st.write(telemetry_df.sample(100))


    # with st.spinner('Preparing data to download'):
    #     st.download_button(
    #     label="Descarca tabelul",
    #     data=telemetry_df.to_csv(index=False).encode('utf-8'),
    #     file_name='Telemetry.csv',
    #     mime='text/csv',
    # )
    
