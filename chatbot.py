import keyboard
import streamlit as st
import numpy as np
import sklearn
import string
import nltk                     #library for natural language procesing
import random

user_response=""
st.title("ASK 'EDA' ANYTHING REGARDING PCOD AND PCOS: ")
path="C:/mahua/Projects/miniproject/chatbot.txt"
f=open(path,'r',errors='ignore')
raw_doc=f.read()
raw_doc=raw_doc.lower()         #converts text to lower case for preprocessing
nltk.download('punkt')          #punkt is tokenizer 
nltk.download('wordnet')        #wordnet is english dictionary in nltk
sent_tokens=nltk.sent_tokenize(raw_doc)     #converts doc to list of sentence
word_tokens=nltk.word_tokenize(raw_doc)     #converts doc to list of words

#text preprocessing
lemmer = nltk.stem.WordNetLemmatizer()
def Lemtokens(tokens):
    return[lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct),None) for punct in string.punctuation)
def LemNormalize(text):
    return Lemtokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

#Greeting inputs
greet_ip=('hello','hi','hey',)
greet_op=[' hello :)',' hi',' hey!',' I am glad to meet you!']
def greet(sentence):
    for word in sentence.split():
        if word.lower() in greet_ip:
            return random.choice(greet_op)

from sklearn.feature_extraction.text import TfidfVectorizer     #term freq and inverse doc freq => occurence of one words
from sklearn.metrics.pairwise import cosine_similarity          #gives an normalised op

def response(user_response):
    robo1_response=''
    Tfidfvec=TfidfVectorizer(tokenizer=LemNormalize,stop_words='english')
    tfidf=Tfidfvec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1],tfidf)
    idx=vals.argsort()[0][-2]                                   #verify from first to second last word
    flat = vals.flatten()
    flat.sort()
    req_tfidf=flat[-2]
    
    if(user_response == ""):
        robo1_response=robo1_response+"Waiting for input ...."
        return robo1_response
    elif(req_tfidf==0):
        robo1_response=robo1_response+"Sorry! I can't Understand"
        return robo1_response
    else:
        robo1_response=robo1_response+sent_tokens[idx]
        return robo1_response

flag=True
user="User"
user_response=st.text_input("Hi please enter your name: ")
user=user_response
i=0
while (flag==True):
    key1=i
    for i in range(15):
        key1=i+1
        if user_response!='':
            user_response=st.text_input("\n"+user+":",key=key1)
            user_response=user_response.lower()
            if(user_response.startswith('bye')!=True):
                if(user_response.startswith("thanks") or user_response.startswith("thank")):
                    flag=False
                    st.write("Edah: You're Welcome !")
                    flag=True
                    user_response=user_response.lower()
                elif(user_response=="how are you?" or user_response=="how are you"):
                    flag=False
                    st.write("Eda: All good!")
                    flag=True
                    user_response=user_response.lower()
                elif(user_response=="can you help me?" or user_response=="i need your help"):
                    flag=False
                    st.write("Eda: I would be pleased to help you")
                    flag=True
                    user_response=user_response.lower()
                elif(user_response.startswith("good")==True):
                    flag=False
                    st.write(user_response)
                    flag=True
                    user_response=user_response.lower()
                elif "i love" in user_response:
                    flag=False
                    st.write("Eda: That's great!")
                    flag=True
                elif "i like" in user_response:
                    flag=False
                    st.write("Eda: That's great!")
                    flag=True
                else:
                    if(greet(user_response)!=None):
                        flag=False
                        st.write(" "+greet(user_response))
                        flag=True
                        user_response=user_response.lower()
                    else:
                        flag=False
                        sent_tokens.append(user_response)
                        word_tokens=word_tokens+nltk.word_tokenize(user_response)
                        final_words=list(set(word_tokens))
                        st.write("Edah: ")
                        st.write(response(user_response))
                        flag=True
                        sent_tokens.remove(user_response)
                        user_response=user_response.lower()
            else:
                st.write("Edah: Bye! Take Care")
                flag=False
                break
    