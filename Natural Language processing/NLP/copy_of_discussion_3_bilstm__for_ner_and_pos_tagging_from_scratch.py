# -*- coding: utf-8 -*-
"""Copy of Discussion 3 BiLSTM _for_NER_and_POS_tagging_from_scratch.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_IwSsft7h6-VbQv3rblCzLzf6U8UmJ7N

**Implimentation of BiLSTM for NER and POS tagging from scratch**

###**Import all the Neccesary Libraries**


We'll perform the following steps:

1.Tokenize the text.

2.Label the tokens for POS tagging.

3.Label the tokens for NER.
"""

# Import The Required Library
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Embedding, Dense, TimeDistributed, Bidirectional

import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('universal_tagset')

# Provided text
text = """
The recently released 2019 national census report putting Nairobi as the most populous county is an indicator of rising job and investment opportunities, Nairobi Governor Mike Sonko has said. Addressing guests during the launch of the International Conference on Population (ICPD25), Sonko said the new resident population will shape development planning for the county. “This reality poses endless social and economic opportunities for all Kenyans and our friends from all over the world,” Sonko said. The Kenya Population and Housing Census 2019 results indicate that Nairobi has a resident population of 4.4 million people. “Over and above this figure, Nairobi has a day population in excess of six million people,” he added. Nairobi still generates over 60% of the country’s Gross Domestic Product and was recently ranked as the sixth wealthiest city in Africa. However, the governor admitted that there are still challenges in terms of infrastructure and social development. “Our investment in these sectors has not grown in tandem with the population over the years and we must improve on this,” he said. The theme of this year’s conference is “Accelerating The Promise” and the Governor has asked participants to focus on offering practical solutions that can be infused in the development planning of the city. National Treasury and Planning CS Ukur Yatani said the national government will continue working closely with the county in financing urban development.
"""

# Step 1: Tokenize the text
from nltk.tokenize import word_tokenize
tokens = word_tokenize(text)
tokens

# Step 2: Label the tokens for POS tagging
# We will use NLTK's pos_tag function for this task
pos_tags = nltk.pos_tag(tokens)
pos_tags

# Step 3: Label the tokens for NER
# Manually labeling some entities in the text
ner_labels = [
    ('Nairobi', 'GPE'), ('2019', 'DATE'), ('Mike Sonko', 'PERSON'), ('Nairobi', 'GPE'), ('ICPD25', 'ORGANIZATION'),
    ('Kenya', 'GPE'), ('2019', 'DATE'), ('Nairobi', 'GPE'), ('Nairobi', 'GPE'), ('Nairobi', 'GPE'), ('Africa', 'LOCATION'),
    ('Nairobi', 'GPE'), ('CS Ukur Yatani', 'PERSON')
]

# Step 4: Prepare the data for training
#Creating sequences of tokens and their corresponding POS and NER labels
pos_data = [(token, pos) for token, pos in pos_tags]
ner_data = [(token, label) for token, label in ner_labels]

pos_data

ner_data

# Define the vocabulary based on unique words in the text
vocab = set(tokens)

# Define word-to-index dictionary
word2idx = {word: idx + 1 for idx, word in enumerate(vocab)}

# Define the inverse mapping from index to word
idx2word = {idx: word for word, idx in word2idx.items()}
word2idx["ENDPAD"] = 0  # Add padding token

# Step 4: Prepare the data for training
# Convert words to indices using word2idx dictionary
pos_X = []
for token, _ in pos_data:
    if token in word2idx:
        pos_X.append(word2idx[token])
    else:
        pos_X.append(word2idx["ENDPAD"])  # Use padding token for out-of-vocabulary words

ner_X = []
for token, _ in ner_data:
    if token in word2idx:
        ner_X.append(word2idx[token])
    else:
        ner_X.append(word2idx["ENDPAD"])  # Use padding token for out-of-vocabulary words

ner_labels

# Convert POS and NER labels to indices
pos_y = [nltk.tag.map_tag('en-ptb', 'universal', pos) for (_, pos) in pos_tags]
pos_y

# Update NER Labels Dictionary
ner_labels = {'GPE': 11, 'DATE': 6, 'PERSON': 12, 'ORGANIZATION': 4, 'LOCATION': 10}

# Update NER Labels Mapping
ner_y = [ner_labels[label] if label in ner_labels else -1 for _, label in ner_data]

# Print updated ner_y
print(ner_y)

# Split the data into training and testing sets
from sklearn.model_selection import train_test_split
pos_X_train, pos_X_test, pos_y_train, pos_y_test = train_test_split(pos_X, pos_y, test_size=0.2, random_state=42)

ner_X_train,ner_X_test, ner_y_train, ner_y_test = train_test_split(ner_X, ner_y, test_size=0.2, random_state=42)