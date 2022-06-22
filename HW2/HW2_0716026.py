# Author: Chu-Hao Hsiao
# Student ID: 0716026
# Homework ID: hw2
# Due Date: 04/20/2022

import csv
import spacy
import pandas

ds = pandas.read_csv('data.csv')
all_sentence = ds['sentence']
all_subject = ds['S']
all_verb = ds['V']
all_object = ds['O']
all_id = ds['id']

nlp = spacy.load('en_core_web_sm')

def del_punct(sub_obj_list):
    inside_punc = False
    del_start = 0
    del_end = 0
    for i in range(len(sub_obj_list)):
        token = sub_obj_list[i]
        if(token.pos_ == "PUNCT" and inside_punc == False):
            inside_punc = True
            del_start = i
        elif(token.pos_ == "PUNCT" and inside_punc == True):
            inside_punc = False
            del_end = i
    if(del_start != 0 or del_end != 0):
        for j in range(del_end,del_start-1,-1):
            del sub_obj_list[j]
    
    return sub_obj_list

def del_after_noun(sub_obj_list):
    del_noun = 0
    for i in range(len(sub_obj_list)):
        token = sub_obj_list[i]
        if(token.pos_ == "NOUN"):
            del_noun = i

    if(del_noun != 0):
        for j in range(len(sub_obj_list)-1,del_noun,-1):
            del sub_obj_list[j]

    return sub_obj_list

SUBJECT = ["nsubj", "nsubjpass", "csubj", "csubjpass", "agent", "expl"]
OBJECT = ["attr", "dobj", "dative", "oprd", "pobj"]

first_write = True

header = ['id', 'label']
with open('submission3(0.755).csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(header)

for i in range(len(all_sentence)):
    sentence = all_sentence[i]
    doc = nlp(sentence)

    ver = []
    sub = []
    obj = []
    for token in doc:
        verb_list = []
        if(token.dep_ == "ROOT"):
            verb_list.append(token)
            ver.append(verb_list)
            for tkn in doc:
                if(tkn.dep_ in SUBJECT and tkn.head in verb_list):
                    sub_list = list(tkn.subtree)
                    sub_list = del_punct(sub_list)
                    sub_list = del_after_noun(sub_list)
                    sub.append(sub_list)
                if(tkn.dep_ in OBJECT and tkn.head in verb_list):
                    obj_list = list(tkn.subtree)
                    obj_list = del_punct(obj_list)
                    obj_list = del_after_noun(obj_list)
                    obj.append(obj_list)
    
    sub_check = False
    verb_check = False
    obj_check = False

    subject = all_subject[i]
    doc_s = nlp(subject)
    for element in sub:
        for token in element:
            contain_or_not = False
            for doc_token in doc_s:
                if(str(token) == str(doc_token)):
                    contain_or_not = True
                    break
            if(contain_or_not == False):
                sub_check = False
                break    
            else:
                sub_check = True
        if(sub_check == True):
            break


    verb = all_verb[i]
    doc_v = nlp(verb)
    for element in ver:
        for token in element:
            contain_or_not = False
            for doc_token in doc_v:
                if(str(token) == str(doc_token)):
                    contain_or_not = True
                    break
            if(contain_or_not == False):
                verb_check = False
                break
            else:
                verb_check = True
        if(verb_check == True):
            break

    object = all_object[i]
    doc_o = nlp(object)
    for element in obj:
        for token in element:
            contain_or_not = False
            for doc_token in doc_o:
                if(str(token) == str(doc_token)):
                    contain_or_not = True
                    break
            if(contain_or_not == False):
                obj_check = False
                break
            else:
                obj_check = True
        if(obj_check == True):
            break

    id = all_id[i]
    label = 0
    if(sub_check and verb_check and obj_check):
        label = 1
    data = [id, label]
    with open('submission3(0.755).csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)