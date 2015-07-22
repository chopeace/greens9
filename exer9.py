import sqlite3,os
from bottle import route,get, run, debug, template, request, static_file, error, TEMPLATE_PATH, response
import ast,json,yaml
import mimeparse, os, sys

# only needed when you run Bottle on mod_wsgi
#from bottle import default_app

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

db_path = os.path.join(BASE_DIR, "contact.db")
print "DB_PATH:" , db_path

#conn = sqlite3.connect(db_path)

#TEMPLATE_PATH.insert(0, '/home/chopeace/weekly/exer8')
TEMPLATE_PATH.insert(0, BASE_DIR)

@get('/<filename:re:.*\.tpl>')
def javascripts(filename):
        return static_file(filename, root='/home/chopeace/weekly/exer9')

@route('/')
def contact_list():


    #conn = sqlite3.connect('todo.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT id, firstname,lastname,email,phone,notes FROM contact;")
    result = c.fetchall()
    c.close()

    output = template('list_contact.tpl', rows=result)
    return output


@route('/<no:int>', method='GET')
def view_item(no):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT id, firstname,lastname,email,phone,notes FROM contact WHERE id LIKE ?", (str(no)))
    cur_data = c.fetchone()

    return template('view_contact', old = cur_data, no = no)

@route('/new', method='GET')
def new_item():

    if request.GET.get('save','').strip():

        print "new: ", db_path
        firstname = request.GET.get('first_name', '').strip()
        lastname = request.GET.get('last_name', '').strip()
        email = request.GET.get('email', '').strip()
        phone = request.GET.get('phone', '').strip()
        notes = request.GET.get('notes', '').strip()

        conn = sqlite3.connect(db_path)

        c = conn.cursor()

        c.execute("INSERT INTO contact (firstname,lastname,email,phone,notes) VALUES (?,?,?,?,?)", (firstname,lastname,email,phone,notes))
        new_id = c.lastrowid

        conn.commit()
        c.close()

        return '<p>The new contact was inserted into the database, the ID is %s</p>\n <a href="/peace/exer9">List of people</a> ' % new_id
    else:
        return template('new_contact.tpl')



@route('/edit/<no:int>', method='GET')
def edit_item(no):

    if request.GET.get('save','').strip():

        firstname = request.GET.get('first_name', '').strip()
        lastname = request.GET.get('last_name', '').strip()
        email = request.GET.get('email', '').strip()
        phone = request.GET.get('phone', '').strip()
        notes = request.GET.get('notes', '').strip()

        print "save edit:?,db_path:?", (no,db_path)
        conn = sqlite3.connect(db_path)
        print "save edit: db connected"

        c = conn.cursor()
        c.execute("UPDATE contact SET firstname = ?, lastname = ?, email =?, phone= ?, notes=? WHERE id LIKE ?", (firstname,lastname,email,phone,notes,no))
        conn.commit()

        return '<p>The contact id %s was successfully updated</p>\n <a href="/peace/exer9">List of people</a> | <a href="/peace/exer9/%s">View Contact</a> ' %(no,no)

    else:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("SELECT id, firstname,lastname,email,phone,notes FROM contact WHERE id LIKE ?", (str(no)))
        cur_data = c.fetchone()

        return template('edit_contact', old = cur_data, no = no)

def db_update_contact(no,firstname,lastname,email,phone,notes):

    print "save edit:?,db_path:?", (no,db_path)
    conn = sqlite3.connect(db_path)
    print "save edit: db connected"

    c = conn.cursor()
    c.execute("UPDATE contact SET firstname = ?, lastname = ?, email =?, phone= ?, notes=? WHERE id LIKE ?", (firstname,lastname,email,phone,notes,no))
    conn.commit()

    print "updated : %d,%s,%s,%s,%s,%s" %(no,firstname,lastname,email,phone,notes)

def db_insert_contact(firstname,lastname,email,phone,notes):
    print "new: ", db_path
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO contact (firstname,lastname,email,phone,notes) VALUES (?,?,?,?,?)", (firstname,lastname,email,phone,notes))
    new_id = c.lastrowid
    conn.commit()
    c.close()

    print "inserted : %d,%s,%s,%s,%s,%s" %(1,firstname,lastname,email,phone,notes)

def db_select_contact_json(no):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT id, firstname,lastname,email,phone,notes FROM contact WHERE id LIKE ?", (str(no)))
    
    rows_count = cursor.execute(query_sql)
    if rows_count > 0:
        rs = cursor.fetchall()
        json_user = json.dumps(rs[0])
        user = yaml.safe_load(json_user)
        
    else:
        user = {}

    return user

def db_delete_contact(no):
    conn = sqlite3.connect(db_path)
    print "save delete: db connected"

    c = conn.cursor()
    c.execute("DELETE FROM contact WHERE id LIKE ?",str(no))
    conn.commit()
    print "delete_contact:%d" % no

@route('/item<item:re:[0-9]+>')
def show_item(item):

    #conn = sqlite3.connect('todo.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT firstname FROM contact WHERE id LIKE ?", (item))
    result = c.fetchall()
    c.close()

    if not result:
        return 'This item number does not exist!'
    else:
        return 'contact: %s' %result[0]

@route('/help')
def help():

    static_file('help.html', root='.')

@route('/json<json:re:[0-9]+>')
def show_json(json):

    #conn = sqlite3.connect('todo.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT firstname FROM contact WHERE id LIKE ?", (json))
    result = c.fetchall()
    c.close()

    if not result:
        return {'contact':'This item number does not exist!'}
    else:
        return {'contact': result[0]}

@route('/<no:int>.json', method='GET')
def select_contact(no):
    # id, firstname,lastname,email,phone,notes
    cur_data = db_select_contact(no)

    firstRow = cur_data[0]
    #json_data = json.dumps(cur_data[0]);#first row
    #print "json_data:", json_data
    #return template('{{json}}', json =json_data )
    return {
        "first_name": firstRow[1], 
        "last_name": firstRow[2], 
        "email": firstRow[3], 
        "phone": firstRow[4],
        "notes": firstRow[5]
    }

@route('/contact/<no:int>', method ='GET')
def select_contact(no):
    # Check to make sure JSON is ok
    type = mimeparse.best_match(['application/json'], request.headers.get('Accept'))
    if not type: return abort(406)

    print "Content-Type: %s" % request.headers.get('Content-Type')

    # Check to make sure the data we're getting is JSON
    #if request.headers.get('Content-Type') != 'application/json': return abort(415)
    response.headers.append('Content-Type', type)
    
    # id, firstname,lastname,email,phone,notes
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    rows_count = c.execute("SELECT id, firstname,lastname,email,phone,notes FROM contact WHERE id LIKE ?", (str(no)))

    if rows_count > 0:
        rs = c.fetchall()
        conn.close()
        firstRow = rs[0]
        print "firstRow: " , firstRow
        #json_data = json.dumps(cur_data[0]);#first row
        #print "json_data:", json_data
        #return template('{{json}}', json =json_data )
        return {
            "first_name": firstRow[1],
            "last_name": firstRow[2],
            "email": firstRow[3],
            "phone": firstRow[4],
            "notes": firstRow[5]
        }
    else:
        return {}

@route('/contact', method ='POST')
def insert_contact():
    # Check to make sure JSON is ok
    type = mimeparse.best_match(['application/json'], request.headers.get('Accept'))
    if not type: return abort(406)

    print "Content-Type: %s" % request.headers.get('Content-Type')

    # Check to make sure the data we're getting is JSON
    #if request.headers.get('Content-Type') != 'application/json': return abort(415)
    response.headers.append('Content-Type', type)

    # Read in the data
    data = json.load(request.body)
    firstname = data.get('first_name')
    lastname = data.get('last_name')
    email = data.get('email')
    phone = data.get('phone')
    notes = data.get('notes')

    print firstname,lastname,email,phone,notes
    db_insert_contact(firstname,lastname,email,phone,notes)

    # Basic sanity checks on the task
    #if iscommand(command): command = command
    #if not iscommand(command): return {"Result": "ERROR: your comamnd doesnot allowed in our api"}   #   abort(400)
    # Return the new rating for the entity
    return {
        "Result": "OK"
    }

# curl -XPUT -H'Content-type: application/json' -d'{"command": "turn_on_all"}' http://52.24.231.104:7070/api/ peace
@route('/contact/<no:int>', method ='PUT')
def update_contact(no):
    # Check to make sure JSON is ok
    type = mimeparse.best_match(['application/json'], request.headers.get('Accept'))
    if not type: return abort(406)

    print "Content-Type: %s" % request.headers.get('Content-Type')

    # Check to make sure the data we're getting is JSON
    #if request.headers.get('Content-Type') != 'application/json': return abort(415)
    response.headers.append('Content-Type', type)

    # Read in the data
    data = json.load(request.body)
    firstname = data.get('first_name')
    lastname = data.get('last_name')
    email = data.get('email')
    phone = data.get('phone')
    notes = data.get('notes')

    print no,firstname,lastname,email,phone,notes
    db_update_contact(no,firstname,lastname,email,phone,notes)

    # Basic sanity checks on the task
    #if iscommand(command): command = command
    #if not iscommand(command): return {"Result": "ERROR: your comamnd doesnot allowed in our api"}   #   abort(400)
    # Return the new rating for the entity
    return {
        "Result": "OK"
    }

@route('/contact/<no:int>', method='DELETE')
def delete_contact(no):
    db_delete_contact(no)
    #count = client.delete('/rating/'+entity)
    #if count == 0: return abort(404)
    #return { "rating": None }






@error(403)
def mistake403(code):
    return 'There is a mistake in your url!'

@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'


#debug(True)
#run(reloader=True)
#remember to remove reloader=True and debug(True) when you move your application from development to a productive environment
