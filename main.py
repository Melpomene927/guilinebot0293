from flask import *
from datetime import datetime
#import pandas as pd
#import pandas_datareader as pdr
import json
import numpy as np

import sqlData

app = Flask(__name__)
@app.route('/')
@app.route('/index')
@app.route('/index/<string:name>')
def index(name='Mikee'):
    time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('index.html', **locals())

@app.route('/Hello')
def Hello():
    return 'Hello!'

@app.route('/test/<string:name>')
def test(name):
    str=f'Hello world! {name}'
    return str

#呼叫模板網頁
@app.route('/test_html')
def test_html():
    return render_template('test.html')

from stock import GetStock
@app.route('/stock')
def stock():
    time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    stocks=GetStock()
    return render_template('stock.html',**locals())

from pm25 import getPM25
@app.route('/pm25')
def pm25Site():
    time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    theads,pm25=getPM25()
    return render_template('pm25.html',**locals())


@app.route('/pm25chart')
def pm25char():
    return render_template('pm25chart.html',**locals())

@app.route('/chart')
def char():
    return render_template('my_template.html',**locals())

@app.route('/getPm25Data',methods=["POST"])
def getPm25Data():
    if request.method=="POST":
        name=[]
        qty=[]
        stock=[]
        theads,pm25=getPM25()

        for data in pm25:
            if not np.isnan(data[2]):
                name.append(data[0])
                qty.append(data[2])
                stock.append(data[1])
    dict1={'name':name, 'qty':qty, 'stock':stock}

    return (json.dumps(dict1,ensure_ascii=False))

@app.route('/getSqlData',method=["GET","POST"])
def getSqlData():
    data={}
    if request.method =='POST':
        res = sqlData.getDBData()
        print(res)
        data['name']=[x[0] for x in res]
        data['qty']=[x[1] for x in res]
        data['stock']=[x[2] for x in res]
    return (json.dumps(data,ensure_ascii=False))


if __name__ == '__main__':
    app.run(debug=True)
