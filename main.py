#!/bin/bash
# -*- UTF-8 -*-
from flask import Flask
from flask import render_template
from flask import request
from flask import Response

app = Flask(__name__)

class Line(object):
    def __init__(self, idLine, field1, field2, field3):
        self.idLine = idLine
        self.field1 = field1
        self.field2 = field2
        self.field3 = field3

def readFile(filename):
    f = open(filename, 'r')
    result = {}
    for l in f:
        parts = l.replace("\n", "").split('|')
        idLine = parts[0]
        line = Line(idLine, parts[1], parts[2], parts[3])
        result[idLine] = line
    f.close()
    return result

def writeFile(filename, content):
    f = open(filename, 'w')
    for key,line in content.iteritems():
        f.write(key+"|"+line.field1+"|"+line.field2+"|"+line.field3+"\n")
    f.close()

@app.route("/post", methods=['POST'])
def post():
    print("Modifying the element "+request.form['pk']+" for field "+request.form['name']+" with new value "+request.form['value'])
    idLine = request.form['pk']
    fileContent = readFile('list.csv')
    response = Response()
    if idLine in fileContent.keys():
        name = request.form['name']
        value = request.form['value']
        response.status_code = 200
        if name.startswith('field1'):
            fileContent[idLine].field1 = value
        elif name.startswith('field2'):
            fileContent[idLine].field2 = value
        elif name.startswith('field3'):
            fileContent[idLine].field3 = value
        else:
            response.status_code = 409
            response.data = "Unknown field"
        if response.status_code == 200:
            writeFile('list.csv', fileContent)
    else:
        response.status = 409
        response.data = "Row unknown"
    return response


@app.route("/")
def hello():
    result = readFile('list.csv')
    return render_template("index.html", result = result)

if __name__ == "__main__":
    app.debug = True
    app.run()
