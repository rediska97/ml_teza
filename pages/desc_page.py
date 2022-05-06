import streamlit as st
from loadFiles import telemetry_df,errors_df,maint_df,failures_df,machines_df

def app():
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
    if st.button('Arata tabelul',key = 'telemetry'):
        st.write(telemetry_df.sample(100))
    
    st.download_button(
        label="Descarca tabelul",
        data=telemetry_df.to_csv(index=False).encode('utf-8'),
        file_name='Telemetry.csv',
        mime='text/csv',
    )

    st.write('**Tabelul Errori**, numarul de înregistrări:', errors_df.size)
    if st.button('Arata tabelul', key = 'errors'):
        st.write(errors_df.sample(100))
    
    st.download_button(
        label="Descarca tabelul",
        data=errors_df.to_csv(index=False).encode('utf-8'),
        file_name='errors.csv',
        mime='text/csv',
    )

    st.write('**Tabelul Maintenance**, numarul de înregistrări:', maint_df.size)
    if st.button('Arata tabelul',key = 'maintenance'):
        st.write(maint_df.sample(100))
    
    st.download_button(
        label="Descarca tabelul",
        data=maint_df.to_csv(index=False).encode('utf-8'),
        file_name='maintenance.csv',
        mime='text/csv',
    )
    st.write('**Tabelul Esecuri**, numarul de înregistrări:', failures_df.size)
    if st.button('Arata tabelul', key = 'failures'):
        st.write(failures_df.sample(100))
    
    st.download_button(
        label="Descarca tabelul",
        data=failures_df.to_csv(index=False).encode('utf-8'),
        file_name='failures.csv',
        mime='text/csv',
    )
    st.write('**Tabelul Masini**, numarul de înregistrări:', machines_df.size)
    if st.button('Arata tabelul', key = 'machines'):
        st.write(machines_df.sample(100))
    
    st.download_button(
        label="Descarca tabelul",
        data=machines_df.to_csv(index=False).encode('utf-8'),
        file_name='machines.csv',
        mime='text/csv',
    )

