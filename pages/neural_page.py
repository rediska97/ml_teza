import streamlit as st
from keras.models import Sequential
from keras.layers import Dense
import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler

def app():
    appstate = st.session_state
    
    errors_df = appstate.errors_df
    machines_df = appstate.machines_df
    maint_df = appstate.maint_df
    failures_df = appstate.failures_df
    telemetry_df = appstate.telemetry_df



    # LEFT JOIN la tabelul TELEMETRY cu FAILURES
    # SCHIMBAM TOTI NA CU DONE
    querry_data = telemetry_df.join(failures_df.set_index(['datetime','machineID']), on=['datetime','machineID'])
    querry_data['failure'] = querry_data['failure'].replace(np.nan, 'done')
    
    st.title("Implementarea retelelor neuronale pentru predictie starii automobilului")
    st.subheader("1. Extragerea datelor initiale din tabele")
    st.write('Vom pregati setul de date pentru a putea face studiu. Pentru aceasta v-om face',
            ' un join intre tabele *telemetry* si *failures*, iar campurile unde este absenta valoarea stării',
            'o vom considera ca buna (done). Tabelul rezultat este: ', querry_data)

    with st.expander("Statistica descriptiva a datelor din urma interogarii"):
        st.write(querry_data.describe())

    
    temp_table = querry_data[['volt', 'rotate', 'pressure', 'vibration', 'failure']]
    
    total_done_rows = temp_table[temp_table['failure'] == 'done']
        #Toate inregistrarile in care este vre-o defec'iune
    total_fail_rows = temp_table[temp_table['failure'] != 'done']
    

    st.subheader("2. Extragerea subeșantionului de date")
    #Extragem numarul selectat de inregistari dupa fiecare tip (cu defecte/ si fara )
    st.write("Datorita ca numarul totald de inregistrari cu defectiuni este:",
            total_done_rows.shape[0], 'iar fara :', total_fail_rows.shape[0],
            " vom extrage un subeșantion cu dimensiunile specificate de noi în **(Input)** ")
    

    def samplesize_callback():
        if 'mixed_data' in appstate:
            del appstate.mixed_data
        if 'trainEvent' in appstate:
            del appstate.trainEvent
        if 'train_X' in appstate:
            del appstate.train_X
        if 'model' in appstate:
            del appstate.model

        done_rows = total_done_rows.sample(n=appstate.nr_done_rows)
        fail_rows = total_fail_rows.sample(n=appstate.nr_fail_rows)
        appstate.mixed_data = done_rows.append(fail_rows, ignore_index=True).sample(frac=1)

       


    with st.form(key="samples_size"):
        col1, col2 = st.columns(2)
        with col1:
            label_done = "Numarul de inregistrari FĂRĂ defecte MAX(" + str(total_done_rows.shape[0]) + ")"
            st.number_input(label_done, key="nr_done_rows", value=3100, step=50, max_value=total_done_rows.shape[0])
        with col2:
            label_fail = "Numarul de inregistrari CU defecte MAX:(" + str(total_fail_rows.shape[0]) + ")"
            st.number_input(label_fail, key = "nr_fail_rows", value=500, step=50, max_value=total_fail_rows.shape[0])
        st.form_submit_button(label="Extrage subeșantionul", on_click=samplesize_callback)
            

    
    if 'mixed_data' in appstate:
        # Crearea matricei din date ce contin defectiuni si fara ele.
        # mixed_data = st.session_state.mixed_data
        # if 'mixed_data' not in st.session_state:
        #      = mixed_data
        st.write('Numarul de inregistrari extrase este:',appstate.mixed_data.shape[0],' iar inregistrarile din tabel le randomizăm, astfel obținem:', appstate.mixed_data)


        st.subheader("3. Normalizarea datelor si pregatirea pentru a antrena modelul retelei neuronale.")
        st.write('''Pentru antrenarea modelului reteli neuronale, esantionul de date trebuie imparțit în subeșantioane aproximativ \n80% - datele de antrenare, \n20% - datele de testare''')
        
        st.write('''Alta etapa importanta reprezinta separarea datelor din fiecare subeșantion în **X** și **Y**, unde: \n**X** - este alcătuit din coloanele ce 
                    descriu parametrii de lucru a mașinii",\n **Y** - reprezinta clasa care indica care component ar putea fi defectat!''')


        def normalizeDataCallback():
            #Selectionarea di datele mixate 80/20 pentru antrenare si testare
            appstate.train = appstate.mixed_data.sample(frac=0.8)
            appstate.test = appstate.mixed_data.drop(appstate.train.index)
            #separarea X si Y pentru antrenare
            appstate.train_X = appstate.train[['volt','rotate','pressure','vibration']]
            appstate.train_y = appstate.train['failure']
            #separarea X si Y pentru testare
            appstate.test_X = appstate.test[['volt','rotate','pressure','vibration']]
            appstate.test_y = appstate.test['failure']

            scaler = MinMaxScaler(feature_range=(0, 1))
            appstate.enc_train_X = scaler.fit_transform(appstate.train_X)
            appstate.enc_train_Y = pd.get_dummies(appstate.train_y)
        
            appstate.enc_test_X = scaler.fit_transform(appstate.test_X)
            appstate.enc_test_Y = pd.get_dummies(appstate.test_y)
            

        st.button(label="normalizarea datelor", key='normalize', on_click=normalizeDataCallback)
        
        if 'train_X' in appstate:
            rcol1, rcol2 = st.columns(2)
            with rcol1:
                st.info('**Datele pina la normalizare** ')
                st.caption("Valorile X")
                st.write(appstate.train_X)
                st.caption("Valorile Y")
                st.write(appstate.train_y)
            with rcol2:
                st.info("**Datele obtinute in urma normalizarii**")
                st.caption("Valorile X")
                st.write(appstate.enc_train_X)
                st.caption("Valorile Y")
                st.write(appstate.enc_train_Y)
            
            
            st.subheader('4. Atrenarea modelului, si prezicerea starii tehnice')
        
            def trainModelCallback():
                if 'model' in appstate:
                    del appstate.model

                model = Sequential()
                appstate.model = model
                # create model
                model.add(Dense(16, input_dim=4, activation='relu'))
                model.add(Dense(8, activation='relu'))
                model.add(Dense(5, activation=appstate.out_activate_func)) ##ultimul sloi sigmoid / softmax

                # Compile model
                model.compile(loss=appstate.model_loss_func, optimizer=appstate.optimize_func,metrics=['accuracy'])
                # model.compile(optimizer='adam', loss=SparseCategoricalCrossentropy(from_logits=True),metrics=['accuracy'])

                model.fit(appstate.enc_train_X, appstate.enc_train_Y, epochs=appstate.epoch_numbers, batch_size=appstate.batch_size,  verbose=0)
                appstate.model = model

            with st.form(key= 'train_model'):
                st.info("introduceti parametrii de configurare doriti")
                st.number_input(label = "Numarul de epoci", value=60, step=1, key='epoch_numbers')
                st.number_input(label = "Marimea setului de date / epoca", value=24, step=1, key='batch_size')
                st.radio(label="functia de activare la iesire", options=('sigmoid','softmax'), key='out_activate_func')
                st.radio(label="functia de optimizare", options= ('adam','sgd'), key ='optimize_func')
                st.radio(label="Loss function", options= ('categorical_crossentropy','binary_crossentropy','mean_squared_error'), key='model_loss_func')

                if 'model' in appstate:
                    model = appstate.model
                    with st.spinner('Antrenarea Modelului creat Datelor si prezicerea starii'):
                        test_loss, test_acc = model.evaluate(appstate.enc_test_X, appstate.enc_test_Y)
                        st.write("Denumire Metriciii", model.metrics_names[1])
                        st.write("Test loss:",test_loss)
                        st.write("Test Accuracy:",test_acc)
                button = st.form_submit_button(label="Configurarea și Antrenarea retelei", on_click=trainModelCallback)


            with st.form("introducerea valorilor pentru prezicere"):
                stat = appstate.mixed_data.describe().T[['min','max']]
                st.write(stat)
                c1,c2,c3,c4 = st.columns(4)
                with c1:
                    input_volt = st.number_input("Introduceti voltajul", value=110, step=10)
                    input_volt_norm = (input_volt - stat.loc['volt']['min'])/(stat.loc['volt']['max'] - stat.loc['volt']['min'])
                with c2:
                    input_rotate = st.number_input("Introduceti rotatiile", value= 270, step=10)
                    input_rotate_norm = (input_rotate - stat.loc['rotate']['min'])/(stat.loc['rotate']['max'] - stat.loc['rotate']['min'])
                with c3:
                    input_pressure = st.number_input("Introduceti presiunea", value = 120, step=10)
                    input_pressure_norm = (input_pressure - stat.loc['pressure']['min'])/(stat.loc['pressure']['max'] - stat.loc['pressure']['min'])
                with c4:
                    input_vibration = st.number_input("Introduceti vibratiile", value = 30, step=10)
                    input_vibration_norm = (input_vibration - stat.loc['vibration']['min'])/(stat.loc['vibration']['max'] - stat.loc['vibration']['min'])
            
                predict = st.form_submit_button("Faceti prezicerea")    
                if predict:
                    prediction = appstate.model.predict([[input_volt_norm,
                                input_rotate_norm,
                                input_pressure_norm,
                                input_vibration_norm]])
                    
                    st.write('''Ca rezultat ne va fi returnat un tabel unde ne este indicat carei clase ii 
                    apartine starea selectata. Pentru a putea descifra, ne uitam numarul la coloana din 
                    tabelul rezultat, cu tabelul normalizat **Y**.''',prediction)