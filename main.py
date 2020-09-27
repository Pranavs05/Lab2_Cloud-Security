from google.cloud import datastore
from flask import Flask,render_template,jsonify,request,redirect,send_from_directory,url_for,make_response
import datetime
import requests
import bcrypt
import uuid
DS = datastore.Client()
EVENT = 'Event' 
#ROOT = DS.key('Event', 'root') 
app = Flask(__name__)

print("INto main")
@app.route('/')
def test():
    user_id = request.cookies.get('username')
    print('Server Reached')
    print(user_id)
    if user_id:
        return send_from_directory('www','index.html')
               
    else:
        return send_from_directory('www','login.html')
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



@app.route('/login',methods=["POST","GET"])
def login():
    if request.method == 'POST':
        print('herePost')
        data = request.get_json(force = True)
        v = data['username']
        query=DS.query(kind='event')
        query=query.add_filter('username','=','jameel').fetch()
        v1=list(query)
        val=v1[0]
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
             salt = bcrypt.gensalt(10)
             hashed = bcrypt.hashpw(passwd, salt)
             print(salt)
             print(hashed)
             #if val['pass']==hashed:
             if hashed:
                token = uuid.uuid1() 
                #token = data['username'] + '1234'
                # Set-Cookie: username= 1234; path=/;
                response = make_response(redirect('/'))
                print(response)
                response.set_cookie('secret',token,max_age=60)
                print('redirected')
                #print('auth')
                print(respone)
                return response
             else:
                print('Iam unath')
                return ''
        else: 
             print('inelse')
             return ''
         #return redirect(url_for('/www/login.html'))

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



