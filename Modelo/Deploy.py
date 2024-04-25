import pandas as pd
from sklearn.metrics import accuracy_score,f1_score, recall_score
from imblearn.metrics import geometric_mean_score
import mysql.connector
import math
from sqlalchemy import create_engine
from Validator import schema
import joblib
from datetime import datetime, timedelta
import schedule
import time


def config():
    # Defina os detalhes da conexão
    config = {
        "user": "user",
        "password": "password",
        "host": "host", # Colocar IP em caso de ser remoto
        "database": "database_name"
    }
    return config

def Load_data(name):
    # Defina os detalhes da conexão
    config()

    #Configuracao Logica de fuso horario
    minuto = datetime.now() - timedelta(seconds= 120)
    horas = minuto.strftime('%Y-%m-%d %H:%M:%S')

    # Crie uma conexão MySQL usando a biblioteca mysql-connector-python
    conn = mysql.connector.connect(**config)

    # Crie um objeto de cursor
    cursor = conn.cursor()

    # Defina sua consulta SQL
    query = f"SELECT * FROM {name} WHERE Data >= '{horas}'"

    # Leia os resultados da consulta em um DataFrame do Pandas
    data = pd.read_sql(query, conn)

    # Feche o cursor e a conexão
    cursor.close()
    conn.close()

    return data

def Retrain_Load_data(name):
    # Defina os detalhes da conexão
    config()

    # Crie uma conexão MySQL usando a biblioteca mysql-connector-python
    conn = mysql.connector.connect(**config)

    # Crie um objeto de cursor
    cursor = conn.cursor()

    # Defina sua consulta SQL
    query = f"SELECT * FROM {name}" 

    # Leia os resultados da consulta em um DataFrame do Pandas
    data = pd.read_sql(query, conn)

    # Feche o cursor e a conexão
    cursor.close()
    conn.close()

    return data


def Insert_data(data, table_name):
    # Defina os detalhes da conexão
    config()

    # Use o SQLAlchemy para criar um mecanismo de conexão
    engine = create_engine(f"mysql+mysqlconnector://{config['user']}:{config['password']}@{config['host']}/{config['database']}")

    # Insira os dados tratados no MySQL
    data.to_sql(name= table_name, con= engine, if_exists='append', index=False)


def Features(data):

    # Remover linhas com valores zerados
    data = data[data['RPM_Motor'] != 0]
    data = data[data['Vibracao_do_Motor'] != 0]
    data = data[data['Temperatura_do_Ar'] != 0]
    data = data[data['Temperatura_do_Motor'] != 0]

    # Calculo do torque
    omega = (2 * math.pi * data['RPM_Motor']) / 60
    data['Torque'] = 44 / omega

    # Adicione a coluna 'Target' com base na condição
    data['Target'] = data['Torque'].apply(lambda x: 2 if x > 0.67 else (1 if x <= 0.61 else 0))
    
    data['Tipo_de_Falha'] = data['Target'].apply(lambda x: 'Torque Alto' if x == 2 else ('Torque Baixo' if x == 1 else 'Funcionamento Normal'))   

    print(data)
    
    return data

def Config_data():
    data_bruta = Load_data("dados_brutos")
    tratados = Features(data_bruta)
    Insert_data(tratados, "dados_tratados")
    data_tratada = Load_data("dados_tratados")

    return data_tratada

def Retrain(model):
    print('Retreinando Modelo')
    data_train = Retrain_Load_data("dados_tratados")

    features =['Temperatura_do_Ar','Temperatura_do_Motor','RPM_Motor','Vibracao_do_Motor','Torque']
    target = 'Target'

    X = data_train[features]
    y = data_train[target]

    model.fit(X,y)

    joblib.dump(model,"model.joblib")


def Score_Verification(pred,rd,md):
    
    ac = accuracy_score(rd,pred)
    f1 = f1_score(rd,pred, average = 'macro')
    gm = geometric_mean_score(rd,pred)
    recall = recall_score(rd,pred, average = 'macro')

    print('--Métricas Atuais--')
    print('Acurácia:', ac)
    print('F1-Score: ', f1)
    print('Recall: ', recall)
    print('G-mean: ', gm)

    if (ac < 0.98 and f1 < 0.98) or gm < 0.96:
        Retrain(md)


def Make_pred():
    DataHora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = Config_data()
    print(data)
    
    validated = schema.validate(data)

    model = joblib.load('model.joblib')
    predictions = model.predict(validated)
    predictions_data = pd.DataFrame({'ID': data['ID'], 'Data': DataHora, 'Previsao': predictions,'DadosReais': data['Target']})
    Insert_data(predictions_data,"previsao")

    Score_Verification(predictions_data['Previsao'],data['Target'],model)
    
if __name__ == '__main__':

    schedule.every(2).minutes.do(Make_pred)
    print('Status: Rodando' + '\nHora:', datetime.now().strftime('%H:%M:%S'))
    while True:
        schedule.run_pending()
        time.sleep(2)   