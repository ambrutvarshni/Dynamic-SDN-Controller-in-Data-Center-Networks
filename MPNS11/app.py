from flask import Flask, render_template, request, session
from cryptography.fernet import Fernet

app = Flask(__name__)

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="mpns11_2023"
)

app.secret_key = 'your secret key'

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/alogin', methods = ['POST', 'GET'])
def alogin():
    if request.method == 'POST':
        uid = request.form['uid']
        pwd = request.form['pwd']
        if uid == 'admin' and pwd == 'admin':
            return render_template('ahome.html')
        else:
            return render_template('admin.html')

@app.route('/auser')
def auser():
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM user')
    account = cursor.fetchall()
    cursor.close()
    return render_template('auser.html', result = account)

@app.route('/anet')
def anet():
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM net')
    account = cursor.fetchall()
    cursor.close()
    return render_template('anet.html', result = account)

@app.route('/afile')
def afile():
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM upload')
    account = cursor.fetchall()
    cursor.close()
    return render_template('afile.html', result = account)

@app.route('/anuser')
def anuser():
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM nusers')
    account = cursor.fetchall()
    cursor.close()
    return render_template('anuser.html', result = account)

@app.route('/net')
def net():
    return render_template('net.html')

@app.route('/nlogin', methods = ['POST', 'GET'])
def nlogin():
    if request.method == 'POST':
        uid = request.form['uid']
        pwd = request.form['pwd']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM net WHERE email = %s AND password = %s', (uid, pwd))
        account = cursor.fetchone()
        cursor.close()
        if account:
            session['nid'] = request.form['uid']
            session['nname'] = account[0]
            return render_template('nhome.html', result = account[0])
        else:
            return render_template('net.html')

@app.route('/nhome')
def nhome():
    return render_template('uhome.html', result = session['nname'])

@app.route('/nuser')
def nuser():
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM user')
    account = cursor.fetchall()
    cursor.close()
    return render_template('nuser.html', result = account)

@app.route('/ngroup')
def ngroup():
    return render_template('ngroup.html')

@app.route('/ngrp', methods = ['POST', 'GET'])
def ngrp():
    if request.method == 'POST':
        nid = session['nid']
        gr = request.form['gr']
        var = (nid, gr)
        cursor = mydb.cursor()
        cursor.execute('insert into nusers values (%s, %s)', var)
        mydb.commit()
        cursor.close()
        if cursor.rowcount == 1:
            return render_template('ngroup.html')
        else:
            return render_template('ngroup.html')

@app.route('/napp')
def napp():
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM kreq where status1="pending"')
    account = cursor.fetchall()
    cursor.close()
    return render_template('napp.html', result = account)

@app.route('/nreq/<string:id>')
def nreq(id):
    cursor = mydb.cursor()
    cursor.execute('SELECT id FROM kreq where id ='+id)
    account = cursor.fetchone()
    cursor.execute('SELECT key1 FROM upload where id ='+ str(account[0]))
    account = cursor.fetchone()
    cursor.execute('update kreq set key1=%s, status1=%s where id=%s', (account[0], 'Approved', id))
    mydb.commit()
    if cursor.rowcount == 1:
        cursor.execute('SELECT * FROM kreq where status1="pending"')
        account = cursor.fetchall()
        cursor.close()
        return render_template('napp.html', result = account)
    else:
        cursor.execute('SELECT * FROM kreq where status1="pending"')
        account = cursor.fetchall()
        cursor.close()
        return render_template('napp.html', result = account)

@app.route('/nfiles')
def nfiles():
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM upload')
    account = cursor.fetchall()
    cursor.close()
    return render_template('nfiles.html', result = account)

@app.route('/nreg')
def nreg():
    return render_template('nreg.html')

@app.route('/netreg', methods = ['POST', 'GET'])
def netreg():
    if request.method == 'POST':
        name = request.form['name']
        com = request.form['com']
        uid = request.form['uid']
        pwd = request.form['pwd']
        mob = request.form['mob']
        loc = request.form['loc']
        var = (name, com, uid, pwd, mob, loc)
        cursor = mydb.cursor()
        cursor.execute('insert into net values (%s, %s, %s, %s, %s, %s)', var)
        mydb.commit()
        cursor.close()
        if cursor.rowcount == 1:
            return render_template('net.html')
        else:
            return render_template('nreg.html')

@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/ulogin', methods = ['POST', 'GET'])
def ulogin():
    if request.method == 'POST':
        uid = request.form['uid']
        pwd = request.form['pwd']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM user WHERE email = %s AND password = %s', (uid, pwd))
        account = cursor.fetchone()
        cursor.close()
        if account:
            session['uid'] = request.form['uid']
            session['name'] = account[0]
            return render_template('uhome.html', result = account[0])
        else:
            return render_template('user.html')
        
@app.route('/uhome')
def uhome():
    return render_template('uhome.html', result = session['name'])

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/ustore', methods = ['POST', 'GET'])
def ustore():
    if request.method == 'POST':
        uid = session['uid']
        fname = request.form['fname']
        f = request.files['file']
        n = f.filename
        fpath = "C:/Users/varsh/Desktop/mini proj 4th yr/MiniProject/MPNS11/static/file/"+n
        f.save(fpath)
        with open(fpath) as f:
            lines = f.readlines()
        l = ""
        for line in lines:
            l += line +" "
        key = Fernet.generate_key()
        fernet = Fernet(key)
        with open(fpath, 'rb') as file:
            original = file.read()
        encrypted = fernet.encrypt(original)
        efname = "C:/Users/varsh/Desktop/mini proj 4th yr/MiniProject/MPNS11/static/file/enc/"+n
        with open(efname, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)
        decrypted = fernet.decrypt(encrypted)
        dfname = "C:/Users/varsh/Desktop/mini proj 4th yr/MiniProject/MPNS11/static/file/dec/"+n
        with open(dfname, 'wb') as dec_file:
            dec_file.write(decrypted)
        var = (uid, fname, l, key, encrypted)
        cursor = mydb.cursor()
        cursor.execute('insert into upload values (0, %s, %s, %s, %s, %s)', var)
        mydb.commit()
        if cursor.rowcount == 1:
            cursor.close()
            return render_template('upload.html')
        else:
            cursor.close()
            return render_template('upload.html')

@app.route('/usch')
def usch():
    return render_template('usch.html')

@app.route('/ush', methods = ['POST', 'GET'])
def ush():
    if request.method == 'POST':
        fname = request.form['fname']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM upload where fname like "%' + fname + '%"')
        account = cursor.fetchall()
        cursor.close()
        return render_template('ush.html', result = account)

@app.route('/ukeys')
def ukeys():
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM upload where uid="'+session['uid']+'"')
    account = cursor.fetchall()
    cursor.execute('SELECT * FROM kreq where uid="'+session['uid']+'"')
    account1 = cursor.fetchall()
    cursor.close()
    return render_template('ukeys.html', result = account, result1 = account1)

@app.route('/fdown', methods = ['POST', 'GET'])
def fdown():
    if request.method == 'POST':
        fname = request.form['key']
        cursor = mydb.cursor()
        cursor.execute('SELECT fname FROM upload where key1 ="' + fname + '"')
        account = cursor.fetchone()
        cursor.close()
        return render_template('fdown.html', result = account)

@app.route('/udown/<string:id>')
def udown(id):
    session['fid'] = id
    return render_template('udown.html')

@app.route('/ureq/<string:id>')
def ureq(id):
    uid = session['uid']
    cursor = mydb.cursor()
    cursor.execute('SELECT fname FROM upload where id ='+ id)
    account = cursor.fetchone()
    var = (account[0], uid, 'pending', 'pending', id)
    cursor.execute('insert into kreq values (0, %s, %s, %s, %s, %s)', var)
    mydb.commit()
    cursor.close()
    if cursor.rowcount == 1:
        return render_template('uhome.html', result = session['name'])
    else:
        return render_template('uhome.html', result = session['name'])


@app.route('/unet')
def unet():
    cursor = mydb.cursor()
    cursor.execute('SELECT networkid FROM nusers where uids like "%' + session['uid'] + '%"')
    account = cursor.fetchall()
    lt = []
    for x in account:
        cursor.execute('SELECT * FROM net where email = "'+ x[0] +'"')
        lt.append(cursor.fetchone())
    cursor.close()
    return render_template('unet.html', result = lt)

@app.route('/reg')
def reg():
    return render_template('reg.html')

@app.route('/ureg', methods = ['POST', 'GET'])
def ureg():
    if request.method == 'POST':
        name = request.form['name']
        uid = request.form['uid']
        pwd = request.form['pwd']
        mob = request.form['mob']
        loc = request.form['loc']
        var = (name, uid, pwd, mob, loc)
        cursor = mydb.cursor()
        cursor.execute('insert into user values (%s, %s, %s, %s, %s)', var)
        mydb.commit()
        cursor.close()
        if cursor.rowcount == 1:
            return render_template('user.html')
        else:
            return render_template('reg.html')
        
@app.route('/logout')
def logout():
    session.pop('uid', None)
    session.pop('name', None)
    session.pop('nid', None)
    session.pop('nname', None)
    return render_template('index.html')

if __name__ == '__main__':
   app.run()