from google.cloud import datastore
from flask import Flask,render_template,jsonify,request,redirect,send_from_directory,url_for,make_response
import datetime
import requests
import bcrypt
import uuid
import os
import pytz
DS = datastore.Client()
EVENT = 'Event' 
USER = 'User'
ROOT = DS.key('Event', 'root') 
app = Flask(__name__,static_url_path='')
asset_folder = os.path.join(app.root_path,'www')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 30


# Redirects to / url on startup and then checks for cookie 
# if cookie exitst return index page else redirects to /login 
@app.route('/')
def test():
    user_id = request.cookies.get('secret')
    if not user_id: 
        nw=datetime.datetime.now()
        s=nw.strftime("%m,%d,%Y, %H,%M%S")
        return redirect("/login?"+s)
    try :
        response = make_response(redirect('/index.html',302))
        response.cache_control.max_age = 30
        response.headers['Cache-Control'] = 'no-store'
        return response
    except Exception as e:
        return str(e)

# Generates the user key for the current user and returns username for that user 
# Checks for invalid session token as well.
def get_user(ss):
    if not ss:
        return None
    s = DS.get(DS.key('session', ss))
    if not s:
        return None
    ed = s.get('exp')
    if ed <= pytz.utc.localize(datetime.datetime.now()):
        return None
    username = s.get('username')
    return username


#Returns event data for the current user
#Queries session  by the  session id to get data and  then fetches  data for the current user key  from the events table
@app.route('/events',methods=["GET"])
def get_data():
    user = get_user(request.cookies.get('secret'))        
    k=DS.key(USER,user)
    vals = DS.query(kind=EVENT, ancestor=k).fetch()
    return jsonify({'events':[{'name':v['name'],'date':v['date'],'id':v.id }
        for v in sorted(vals,key = lambda i:i['date'])],
    })


# Updates event data table with new event name and date in datastore

@app.route('/event',methods=["POST","GET"])
def insert():
    data = request.get_json(force = True)
    user = get_user(request.cookies.get('secret'))
    entity = datastore.Entity(key=DS.key(EVENT, parent=DS.key(USER, user)))
    if len(data['date'].split('-'))<3:
        x=datetime.datetime.now()
        yr=x.year
        m=x.month
        d=x.day
        l=data['date'].split('-')
        if m>int(l[1]):
            yr=yr+1
        elif m==l[1]:
            if d>int(l[2]):
                yr=yr+1
            else:
                yr=yr
        data['date']=str(yr)+'-'+data['date']
        
    entity.update({'name': data['name'], 'date': data['date']})
    DS.put(entity)
    return ''


# Provdies the index page to user.
@app.route('/index.html')
def index():
    response = make_response(send_from_directory('static','index.html'))
    response.cache_control.max_age = 30
    response.headers['Cache-Control'] = 'no-store'
    return response


@app.route('/admin')
def admin():
    print("in admin")
    return send_from_directory('static','admin.html')


# Registers new user into the User kind 
# Sets up a new session for a new user and sets; 
# Sets the  session cookie on the browser with unique session  token id value
@app.route('/register',methods=["POST","GET"])
def register():
     if request.method == 'GET':
          print('get registration')
          return send_from_directory('static','registration.html')
     data = request.get_json(force = True)
     token = str(uuid.uuid1())
     username=data['username']
     entity = datastore.Entity(key=DS.key(USER,username))
     passwd=data['pass'].encode("utf-8")
     salt = bcrypt.gensalt(5)
     hashed = bcrypt.hashpw(passwd, salt)
     entity.update({'username': data['username'], 'pass': hashed})
     session = datastore.Entity(key=DS.key('session', token))
     expt= datetime.datetime.now()+datetime.timedelta(hours=1)
     session.update({
        'username': data['username'],
         'exp': expt,
      })
     DS.put(session)
 
     response = redirect("/index.html")
     response.set_cookie('secret',token,max_age=60*60)
     DS.put(entity)   
     response.cache_control.max_age = 30
     response.headers['Cache-Control'] = 'no-store'
     return response   


#logs out user from index page and deletes current session .
@app.route('/logout',methods=["POST","GET"])
def logout():
      sess=request.cookies.get('secret')
      DS.delete(DS.key('session', sess))
      return ''   


#Deltes session after standard time of  1 hour .
@app.route('/delete_session')
def delete_session():
    try: 
        query=DS.query(kind='session').fetch()
        val=list(query)
        nw=datetime.datetime.now()
        for session in val :
            if  pytz.utc.localize(nw)  > session['exp']:
                k=DS.key('session',session.key.name)
                DS.delete(k)
        return {'sessions deleted'}, 200

    except Exception as e :
        return str(e)


#Checks for user username and password against datastore and validates password hash 
# If user record matches , redirects to the index page
# If user not is datastore redirects to register page to get new user data
@app.route('/login',methods=["POST","GET"])
def login():
    if request.method == 'POST':
        data = request.get_json(force = True)
        v = data['username']
        query=DS.query(kind=USER)
        query=query.add_filter('username','=',v).fetch()
        val=list(query)
        k = DS.key('Event')
        if val:
             passwd=data['pass'].encode("utf-8")
             hashed = bcrypt.hashpw(passwd, val[0]['pass'])
                
             if hashed==val[0]['pass']:
                token = str(uuid.uuid1())
                session = datastore.Entity(key=DS.key('session', token))
                expt= datetime.datetime.now()+datetime.timedelta(hours=1)
                session.update({
                    'username': data['username'],
                    'exp': expt,
                })
                DS.put(session)
                response = make_response(redirect("/index.html"))
                response.set_cookie('secret',token,max_age=60*60)
                response.cache_control.max_age = 30
                response.headers['Cache-Control'] = 'no-store'
                return response,302
             return redirect('/login')

        return redirect('/register')
    return send_from_directory('static','login.html')


# Deletes event data for an id .
@app.route('/event/<event_id>',methods=["DELETE","GET"])
def deleteevent(event_id):
    user = get_user(request.cookies.get('secret'))
    k=k=DS.key(USER,user)
    DS.delete(DS.key(EVENT, int(event_id), parent=k))
    return ''
