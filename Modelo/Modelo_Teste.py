import pandas as pd
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from lightgbm import LGBMClassifier
import joblib
from pandera import Column, DataFrameSchema, Check, Int, Float, Index
import mysql.connector

def Load_data():
    # Defina os detalhes da conexão
    config = {
        "user": "user",
        "password": "Password",
        "host": "host", # Colocar IP em caso de ser remoto
        "database": "database_name"
    }

    # Crie uma conexão MySQL usando a biblioteca mysql-connector-python
    conn = mysql.connector.connect(**config)

    # Crie um objeto de cursor
    cursor = conn.cursor()

    # Defina sua consulta SQL
    query = "SELECT * FROM dados_tratados WHERE Data <= '2023-10-30'"

    # Leia os resultados da consulta em um DataFrame do Pandas
    data = pd.read_sql(query, conn)

    # Feche o cursor e a conexão
    cursor.close()
    conn.close()

    return data

data = Load_data()

features =['Temperatura_do_Ar','Temperatura_do_Motor','RPM_Motor','Vibracao_do_Motor','Torque']
target = 'Target'

X = data[features]
y = data[target]

model = make_pipeline(SimpleImputer(), LGBMClassifier(objective= 'multiclass', num_class=len(np.unique(y)) ,boosting_type = 'gbdt', class_weight = 'balanced', max_depth = 30, n_estimators = 160, num_leaves = 43, random_state = 37))

model.fit(X,y)

joblib.dump(model,"model.joblib")

schema = DataFrameSchema({
    "Temperatura_do_Ar":Column(Float,Check(lambda x: x>=0),nullable= True),
    "Temperatura_do_Motor": Column(Float, Check(lambda x: x>=0),nullable= True),
    "RPM_Motor": Column(Float, Check(lambda x: x>=0), nullable= True),
    "Vibracao_do_Motor": Column(Float, Check(lambda x: x>=0), nullable= True),
    "Torque": Column(Float, Check(lambda x: x>=0), nullable= True),
},
index = Index(Int),
ordered= True,
strict= "filter"
)

schema.validate(X)

Validator = schema.to_script()

with open("Validator.py","w") as f:
    f.write(Validator)