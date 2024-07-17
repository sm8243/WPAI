from flask import Flask, render_template, request, send_file
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form['url']
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')

    Film = []
    Year = []
    Award = []
    Nomination = []
    count = 0
    for i in soup.findAll('td'):
        i = re.sub('^<td>.*">|<td>|</td>|<.*>|\n', "", str(i))
        if count == 0:
            Film.append(i)
            count += 1
        elif count == 1:
            Year.append(i)
            count += 1
        elif count == 2:
            Award.append(i)
            count += 1
        else:
            count = 0
            Nomination.append(i)

    oscar = pd.DataFrame({
        "Film": Film[:1360],
        "Year": Year[:1360],
        "Award": Award[:1360],
        "Nomination": Nomination[:1360]
    })

    oscar.to_excel("films_awards.xlsx", index=False)
    return send_file("films_awards.xlsx", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
