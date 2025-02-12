import datetime
from flask import Flask, jsonify, redirect, render_template_string, request, session, url_for
from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
#from ariadne.constants import PLAYGROUND_HTML
import subprocess
import psycopg2

# Connect to database
connection = psycopg2.connect(database="mydb", user="g.fabi", password="postgres", host="localhost", port=5432)
cursor = connection.cursor()

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/")
def index():
    if 'username'  not in session:
        return f'You are not logged in <a href="/login">Login</a>'
    return f'Logged in as {session["username"] } <a href="/logout">Logout</a>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'admin' and password == 'password':  # check user and password
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    return render_template_string('''
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    ''')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/date', methods=['GET'])
def get_date():
    if 'username' not in session:
        return  'You are not logged in <a href="/login">Login</a>'
    currentDate = datetime.date.today()
    strCurrentDate = str(currentDate)
    return jsonify({'date': strCurrentDate.strip()})

@app.route('/contatti', methods=['GET'])
def get_contatti():
    if 'username' not in session:
        return  'You are not logged in <a href="/login">Login</a>'
    tel = 123456789
    email = "gabrielefabi7@gmail.com"
    return jsonify({'telefono': tel, 'email': email})

@app.route('/time', methods=['GET'])
def get_time():
    if 'username' not in session:
        return  'You are not logged in <a href="/login">Login</a>'
    currentTime = datetime.datetime.now().time()
    strCurrentTime = str(currentTime)
    return jsonify({'time': strCurrentTime.strip()})


@app.route('/db', methods=['GET'])
def get_db():
    if 'username' not in session:
        return  'You are not logged in <a href="/login">Login</a>'
    cursor.execute("SELECT * from persons;")
    #Fetch all rows from database
    record = cursor.fetchall()
    return jsonify({'db': record})  

@app.route('/create', methods=['GET', 'POST'])
def create():
    if 'username' not in session:
        return  'You are not logged in <a href="/login">Login</a>'
    if request.method == 'POST':
        lastname = request.form.get('lastname')
        firstname = request.form.get('firstname')
        address = request.form.get('address')
        city = request.form.get('city')

        cursor.execute("INSERT INTO persons (lastname, firstname, address, city) VALUES (%s, %s, %s, %s)", (lastname, firstname, address, city))
        connection.commit()
        return redirect(url_for('index'))

    return render_template_string('''
        <form method="post">
            Lastname: <input type="text" name="lastname"><br>
            Firstname: <input type="text" name="firstname"><br>
            Address: <input type="text" name="address"><br>
            City: <input type="text" name="city"><br>
            <input type="submit" value="Submit">
        </form>
    ''')


@app.route('/form-example', methods=['GET', 'POST'])
def form_example():
    if 'username' not in session:
        return  'You are not logged in <a href="/login">Login</a>'
    # handle the POST request
    if request.method == 'POST':
        language = request.form.get('language')
        framework = request.form.get('framework')
        return  redirect(url_for('url_example', language=language, framework=framework))
                  
    # otherwise handle the GET request
    return '''
           <form method="POST">
               <div><label>Language: <input type="text" name="language"></label></div>
               <div><label>Framework: <input type="text" name="framework"></label></div>
               <input type="submit" value="Submit">
           </form>'''

@app.route('/url-example')
def url_example():
    if 'username' not in session:
        return  'You are not logged in <a href="/login">Login</a>'
    # if key doesn't exist, returns None
    language = request.args.get('language')

    framework = request.args.get('framework')

    return '''
              <h1>The language value is: {}</h1>
              <h1>The framework value is: {}</h1>'''.format(language, framework)

"""
type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, snake_case_fallback_resolvers
)


@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code
"""

if __name__ == '__main__':
    app.run()