from google.cloud import datastore
from flask import Flask,render_template,jsonify,request,redirect,send_from_directory,url_for,make_response
import datetime
import requests
import bcrypt
import uuid
import os
DS = datastore.Client()
EVENT = 'Event' 
#ROOT = DS.key('Event', 'root') 
app = Flask(__name__,static_url_path='')
asset_folder = os.path.join(app.root_path,'www')

print("INto main")
@app.route('/')
def test():
    user_id = request.cookies.get('secret')
    print('Server Reached')
    print(os.getcwd())
    print(user_id)
    if not user_id:
        #query=DS.query(kind='Event')
        #query=query.add_filter('token_id','=',user_id).fetch()
        #val=list(query)
        #if val:
        print(os.getcwd())
        return redirect("/login?foo=123")
        #return send_from_directory('static','index.html')
        #return redirect("/www/index.html?fffg=158855")

        #return send_from_directory('www','registration.html')             
   # else:
        #return send_from_directory('www','registration.html')
    #root_dir = os.path.dirname(os.getcwd())
    #print('main try')
    #print(root_dir)
    #print(os.path.join(root_dir,'static'))
    #return send_from_directory(os.path.join(root_dir,'static'),'index.html')

    return send_from_directory('static','index.html')

    #return redirect("/login")
#@app.route('/')
#def mainpage():
#    print('into index')
#    user_id = request.cookies.get('username')
#    print('after id')
#    print('Printing + '+user_id)
#    if user_id
#        print('Success'+user_id)
       # user = database.get(user_id)
        #if user:
            # Success!
   #     return send_from_directory('www','index.html')
        #return redirect('/www/index.html')
        #else:
        #    return redirect(url_for('/registration'))
#    else:
#        print('No user id')
#        return send_from_directory('www','login.html')
        #return redirect('loginhtm')
    #return send_from_directory('index.html', www)


@app.route('/index.html')
def index():
    print("in index3")
    print(os.getcwd())
    return send_from_directory('static','index.htm')
    #return render_template('index.html')





@app.route('/register',methods=["POST","GET"])
def register():
     if request.method == 'GET':
          print('get registration')
          return send_from_directory('static','registration.html')
     print('hereRegister')
     data = request.get_json(force = True)
     entity = datastore.Entity(key=DS.key(EVENT))
     #entity.update({'username': data['username'], 'pass': data['pass']})
     passwd=data['pass'].encode("utf-8")
     salt = bcrypt.gensalt(5)
     hashed = bcrypt.hashpw(passwd, salt)
     print(salt)
     print(hashed)
     entity.update({'username': data['username'], 'pass': hashed})
     #Ds.put(entity)
     token = data['username'] + '1234'
     response = redirect("/?g=1234")
     response.set_cookie('secret',token,max_age=60*2)
     entity.update({'token_id':token})
     DS.put(entity)    
     return response   


@app.route('/logout',methods=["POST","GET"])
def logout():
      response = make_response(redirect("/?g=123"))
      response.set_cookie('secret','',max_age=0)
      print('Logout')
      #data = request.get_json(force = True)
      sess=request.cookies.get('secret')
      print(sess)
      DS.delete(DS.key('session', sess))
      return response  


@app.route('/login',methods=["POST","GET"])
def login():
    if request.method == 'POST':
        print('herePost')
        data = request.get_json(force = True)
        v = data['username']
        query=DS.query(kind='Event')
        print(query)
        print('Query Generation')
        query=query.add_filter('username','=',v).fetch()
        val=list(query)
        #val=v1[0]
        print(val)
#        return 'Done with login check'
#    return 'out'
        k = DS.key('Event')
        #k = DS.key('Event',parent=ROOT)
        #print(k)
        #val=DS.get(k)
        #e=datastore.Entity(key=k)
        #e['username']=data['username']
        #e['pass']=data['pass']
#       #print(val)
        #print(e)
        #DS.put(e)
        #print('Saved {}: {}'.format(task.key.name, task['description']))
        #return ''
        if val:
             passwd=data['pass'].encode("utf-8")
             #salt = bcrypt.gensalt(5)
             print(val[0]['pass'])
             hashed = bcrypt.hashpw(passwd, val[0]['pass'])
             print(hashed)
             #if val['pass']==hashed:
                
             if hashed==val[0]['pass']:
                token = str(uuid.uuid1())
                session = datastore.Entity(key=DS.key('session', token))
                session.update({
                    'username': data['username'],
                    'exp': 1,
                })
                DS.put(session)

                #token = data['username'] + '1234'
                # Set-Cookie: username= 1234; path=/;
                #response = make_response("")
                #response = make_response(redirect("/index.html"))
                response = redirect("/?g=1234")
                print("Redirected tiot")
                #response.headers['location'] = url_for('test')
                response.set_cookie('secret',token,max_age=60*2)
                print('redirected now')
                #print('auth')
                #val[0].update({'token_id':token})
                #DS.put(val[0])
                print(response)
                return response
             #else:
             print('Iam unath login again')
             return redirect('/login?f=1234')

        #return redirect('/login?g=1234')
        return redirect('/register')
        #else: 
             #print('inelse-register')
             #return render_template('index.html')
        #     return send_from_directory('static','registration.html')
    #else:
    print('Login Get request')
    return send_from_directory('static','login.html')

#@app.route('/event',methods=["POST","GET"])
#def insert():
    '''
        puts json object into datastore
        checks for yearless date and correspondingly assigns year
         
    '''
#    data = request.get_json(force = True)
#    entity = datastore.Entity(key=DS.key(EVENT, parent=ROOT))
#    if len(data['date'].split('-'))<3:
#        x=datetime.datetime.now()
#        yr=x.year
#        m=x.month
#        d=x.day
#        l=data['date'].split('-')
#        if m>int(l[1]):
#            yr=yr+1
#        elif m==l[1]:
#            if d>int(l[2]):
#                yr=yr+1
#            else:
#                yr=yr
#        data['date']=str(yr)+'-'+data['date']
        
#    entity.update({'name': data['name'], 'date': data['date']})
#    DS.put(entity)
#    return ''



