# Analysis of artificial intelligence in predictive maintenance present in automation systems within the industrial environmen

# English Version 🇺🇸:

This project consisted of a study to identify the best possible Machine Learning model to make predictions of errors that occurred in a machinery, for this more than 6 models were used for testing, verifying their quality and accuracy, several optimization techniques were used, so that the model took into account several factors.

For data collection, temperature, vibration, and rotation sensors were used, and the data underwent preprocessing before being stored in a database for testing. Several libraries were employed to ensure the model didn't overfit and adapted well to the data. During testing, additional datasets were used to distinguish the best model, which were similar to the machinery datasets and helped distinguish with better precision, aiding in selecting the appropriate model for production.

**How to Use:**

Inside the 'model' folder, there are 3 files: Model_Test, Deploy, and Validator.

When running the Model_Test file, the validator file is created along with a model.joblib file. These files are necessary for the Deploy file to run the model.

The Deploy file encompasses the functionality of the entire model with data in the database. It makes data calls, checks for any null rows (rows containing only zeros), reallocates data if necessary, and after prediction, checks if model retraining is needed. If so, the model is retrained. The model runs every 2 minutes in the file to make predictions.


# Portuguese Version <span>&#x1f1e7;&#x1f1f7;</span>:

Esse projeto consistiu em um estudo para identificar qual o melhor modelo possível de Machine Learning para realizar predições de erros que ocorriam em um maquinário, para isso foram utilizados mais de 6 modelos para teste, verificando sua qualidade e precisão, foram utilizadas várias técnicas de otimização, para que o modelo levasse em consideração vários fatores.

Para a coleta de dados foram utilizados sensores de temperatura, vibração e rotação, os dados foram tratados e realocados em um banco de dados para realizar os testes, foram utilizadas algumas bibliotecas para garantir que  o modelo não realizasse overfitting e acabasse se adaptando aos dados, durante os teste também utilizamos outros datasets para destinguir o melhor modelo, os datasets eram de maquinários semehlantes e assim ajudaram a destinguir com melhor precisão, e na escolha adequada para qual modelo levar a produção.

**Como Usar:**

Dentro da Pasta modelo, podemos verificar 3 arquivos, sendo eles Modelo_Teste, Deploy e Validator.

Ao rodar o arquivo Modelo_Teste, o arquivo validator é criado e um arquivo model.joblib.Esses arquivos serão necessário para que o arquivo Deploy consiga rodar o modelo.

Para o arquivo Deploy temos o funcionamento de todo modelo com os dados no banco de dados, ele realiza a chamada dos dados, verifica se por algum motivo foi criada uma linha nula (linha que só contenha zeros), realoca os dados caso necessários e após a predição, verifica se há necessidade de retreinar o modelo, caso haja, o modelo é retreinado, no arquivo o modelo roda a cada 2 minutos para realizar as previsões.
