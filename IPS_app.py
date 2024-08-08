from flask import render_template, Flask, request, redirect, url_for, flash
from Backend.IPS_database import IPS_db
from flask_mysqldb import MySQL
from Backend.vehicle_count import VehicleCount

app = Flask(__name__)
app.secret_key = "secret key"

# mysql connector to connect our database
connector = None  
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'ips_db'

app.config['MYSQL_HOST'] = 'sql12.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql12619059'
app.config['MYSQL_PASSWORD'] = '6GmWFCN3EJ'
app.config['MYSQL_DB'] = 'sql12619059'

mysql = MySQL(app)

# home page ------------------------------------------
@app.route('/')
def home_page():
    # flash('You are already registered, please log in')
    return render_template('Index.html')


# user pages ------------------------------------------
@app.route('/user')
def user():
    return render_template('Customer/login_page/user.html')

@app.route('/user_form', methods =["GET", "POST"])
def user_signup():
    # instance of database
    db = IPS_db(mysql)
    if request.method == 'POST':
        fname = request.form.get('fname')
        email = request.form.get('email')
        password = request.form.get('password')
        # insert data into user_table
        db.insert_user(fname, email, password)
    return redirect(url_for('home_page'))

@app.route('/user/login', methods=["GET", "POST"])
def user_login():
    # instance of database
    db = IPS_db(mysql)
    error_message = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # match data from user_table
        if db.match_user_data(email, password):
            return redirect(url_for('user_dashboard', name = email))
        else:
            error_message = "Invalid Username or Password, Login Again!!"
    return  render_template('Customer/login_page/user.html', error_message=error_message)

@app.route('/user/<name>/dashboard')
def user_dashboard(name):
    # making connection and creating a cursor
    cursor = mysql.connection.cursor()
    cursor.execute('Select distinct(company) from company_table;')
    company_info = cursor.fetchall()
    cursor.execute(f'Select fname from user_table where email="{name}";')
    u_name = cursor.fetchall()
    return render_template('Customer/dashboard.html', companies_name = company_info, data = '', name = name, u_name = u_name)

@app.route('/user/dashboard/update', methods=['GET', 'POST'])
def user_dashboard_update(company):
    # retrieve the values from the submitted form
    company = request.args.get('company')
    name = request.args.get('name')
    # making connection and creating a cursor
    cursor = mysql.connection.cursor()
    cursor.execute('Select distinct(company) from company_table;')
    company_info = cursor.fetchall()
    cursor.execute(f'Select company, address, block, slots, ip_address from company_table where company = "{company}";')
    table_data = cursor.fetchall()
    data = []
    ip_addresses = []
    slot_list = []
    for row in table_data:
        data.append(row[:-1])
        # commented below code to store slots no. to generate random no. between 0 and no. of slots only not ip_address of camera
        # ip_addresses.append(row[-1])
        slot_list.append(random.randint(0,row[-2]))
    # available_slots = VehicleCount(ip_addresses)
    available_slots = slot_list
    for i, d in enumerate(available_slots):
        data[i] = list(data[i])
        # subtracting total vehicle count from total parking slots to get available vacant slots
        data[i].append(int(data[i][3]) - int(d))
    # Now data contain - [company, address, block, slots, vacant slots]
    cursor.execute(f'Select fname from user_table where email="{name}";')
    u_name = cursor.fetchall()
    return render_template('Customer/dashboard.html', companies_name = company_info, data = data, name = name, u_name = u_name)

@app.route('/user/<name>/booking')
def bookingrequest(name):
    # making connection and creating a cursor
    cursor = mysql.connection.cursor()
    cursor.execute(f'Select fname from user_table where email="{name}";')
    u_name = cursor.fetchall()
    # fetching booking history
    cursor.execute(f'Select * from booking_table where email="{name}" order by parking_time desc;')
    data = cursor.fetchall()
    if len(data) == 0:
        data = ''    
    return render_template('Customer/bookingrequest.html', name = name, u_name = u_name, data = data)

@app.route('/user/<name>/bookingupdate', methods=["GET", "POST"])
def bookingupdate(name):
    # instance of database
    db = IPS_db(mysql)
    if request.method == 'POST':
        company = request.form.get('company')
        parking_time = request.form.get('parking_time')
        parking_duration = request.form.get('parking_duration')
        contact = request.form.get('contact')
        email = request.form.get('email')
        u_name = request.form.get('u_name')
        vehicle_no = request.form.get('vehicle_no')
        amount = 100*int(parking_duration)
        # insert data into user_table
        db.insert_booking_details(company, parking_time, parking_duration, contact, email, u_name, vehicle_no, amount)
    return redirect(url_for('bookingrequest', name = name))

# @app.route('/user/<name>/payment_history')
# def payment(name):
#     return render_template('Customer/payment_history.html', name = name)


# member pages --------------------------------------------------
@app.route('/member')
def member():
    return render_template('Admin/member.html')

@app.route('/member_form', methods =["GET", "POST"])
def member_signup():
    # instance of database
    db = IPS_db(mysql)
    if request.method == 'POST':
        fname = request.form.get('fname')
        email = request.form.get('email')
        contact = request.form.get('contact')
        address = request.form.get('address')
        password = request.form.get('password')
        # insert data into member_table
        db.insert_member(fname, email, contact, address, password) 
    return redirect(url_for('home_page'))

@app.route('/member/login', methods=["GET", "POST"])
def member_login():
    # instance of database
    db = IPS_db(mysql)
    error_message = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # match data from user_table
        if db.match_member_data(email, password):
            return redirect(url_for('member_dashboard', name = email))
        else:
            error_message = "Invalid Username or Password, Login Again!!"
    return  render_template('Admin/member.html', error_message=error_message)

@app.route('/member/<name>/dashboard')
def member_dashboard(name):
    # making connection and creating a cursor
    cursor = mysql.connection.cursor()
    cursor.execute(f'Select fname from member_table where email="{name}";')
    m_name = cursor.fetchall()
    cursor.execute(f'Select sum(slots) from company_table where email="{name}";')
    slots = cursor.fetchall()
    # print(slots)
    slots = slots[0][0]
    return render_template('Admin/dashboard.html', name = name, m_name = m_name, total_parking_slot = slots)

@app.route('/member/<name>/member_information')
def member_information(name):
    # making connection and creating a cursor
    cursor = mysql.connection.cursor()
    cursor.execute(f'Select * from company_table where email = "{name}";')
    member_info = cursor.fetchall()
    cursor.execute(f'Select fname from member_table where email="{name}";')
    m_name = cursor.fetchall()
    # mysql.connection.close() # Giving ERROR
    return render_template('Admin/member_information.html', data = member_info, name = name, m_name = m_name)

@app.route('/member/<name>/member_information/add', methods=["GET", "POST"])
def add_information(name):
    # instance of database
    db = IPS_db(mysql)
    if request.method == 'POST':
        company = request.form.get('company')
        address = request.form.get('address')
        block = request.form.get('block')
        slots = request.form.get('slots')
        ip_address = request.form.get('ip_address')
        email = request.form.get('email')
        # insert data into member_table
        db.add_company_info(company, address, block, slots, ip_address, email) 
    return redirect(url_for('member_information', name = name))

@app.route('/member/<name>/member_information/update', methods=["GET", "POST"])
def update_information(name):
    # instance of database
    db = IPS_db(mysql)
    if request.method == 'POST':
        company = request.form.get('company')
        address = request.form.get('address')
        block = request.form.get('block')
        slots = request.form.get('slots')
        ip_address = request.form.get('ip_address')
        email = request.form.get('email')
        id = request.form.get('id')
        # insert data into member_table
        db.update_company_info(company, address, block, slots, ip_address, email, id) 
    return redirect(url_for('member_information', name = name))



if __name__ == '__main__':
    app.run(debug=True)
