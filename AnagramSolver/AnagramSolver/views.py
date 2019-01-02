"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from AnagramSolver import app
from flask import Flask, request
import json
import requests

	#09e0e9b5
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
  stringURL = 'http://www.anagramica.com/best/' + word
  getJSON = requests.get(stringURL)
  anagram = json.loads(getJSON.text)
  return render_template('index.html',
    title = 'Home Page',
    year = datetime.now().year,
    anagrams = anagram['best'])