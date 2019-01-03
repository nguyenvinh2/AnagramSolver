"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from AnagramSolver import app
from flask import Flask, request
import json
import requests

class Word():
  def __init__(self, word, definition):
    self.word = word
    self.definition = definition

#gets all possible permutations
def find_anagram(word):
  if len(word) <= 1:
    return word
  else:
    word_array = []
    for anagram in find_anagram(word[1:]):
      for i in range(len(word)):
        word_array.append(anagram[:i] + word[0:1] + anagram[i:])
    return word_array

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template('index.html',
        title='Home Page',
        year=datetime.now().year,)

@app.route('/anagram', methods=['POST'])
def anagram():
  word = request.form['getWord']
  print(word)
  stringURL = 'http://www.anagramica.com/best/' + word
  getJSON = requests.get(stringURL)
  anagram = json.loads(getJSON.text)
  wordList = []

  for eachword in anagram['best']:
    wordList.append(Word(eachword, dictionary(eachword)))
  return render_template('index.html',
    title = 'Home Page',
    word = word,
    year = datetime.now().year,
    anagrams = wordList)

def dictionary(word):
  app_id = 'Your Oxford API ID'
  app_key = 'You Oxford API KEY'
  language = 'en'
  url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word.lower()

  print(word)
  response = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
  print(response.text)
  print("Code {}\n".format(response.status_code))
  getJSON = json.loads(response.text)
  definition = getJSON['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
  return definition
