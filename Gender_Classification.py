#!/usr/bin/env python
# coding: utf-8

# # Classificação Homem e Mulher

# ## Importando Bibliotecas

# In[1]:


import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


# ## Importando DataSet

# In[2]:


dados = pd.read_csv('C://Users/User/Downloads/gender_classification_v7.csv')
dados.head()


# ## Visualizando quantos dos dados são nulos

# In[3]:


print(f'Temos {dados.isna().sum().sum()} dados nulos')


# ## Tratando os Dados e colunas

# In[4]:


a_renomear = {'long_hair' : 'cabelo_longo', 'forehead_width_cm' : 'largura_da_testa_cm',
              'forehead_height_cm' : 'altura_da_testa_cm', 'nose_wide' : 'nariz_largo',
             'nose_long' : 'nariz_longo', 'lips_thin' : 'labios_finos', 'distance_nose_to_lip_long' : 'distancia_naris_labio',
              'gender' : 'genero'}

a_trocar_genero = {'Male' : 1, 'Female' : 0}

dados = dados.rename(columns=a_renomear)
dados.genero = dados.genero.map(a_trocar_genero)
dados.head()


# In[5]:


x = dados[['cabelo_longo', 'nariz_largo', 'labios_finos', 'distancia_naris_labio']]
y = dados['genero']


SEED = 5
np.random.seed(SEED)
treino_x, teste_x, treino_y, teste_y = train_test_split(x, y,
                                                        stratify = y, test_size = 0.25)
print(f'Treinamento com {len(treino_x)} e teste com {len(teste_x)} elementos')

model = LinearSVC()
model.fit(treino_x, treino_y)
previsoes = model.predict(teste_x)

acuracia = accuracy_score(teste_y, previsoes) * 100
print(f'A acuracia foi {acuracia:.2f} %')


# In[6]:


SEED = 5
np.random.seed(SEED)
raw_treino_x, raw_teste_x, treino_y, teste_y = train_test_split(x, y,
                                                        stratify = y, test_size = 0.25)
print(f'Treinamento com {len(treino_x)} e teste com {len(teste_x)} elementos')

model = DecisionTreeClassifier(max_depth=4)
model.fit(raw_treino_x, treino_y)
previsoes = model.predict(raw_teste_x)

acuracia = accuracy_score(teste_y, previsoes) * 100
print(f'A acuracia foi {acuracia:.2f} %')


# In[7]:


from sklearn.tree import export_graphviz
import graphviz

features = x.columns
dot_data = export_graphviz(model, out_file=None,
                          filled = True, rounded = True,
                           feature_names=features,
                          class_names = ['mulher', 'homem'])
grafico = graphviz.Source(dot_data)
grafico


# In[ ]:




