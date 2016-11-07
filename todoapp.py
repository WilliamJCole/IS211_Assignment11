#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This is my docstring."""

from flask import Flask, request, redirect, render_template, session
import pickle
import os
import sys
import re

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index(debug=True):
    try:
        infile = open('db.txt', 'rb')
        mylist = []
        while 1:
            try:
                mylist.append(pickle.load(infile))
            except:
                break
        #print ("Loading the list from file: ", mylist)
        infile.close()
        return render_template('index.html', posts=mylist)
    
    except(ValueError, IOError):
        return render_template('index.html')


@app.route('/submit', methods = ['POST'])
def submit(debug=True):
    email = request.form['email']
    priority = request.form['priority']
    task = request.form['task']
    
    if not re.search('(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', email):
        error_field = 'Email'
        return render_template('error.html', methods = ['POST'], error_field = error_field)
    elif not re.search('(Low|Medium|High)', priority):
        error_field = 'Priority'
        return render_template('error.html', methods = ['POST'], error_field = error_field)
    mydict = {'task': task, 'email': email, 'priority': priority}

    print ("From within submit: ", mydict)
    
    outfile = open('db.txt', 'ab')
    pickle.dump(mydict, outfile)
    outfile.close()
    
    return redirect('/')


@app.route('/clearall', methods = ['POST'])
def delete_record(debug=True):
    try:
        os.remove('db.txt')
    except(OSError):
        pass
    
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
