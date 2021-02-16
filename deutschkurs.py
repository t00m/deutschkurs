#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Module with the application logic.

# Author: Tomás Vírseda <tomasvirseda@gmail.com>
# License: GPLv3
"""

# Standard libraries
import os
import json
import pprint

# Natural Language Toolkit
# https://www.nltk.org/
import nltk
try:
    nltk.data.find('tokenizers/punkt')
    print("Tokenizer Punkt found!")
except LookupError as error:
    print("Tokenizer Punkt not found!")
    nltk.download('punkt')

# DEMorphy is a morphological analyzer for German language.
# https://github.com/DuyguA/DEMorphy
from demorphy import Analyzer
analyzer = Analyzer(char_subs_allowed=True)

# spaCy is a free, open-source library for advanced Natural Language Processing (NLP) in Python.
# https://spacy.io/
"""
    Text: The original word text.
    Lemma: The base form of the word.
    POS: The simple UPOS part-of-speech tag.
    Tag: The detailed part-of-speech tag.
    Dep: Syntactic dependency, i.e. the relation between tokens.
    Shape: The word shape – capitalization, punctuation, digits.
    is alpha: Is the token an alpha character?
    is stop: Is the token part of a stop list, i.e. the most common words of the language?
"""
import spacy
try:
    print("Loading German corpus")
    # ~ nlp = spacy.load("de_core_news_lg")
    nlp = spacy.load("de_dep_news_trf")
except:
    print("German corpus not found. Download it manually:")
    print("python3 -m spacy download de_dep_news_trf")
    # python3 -m spacy download de_core_news_sm
    exit(-1)


pp = pprint.PrettyPrinter(indent=4)

# Check directories existence
if not os.path.exists('cache'):
    os.makedirs('cache')

if not os.path.exists('docs'):
    os.makedirs('docs')


# Global cache for words
cache_path = os.path.join('cache', 'cache.json')
try:
    with open(cache_path, 'r') as fc:
        cache = json.load(fc)
        print("Words cache loaded")
except:
    cache = {}
    print("Words cache created")

def analyze(topic, text):
    global cache
    doc = nlp(text)

    sentences = nltk.sent_tokenize(text)
    tobj = {}

    for doc in sentences:
        if not doc in tobj:
            tobj[doc] = {}
            tobj[doc]['topic'] = topic
            tobj[doc]['sentences'] = set()
            sentence = nlp(doc)
            print("--> %s" % sentence)
            for word in sentence:
                if not word.pos_ in ['PUNCT', 'SPACE']: # avoid punctuactions
                    key = word.text.lower()
                    if not key in cache: # check if word is not in global cache
                        if not key in tobj[doc]: # check if word doesn't repeat in the same sentence
                            tobj[doc][key] = {}
                            if word.pos_ == 'NN':
                                tobj[doc][key]['word'] = word.text.title()
                            else:
                                tobj[doc][key]['word'] = word.text.lower()
                            tobj[doc][key]['pos'] = "%s" % spacy.explain(word.pos_) # Part-of-Speech (POS) Tagging
                            tobj[doc][key]['lema'] = word.lemma_ # Root word
                            tobj[doc][key]['prefix'] = word.prefix_ # Prefix
                            tobj[doc][key]['suffix'] = word.suffix_ # Sufix
                            cache[key] = tobj[doc][key]
                            print("\tWord '%s' added to global cache" % key)
                    else:
                        tobj[doc][key] = cache[key]
                        print("\tWord '%s' got from cache" % key)

    return tobj


for topic in os.listdir('userdata'):
    topicpath = os.path.join('userdata', topic)
    for filename in os.listdir(topicpath):
        filepath = os.path.join(topicpath, filename)
        print("Analyzing %s -> %s" % (topic, filename))
        text = open(filepath, 'r').read()
        tobj = analyze(topic, text)
        # ~ pp.pprint(tobj)
    pp.pprint(cache)
    print(list(cache))

with open(cache_path, 'w') as fc:
    json.dump(cache, fc)
    print("Words cache saved")

# Generate docs
TITLE = "= %s\n\n"
PROP = ":%s:\t\t%s\n"
EOHMARK = "// END-OF-HEADER. DO NOT MODIFY OR DELETE THIS LINE\n\n"
BODY = "_%s_ is a _%s_. Its lema is _%s_."

# FIXME: Write Nouns in capital
# FIXME: Check suffixes
for key in cache:
    doc_path = os.path.join('docs', "%s.adoc" % key)
    with open(doc_path, 'w') as fdp:
        s = analyzer.analyze(key)
        print(key)
        print('='*len(key))
        pp.pprint(s)
        print()
        print()
        fdp.write(TITLE % cache[key]['word'])
        fdp.write(PROP % ("Part Of Speech", cache[key]['pos']))
        fdp.write(PROP % ("Lema", cache[key]['lema']))
        fdp.write(PROP % ("Prefix", cache[key]['prefix']))
        fdp.write(PROP % ("Suffix", cache[key]['suffix']))
        fdp.write(EOHMARK)
        fdp.write(BODY % (cache[key]['word'], cache[key]['pos'], cache[key]['lema']))
