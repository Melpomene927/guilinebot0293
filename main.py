from flask import *
from datetime import datetime
#import pandas as pd
#import pandas_datareader as pdr
import json
import numpy as np
import sqlData

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class InputForm(FlaskForm):
    name=StringField('商品名稱',validators=[DataRequired()])
    qty=StringField('販售數量',validators=[DataRequired()])
    stock=StringField('庫存數量',validators=[DataRequired()])
    submit=SubmitField('確認')


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

@app.route('/getPm25Data',methods=["GET","POST"])
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

@app.route('/getDBData',methods=["GET","POST"])
def getDBData():
    data={}
    if request.method =='POST':
        res = sqlData.getDBData()
        data['name']=[x[0] for x in res]
        data['qty']=[x[1] for x in res]
        data['stock']=[x[2] for x in res]
        return (json.dumps(data,ensure_ascii=False))
    if request.method == 'GET':
        res=sqlData.getDBData()
        print(res)
        return f'{res}'

@app.route('/storechart')
def storechart():
    return render_template("storechart.html")

@app.route('/inputForm',methods=["POST","GET"])
def inputForm():
    status=''
    form=InputForm()
    if form.validate_on_submit:
        print(form.name.data, form.qty.data, form.stock.data)

        sqlStr=f'insert into data values("{form.name.data}",{form.qty.data},{form.stock.data})'

        #if not sqlData.CheckDB()

        sqlData.writeDBData(sqlStr)
        status='商品新增成功'
    return render_template('input_form.html',title='商品管理介面',form=form,status=status)



if __name__ == '__main__':
    app.run(debug=True)
