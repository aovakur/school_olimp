from datetime import datetime
import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from FlaskWebProject2 import app
import datetime
from flask_wtf import FlaskForm
import sys
import logging
from flask_mysqldb import MySQL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import tabula
import pandas as pd
from io import StringIO
from flask_paginate import Pagination, get_page_parameter
from .create_db import CreateDB

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'aA123456'
app.config['MYSQL_DB'] = 'test'
mysql = MySQL(app)

CreateDB()

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page.""" 
    return render_template(
        'index.html', title="Главная страница")


class mail():
  def SentMessage(mail):
    try: 
      msg = MIMEMultipart()
      message = "Вы зарегистрировались на сайте СДЮШ Павловского Посада"
      password = "okgqmfflukipscgi"
      msg['From'] = "andrey@businessarchitecture.ru"
      msg['To'] = mail
      msg['Subject'] = "Регистрация на сайте детской школы"
      app.logger.info('Отправляется письмо')
      msg.attach(MIMEText(message, 'plain'))
      server = smtplib.SMTP_SSL('smtp.yandex.ru',465)
      server.login(msg['From'], password)
      server.sendmail(msg['From'], msg['To'], msg.as_string())
      server.quit()
      app.logger.info('Письмо отправлено')
      message = True
    except: 
      app.logger.info('Ошибка')
      message = False
    finally: 
      return bool(message)




class Regiter():
    name =None
    familia= None
    otchestvo=None
    mob=None
    mail= None
    org= ""
    password= None
    check= None
    rule= None
    have_child = None

class Parent(Regiter):
    child_name= None
    child_fam= None
    child_otchestvo= None
    child_bith= None
    have_child= None   

        # 1 - Администратор
        # 2 - Редактор
        # 3 - Преподаватель
        # 4 - Родитель
        # 3 - Гость  

@app.route('/auth/reg_success', methods=['GET', 'POST'])
def reg_success():
    if request.method == 'POST':
        con = mysql.connection
        if session['reg'] == 1:
            user = Parent()
            user.name = request.form['name']
            user.familia = request.form['familia']
            user.otchestvo = request.form['otchestvo']
            user.mob =request.form['mob']
            user.mail = request.form['mail']
            user.org = request.form['org']
            user.password = request.form['password']
            user.check = 0
            user.rule = 4
            user.have_child = int(request.form['countchild'])
            query = "INSERT INTO users (name,familia,otchestvo,mob,mail,have_child,org,password,check_rule, rule) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            args = (user.name,user.familia,user.otchestvo,user.mob,user.mail,user.have_child,user.org,user.password,user.check,user.rule)
            cur = con.cursor()
            cur.execute(query, args)
            con.commit()
            id = cur.lastrowid
            i=1

            while i<= user.have_child and user.have_child!=0:
               user.child_name= str(request.form['child_name'+str(i)])
               user.child_fam= str(request.form['child_fam'+str(i)])
               user.child_otchestvo= str(request.form['child_otchestvo'+str(i)])
               user.child_bith= str(request.form['child_bith'+str(i)])
               query1 = "INSERT INTO child (id,child_name,child_fam,child_otchestvo,child_bith) VALUES ( %s,%s, %s, %s, %s)"
               args2 = (id, user.child_name,user.child_fam,user.child_otchestvo,user.child_bith)
               cur = con.cursor()
               cur.execute(query1, args2)
               con.commit()
               i=i+1
            
            cur.close()
            msg = mail()

            if (mail.SentMessage(user.mail) == True):
               txt = f"{user.familia} {user.name} Вам отправлено письмо на почту {user.mail}"
            else: 
              txt = "Письмо не отправлено"

            return render_template('/auth/reg_success.html', message1 = "Вы успешно зарегистрировались как Родитель ",  message2 = txt, title="Форма регистрации")

        else:
             txt = "" 
             user = Regiter()
             user.name = request.form['name']
             user.familia = request.form['familia']
             user.otchestvo = request.form['otchestvo']
             user.mob =request.form['mob']
             user.mail = request.form['mail']
             user.org = request.form['org']
             user.password = request.form['password']
             user.check = 0
             user.rule = 3
             user.have_child = 0
             query = "INSERT INTO users (name,familia,otchestvo,mob,mail,have_child,org,password,check_rule, rule) VALUES (%s, %s, %s,%s, %s, %s, %s,%s, %s, %s)"
             args = (user.name,user.familia,user.otchestvo,user.mob,user.mail,user.have_child,user.org,user.password,user.check,user.rule)
             cur = con.cursor()
             cur.execute(query, args)
             con.commit()
             
             cur.close()

             if mail.SentMessage(user.mail) == True:
                 txt = f"{user.familia} {user.name} вам отправлено письмо на почту {user.mail}"
             else: txt = "Письмо не отправлено"
             return render_template('/auth/reg_success.html', message1 = "Вы успешно зарегистрировались как Преподаватель", message2 = txt, title="Форма регистрации")
    
    return redirect(url_for('register')) 


@app.route('/auth/login', methods=['GET', 'POST'])
def login():
      
        con = mysql.connection
        cur = con.cursor()
        error = None

        if request.method == 'POST':
          username = request.form['username']
          password = request.form['password']
          app.logger.info('%s', username)
          cur.execute ('SELECT * from users where mail=%s AND password=%s',(username,password))
          account = cur.fetchone()
          cur.close()

          if account:
            # Create session data, we can access this data in other routes
            session['logged_in'] = True
            session['id'] = account[0]
            session['name'] = account[1]
            session['familia'] = account[2]
            session['otchestvo'] = account[3]
            session['mob'] = account[4]
            session['mail'] = account[5]
            session['child'] = account[6]
            session['org'] = account[7]
            session['check_rule'] = account[9]
            session['rule'] = account[10]
           
            return redirect(url_for('authority')) 

        else: 
            return render_template('auth/login.html')

        return render_template('auth/login.html', error = "Ошибка в логине или пароле", title="Форма регистрации")

@app.route('/auth/logout')
def logout():
  session.pop('logged_in', None)
  session.pop('logged_in', None)
  flash('You were logged out')
  return redirect(url_for('home'))

MAX_FILE_SIZE = 1024 * 1024 + 1

@app.route('/olimpik/download', methods=['GET', 'POST'])
def olimpik():
  args = {"method": "GET"}
  PDF=""
  if request.method == "POST":
        file = request.files["file"]
        tmp = tabula.read_pdf(file, pages='all', multiple_tables=True)
        PDF = pd.read_csv(StringIO(str(tmp)),sep=";")
        app.logger.info(PDF)
        if bool(file.filename):
            file_bytes = file.read(MAX_FILE_SIZE)
            args["file_size_error"] = len(file_bytes) == MAX_FILE_SIZE

        args["method"] = "POST"
  return render_template('/olimpik/download.html', column_names=PDF.columns.values, row_data=list(PDF.values.tolist()))

@app.route('/lk/userlist')
def userlist():
  if session['logged_in'] == True and session['rule']=='1': 
    page1 = request.args.get('page', type=int, default=1)
    con = mysql.connection
    cur = con.cursor()
    cur.execute("SELECT * FROM users ORDER BY id ")
    row = cur.fetchall()
    pagination = Pagination(page=page1, total=6)
    return render_template('lk/userlist.html', data = row , pagination=pagination, title="Список пользователей")
  else:  
    return render_template('/auth/login.html', error = "У вас нет доступа, авторизуйтесь", title="Список пользователей")

@app.route('/lk/userok?ok=<int:id>', methods=['GET'])
@app.route('/lk/userok', methods=['GET'])
def userok():
  if session['logged_in'] == True and session['rule']=='1': 
      con = mysql.connection
      cur = con.cursor()
      id_useredit = request.args.get('ok')
      if (id_useredit!=None):
        cur.execute("UPDATE users set check_rule='1' where id=%s",(id_useredit,))
        con.commit()
        cur.close()
        return redirect(url_for('userok'))
      else:   
        cur.execute("SELECT * FROM users where check_rule=0 ORDER BY id ")
        row = cur.fetchall()
        nonerow = ""
        if not row:
          nonerow = "Нет записей для подтверждения"

        return render_template('/lk/ok_user.html', data = row, title="Список пользователей для подтверждения", msg = nonerow)
        
  else:  
    return render_template('/auth/login.html', error = "У вас нет доступа, авторизуйтесь")


@app.route('/lk/edit_user', methods=['GET'])
def edit_user(id =0):
  if request.method == 'GET':
      if session['logged_in'] == True and session['rule']=='1':
        id_userblock = request.args.get('block')
        id_useredit = request.args.get('edit')
        if  (id_useredit!=None and id_userblock==None):
            con = mysql.connection
            cur = con.cursor()
            cur.execute ('SELECT * from users where id=%s',(id_useredit,))
            data_edit_user = cur.fetchone()
            cur.close()
            return render_template('lk/edit_user.html', data = data_edit_user, title="Редактирования пользователя")
        if  (id_useredit==None and id_userblock!=None):
            return redirect(url_for('userlist'))
      else:  
        return render_template('/auth/login.html', error = "У вас нет доступа, авторизуйтесь1")

  return render_template('/auth/login.html', error = "У вас нет доступа, авторизуйтесь")

@app.route('/auth/register')
def register():
  session['reg'] = 1
  return render_template('auth/register.html', title="Регистрация")

@app.route('/auth/register_tutor')
def register_tutor():
  session['reg'] = 2 
  return render_template('auth/register_tutor.html', title="Регистрация преподавателя")


@app.route('/article/success', methods=['POST','get'])
def success():
  return render_template('article/edit_page.html')

@app.route('/article/edit_page', methods=['GET', 'POST'])
def edit_page():
  if request.method == 'POST':
    message ="Запись сохранена"
    return render_template('article/edit_page.html', message = message)
  else: 
    return render_template('article/edit_page.html')


@app.route('/lk')
def authority():
    try:
        if session['logged_in'] == True:
             return render_template('/lk/authority.html', title="Личный кабинет")   
        else: 
            return render_template('auth/login.html', error = "У вас нет доступа, авторизуйтесь")
    except:
        return render_template('auth/login.html', error = "У вас нет доступа, авторизуйтесь")

@app.route('/activity')
def activity():

    """Renders the activity page."""
    return render_template('activity.html' , title="Мероприятия")


@app.route('/statistic')
def statistic():
  try:
    if session['logged_in'] == True: 
      return render_template('statistic.html', title="Статистика")
    else: 
       return render_template('/auth/login.html', error = "У вас нет доступа, авторизуйтесь")
  except KeyError:
      return render_template('/auth/login.html', error= "У вас нет доступа, авторизуйтесь")

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html', title="Контакты")

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html', title="О нас")
