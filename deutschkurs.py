#!/usr/bin/python
# -*- coding: utf-8 -*-

# File: deutschkurs.py
# Author: Tomás Vírseda <tomasvirseda@gmail.com>
# License: GPL v3
# Description: Module with the application logic.


# Standard libraries
import os
import json
import subprocess

import nltk # Natural Language Toolkit (https://www.nltk.org)
from demorphy import Analyzer # DEMorphy is a morphological analyzer for German language (https://github.com/DuyguA/DEMorphy)
import spacy # spaCy is library for advanced Natural Language Processing in Python (https://spacy.io)

from log import get_logger # custom logging module
from mydict import PersonalDictionary

DEBUG_LEVEL = "DEBUG"

msg = get_logger("Deutschkurs", DEBUG_LEVEL)
msg.info("Starting Deutschkurs")

try:
    nltk.data.find('tokenizers/punkt')
    msg.debug("Tokenizer Punkt found!")
except LookupError as error:
    msg.warning("Tokenizer Punkt not found!")
    msg.info("Downloading Tokenizer Punkt for NLTK")
    nltk.download('punkt')

analyzer = Analyzer(char_subs_allowed=True)
msg.debug("DEMorphy initialited")

try:
    msg.debug("Loading German corpus")
    # ~ nlp = spacy.load("de_core_news_lg")
    nlp = spacy.load("de_dep_news_trf")
except:
    msg.error("German corpus not found. Download it manually:")
    msg.info("python3 -m spacy download de_dep_news_trf")
    # python3 -m spacy download de_core_news_sm
    exit(-1)


# Check directories existence

## Words Cache
if not os.path.exists('cache'):
    os.makedirs('cache')
    msg.debug("Directory 'cache' created")

## KB4IT docs
if not os.path.exists('docs'):
    os.makedirs('docs')

## Dictionary definitions
if not os.path.exists('dict'):
    os.makedirs('dict')

## User data
if not os.path.exists('userdata'):
    os.makedirs('userdata')
    # Write README
    with open('userdata/README', 'w') as fout:
        fout.write("Each directory is a topic. Give them a meaninful name\n")
    # Write example
    os.makedirs('userdata/grundschule')
    with open('userdata/grundschule/info-20200901.txt', 'w') as fout:
        sentences = """Liebe Eltern.\n
                    Im Anhang finden Sie die Infos zum Infektionsschutzgesetz.\n
                    Vielen Dank und noch einen schönen Tag!\n
                    Grüße"""
        fout.write(sentences)


# Global cache for words
cache_path = os.path.join('cache', 'cache.json')
try:
    with open(cache_path, 'r') as fc:
        cache = json.load(fc)
        msg.debug("Words cache loaded")
except:
    cache = {}
    msg.debug("Words cache created")


pd = PersonalDictionary(DEBUG_LEVEL)

def get_dict_definition(word):
    pass



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
            msg.info("Sentence[%s]" % sentence)
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
                            msg.debug("[ + ] Word '%s' added to global cache" % key)
                    else:
                        tobj[doc][key] = cache[key]
                        msg.debug("[ = ] Word '%s' got from cache" % key)
                    pd.lookup(key)

    return tobj


for topic in os.listdir('userdata'):
    topicpath = os.path.join('userdata', topic)
    try:
        for filename in os.listdir(topicpath):
            filepath = os.path.join(topicpath, filename)
            msg.info("Topic[%s] - File[%s]", topic, filename)
            text = open(filepath, 'r').read()
            tobj = analyze(topic, text)
    except NotADirectoryError:
        continue


with open(cache_path, 'w') as fc:
    json.dump(cache, fc)
    msg.debug("Words cache saved")

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
        # ~ print(key)
        # ~ print('='*len(key))
        # ~ pp.pprint(s)
        # ~ print()
        # ~ print()
        fdp.write(TITLE % cache[key]['word'])
        fdp.write(PROP % ("Part Of Speech", cache[key]['pos']))
        fdp.write(PROP % ("Lema", cache[key]['lema']))
        fdp.write(PROP % ("Prefix", cache[key]['prefix']))
        fdp.write(PROP % ("Suffix", cache[key]['suffix']))
        fdp.write(EOHMARK)
        fdp.write(BODY % (cache[key]['word'], cache[key]['pos'], cache[key]['lema']))

pd.missing()
msg.info("Ending Deutschkurs")