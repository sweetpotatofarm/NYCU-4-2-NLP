#Author: Chu-Hao Hsiao
#Student ID: 0716026
#HW ID: Hw4
#Due Date: 06/17/2022
 
import numpy as np
import pandas as pd
import json
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import ktrain
from ktrain import text

f = open('train.json')
data = json.load(f)
utterance = []
emotion = []
relation = []
for dialogue_id in data:
    pre = ""
    for j in range(0,len(data[dialogue_id])):
        instance_id = dialogue_id + '_' + str(j+1)
        utt = pre + '///' + data[dialogue_id][j][instance_id]["utterance"]
        utterance.append(utt)
        relation.append(data[dialogue_id][j][instance_id]["listener"][0]["relation"])
        emotion.append(data[dialogue_id][j][instance_id]["emotion"])
        pre = data[dialogue_id][j][instance_id]["utterance"]
f.close()

le = LabelEncoder()
emotion = le.fit_transform(emotion)
data = {'utterance':  utterance,
        'emotion': emotion
        }
df = pd.DataFrame(data)

data_train, data_test = train_test_split(df, test_size=0.2)
(X_train, y_train), (X_test, y_test), preproc = text.texts_from_df(train_df = data_train,
                                                                   text_column = 'utterance',
                                                                   label_columns = 'emotion',
                                                                   val_df = data_test,
                                                                   maxlen = 300,
                                                                   lang = 'zh-*',
                                                                   preprocess_mode = 'bert')

model = text.text_classifier(name = 'bert',
                             train_data = (X_train, y_train),
                             preproc = preproc)

learner = ktrain.get_learner(model=model, train_data=(X_train, y_train),
                   val_data = (X_test, y_test),
                   batch_size = 8)

learner.fit_onecycle(lr = 2e-5, epochs = 2)
predictor = ktrain.get_predictor(learner.model, preproc)

f = open('test.json')
data = json.load(f)
utterance_test = []
id = []
for dialogue_id in data:
    pre = ""
    for j in range(0,len(data[dialogue_id])):
        instance_id = dialogue_id + '_' + str(j+1)
        id.append(instance_id)
        utt = pre + '///' + data[dialogue_id][j][instance_id]["utterance"]
        utterance_test.append(utt)
        pre = data[dialogue_id][j][instance_id]["utterance"]
f.close()

y_pred = predictor.predict(utterance_test)

result_num = []
for i in range(len(y_pred)):
  result_num.append(int(y_pred[i][len(y_pred[i])-1]))

result = le.inverse_transform(result_num)
data = {'id':  id,
        'emotion': result
        }
submission = pd.DataFrame(data)
submission.to_csv('submission.csv', index = False)