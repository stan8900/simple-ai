import nltk
import numpy as np
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download necessary NLTK data
nltk.download('punkt')  # First-time use only
nltk.download('wordnet')  # First-time use only

# Sample data
data = """Hello, how can I help you today?
Hi, I'm looking for some information on artificial intelligence.
Sure, I can help with that. What specifically would you like to know?
I want to know what artificial intelligence is.
Artificial intelligence (AI) refers to the simulation of human intelligence in machines that are programmed to think and learn like humans.
Thank you! That was helpful.
You're welcome! If you have any other questions, feel free to ask.
"""

# Tokenize sentences
sent_tokens = nltk.sent_tokenize(data)

# Tokenize words
word_tokens = nltk.word_tokenize(data)

# Preprocess data
lemmer = nltk.stem.WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

def response(user_response):
    robo_response = ''
    sent_tokens.append(user_response)
    
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    
    if req_tfidf == 0:
        robo_response = "I am sorry! I don't understand you."
    else:
        robo_response = sent_tokens[idx]
    
    sent_tokens.pop()
    
    return robo_response

flag = True
print("Chatbot: Hello! How can I assist you? Type 'bye' to exit.")

while flag:
    user_response = input("You: ").lower()
    if user_response != 'bye':
        if user_response == 'thanks' or user_response == 'thank you':
            flag = False
            print("Chatbot: You're welcome!")
        else:
            if user_response.strip() != '':
                print("Chatbot: ", response(user_response))
    else:
        flag = False
        print("Chatbot: Goodbye! Take care.")
