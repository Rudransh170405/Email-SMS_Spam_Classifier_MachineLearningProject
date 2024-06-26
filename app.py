
import streamlit as st
import pickle
import string

from nltk.corpus import stopwords
import nltk
nltk.download('punkt')
from nltk.stem import PorterStemmer


ps = PorterStemmer()

def transform_text(text):
    text=text.lower()
    text=nltk.word_tokenize(text)
    y=[]
    for i in text:
        if i.isalnum():
          y.append(i)
    text=y[:] #copying of list is done by cloning it is a mutuable datatype
    y.clear()
    for i in text:
      if i not in stopwords.words('english') and i not in string.punctuation:
          y.append(i)

    text=y[:]
    y.clear()
    for i in text:
      y.append(ps.stem(i))

    return " ".join(y)  #returning as a string

tfidf=pickle.load(open('vectorizer.pkl','rb'))
model=pickle.load(open('model.pkl','rb'))

st.title('Email Spam Classifier')
input_email=st.text_input("Enter your email")
if st.button('Predict'):

    # 1.preprocess
    transformed_email=transform_text(input_email)
    # 2.vectorize
    vector_input=tfidf.transform([transformed_email])
    # 3. predict
    result=model.predict(vector_input)[0]
    # 4. display
    if result==1:
        st.header("Email Spam")
    else:
        st.header("Email Not Spam")