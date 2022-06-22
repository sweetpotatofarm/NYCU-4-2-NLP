#Author: Chu-Hao Hsiao 
#Student ID: 0716026 
#HW ID: Hw3
#Due Date: 05/25/2022

from glob import glob
import json
import kenlm

LM = "wiki_5M.arpa"
model = kenlm.LanguageModel(LM)

def list2string(input_list):
    first = True
    return_str = ""
    for element in input_list:
        if(first == True):
            first = False
            return_str = return_str + element
        else:
            return_str = return_str + ' ' + element
            
    return return_str

N = 3

submission_file = open("submission.csv", 'w')
submission_file.write('id,label\n')
for filename in glob("test/*"):
    file = open(filename, 'r')
    data = json.load(file)

    article = data['article']
    article = article.lower()
    for c in ".,=()[]{}\":;><":
        article = article.replace(c, c+" ")
        article = article.replace(c, " "+c)
    article = article.replace("'", " '")
    article = article.replace("\n", " ")
    article = ' '.join(article.split())
    article_token = article.split(' ')

    source = data['source']
    index = 0
    q = ""
    for i in range(len(article_token)):
        if article_token[i] == '_':
            q = source + '_' + str(index)
            index = index+1
            options = data['options'][q]
            left = article_token[max(0, i-N+1):i]
            right = article_token[i+1:i+N]
            high_score = -100
            ans = 'A'
            for option_num in range(len(options)):
                option = options[option_num]
                token_combination = left + [option] + right
                text = list2string(token_combination)
                score = model.score(text, bos = True, eos = True)
                if(score > high_score):
                    high_score = score
                    ans = 'ABCD'[option_num]
            submission_file.write(q + ',' + ans + '\n')
            