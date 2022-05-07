import streamlit as st
from keras.models import Sequential
from keras.layers import Dense
import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler

def app(params):
    errors_df = params["errors_df"]
    machines_df = params["machines_df"]
    maint_df = params["maint_df"]
    failures_df = params["failures_df"]
    telemetry_df = params["telemetry_df"]

    st.sidebar.multiselect("Alegeti coloanele",params.keys()) ## test un select in sidebar (stinga)

    
    # LEFT JOIN la tabelul TELEMETRY cu FAILURES
    # SCHIMBAM TOTI NA CU DONE
    querry_data = telemetry_df.join(failures_df.set_index(['datetime','machineID']), on=['datetime','machineID'])
    querry_data['failure'] = querry_data['failure'].replace(np.nan, 'done')
    
    st.title("Implementarea retelelor neuronale pentru predictie starii automobilului")
    st.write('Vom pregati setul de date pentru a putea face studiu. Pentru aceasta v-om face',
            ' un join intre tabele *telemetry* si *failures*. Tabelul rezultat este: ', querry_data)

    with st.expander("Statistica descriptiva a datelor din urma interogarii"):
        st.write(querry_data.describe())

    
    temp_table = querry_data[['volt', 'rotate', 'pressure', 'vibration', 'failure']]
    

    #Toate inregistrarile in care nu este nici o  defectiune
    total_done_rows = temp_table[temp_table['failure'] == 'done']
    #Toate inregistrarile in care este vre-o defec'iune
    total_fail_rows = temp_table[temp_table['failure'] != 'done']

    #Extragem numarul selectat de inregistari dupa fiecare tip (cu defecte/ si fara )
    st.write("Datorita ca numarul totald de inregistrari cu defectiuni este:",
            total_done_rows.shape[0], 'iar fara :', total_fail_rows.shape[0],
            " vom extrage un subeșantion cu dimensiunile specificate de noi în * **Input** *")


    col1, col2 = st.columns(2)
    with col1:
        label_done = "Numarul de inregistrari FĂRĂ defecte MAX(" + str(total_done_rows.shape[0]) + ")"
        nr_done_rows = st.number_input(label_done, min_value=1, value=1800, step=50, max_value=total_done_rows.shape[0])
        done_rows = total_done_rows.sample(n=nr_done_rows,random_state = 1)
    with col2:
        label_fail = "Numarul de inregistrari CU defecte MAX:(" + str(total_fail_rows.shape[0]) + ")"
        nr_fail_rows = st.number_input(label_fail, min_value=1, value=500, step=50, max_value=total_fail_rows.shape[0])
        fail_rows = total_fail_rows.sample(n=nr_fail_rows,random_state = 1)

    

    
    # Crearea matricei din date ce contin defectiuni si fara ele.
    

    mixed_data = done_rows.append(fail_rows, ignore_index=True).sample(frac=1)

    status_by_code = dict(enumerate(mixed_data['failure'].unique()))
    code_by_status = {v: k for k, v in status_by_code.items()}

    mixed_data = mixed_data.replace({"failure":code_by_status})

    # with col1:
    #     st.write('status dict:',status_by_code)
    
    # with col2:
    #     st.write('code by status dict:', code_by_status)
  

    st.write("Dupa ce am extras un subesantion cu numarul total de inregistrari:",mixed_data.shape[0],
        'codificam coloana "failure" pentru a putea antrena modelul retelei. Astfel tabelul este',mixed_data)
    with st.expander("Statistica descriptiva a datelor"):
        st.write(mixed_data.describe())


    st.write("""Pentru antrenarea modelului retelei neuronale, avem nevoie de a împărți tabelul nostru în 2 seturi,
            iar ele la randul lor de date în 2: **X** și **Y**, unde: \n**X** - este alcătuit din coloanele ce 
            descriu parametrii de lucru a mașinii",\n **Y** - reprezinta clasa care component ar putea fi defectat!""")

    st.write("**Extragerea** datelor pentru antrenare si testare a modelului")
    train = mixed_data.sample(frac=0.8, random_state=200)
    test = mixed_data.drop(train.index)
    rcol1, rcol2 = st.columns(2)
    with rcol1:
        if st.button('Arata tabelul valorilor de antrenare'):
            st.write(train)
        if st.button('Statistica descriptiva a tabelului X'):
            st.write('train',train.describe())
    with rcol2:
        if st.button('Arata tabelul valorilor  de testare'):
            st.write(test)
        if st.button('Statistica descriptiva a tabelului testare'):
            st.write(test.describe())
            
    


    st.subheader('Analiza cu ajutorul Rețelelor neuronale')
    st.write("**Crearea datelor de intrare X ce descriu parametrii de lucru a masinii si le scalam intre valorile de 0 si 1**")
    
    X_train = train[['volt','rotate','pressure','vibration']]
    y_train = train['failure']
    
    X_test = test[['volt','rotate','pressure','vibration']]
    y_test = test['failure']
    
    scaler = MinMaxScaler(feature_range=(0, 1))
    encoded_train_X = scaler.fit_transform(X_train)
    # encoded_train_X = pd.DataFrame(encoded_train_X)

    encoded_train_Y = pd.get_dummies(y_train)
    ## for test
    encoded_test_X = scaler.fit_transform(X_test)
    # encoded_test_X = pd.DataFrame(encoded_test_X)

    encoded_test_Y = pd.get_dummies(y_test)

    st.write('Datele scalate a valorilor de intrare X pentru antrenarea retelei:', encoded_train_X)

    # st.write('encodedX:', encoded_X)
    # st.write('encoded______ :', )
    # st.write("Decoded _____: ", pd.get_dummies(y_train).idxmax(axis=1))
   
    model = Sequential()
    train_event = st.button("1. Antrenarea  modelului")

    if train_event:
        with st.spinner('Antrenarea Modelului creat Datelor si prezicerea starii'):
            # create model
            model.add(Dense(40, input_dim=4, activation='relu'))
            model.add(Dense(15, activation='relu'))
            model.add(Dense(4, activation='relu'))
            model.add(Dense(5, activation='sigmoid')) ##ultimul sloi sigmoid / softmax

            # Compile model
            # model.compile(optimizer='adam', loss=SparseCategoricalCrossentropy(from_logits=True),metrics=['accuracy'])
            model.compile(loss='categorical_crossentropy', optimizer='adam',metrics=['accuracy'])
            # model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
            # model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
            # model.compile(loss='binary_crossentropy', optimizer='sgd', metrics=['accuracy'])

            # # Fit the model
            model.fit(encoded_train_X, encoded_train_Y, epochs=300, batch_size=64,  verbose=0)
            test_loss, test_acc = model.evaluate(encoded_test_X, encoded_test_Y)
            st.write("Denumire Metriciii", model.metrics_names[1])
            st.write("Test loss:",test_loss)
            st.write("Test Accuracy:",test_acc)
   


    with st.form("introducerea valorilor pentru prezicere"):
        stat = mixed_data.describe().T[['min','max']]
        st.write(stat)
        c1,c2,c3,c4 = st.columns(4)
        with c1:
            input_volt = st.number_input("Introduceti voltajul", step=1)
            input_volt_norm = (input_volt - stat.loc['volt']['min'])/(stat.loc['volt']['max'] - stat.loc['volt']['min'])
        with c2:
            input_rotate = st.number_input("Introduceti rotatiile",step=1)
            input_rotate_norm = (input_rotate - stat.loc['rotate']['min'])/(stat.loc['rotate']['max'] - stat.loc['rotate']['min'])
        with c3:
            input_pressure = st.number_input("Introduceti presiunea",step=1)
            input_pressure_norm = (input_pressure - stat.loc['pressure']['min'])/(stat.loc['pressure']['max'] - stat.loc['pressure']['min'])
        with c4:
            input_vibration = st.number_input("Introduceti vibratiile",step=1)
            input_vibration_norm = (input_vibration - stat.loc['vibration']['min'])/(stat.loc['vibration']['max'] - stat.loc['vibration']['min'])
    
        predict = st.form_submit_button("Faceti prezicerea")    
        if predict:
            prediction = model.predict([[input_volt_norm,
                        input_rotate_norm,
                        input_pressure_norm,
                        input_vibration_norm]])
            
            st.write(prediction)



