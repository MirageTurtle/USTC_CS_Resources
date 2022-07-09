import logging
import os
from flask import Flask, render_template, request, redirect
from flask import send_from_directory
import pymysql
import datetime
import pandas as pd
import copy


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
)
app = Flask(__name__)


def connect_db(host, port, user, passwd, charset, database):
    db = pymysql.connect(
        host=host,
        port=port,
        user=user,
        passwd=passwd,
        charset=charset,
        db=database
    )
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    return db, cursor


def connect_bank():
    db, cursor = connect_db(
        host="127.0.0.1",
        port=3306,
        user="root",
        passwd="1234",
        charset="utf8",
        database="bank"
    )
    return db, cursor


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


# User part
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    # post register form
    username = pymysql.converters.escape_string(request.form.get("username"))
    password = request.form.get("password")
    logging.debug(
        f"information: Username-{username} Password-{password}"
    )

    # db = pymysql.connect(
    #     host="127.0.0.1",
    #     port=3306,
    #     user="root",
    #     passwd="1234",
    #     charset="utf8",
    #     db="bank"
    # )
    # cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    db, cursor = connect_bank()
    # check if username exists
    query_comm = f"select * from User where Username = '{username}'"
    logging.debug(f"query_comm: {query_comm}")
    cursor.execute(query_comm)
    query_data = cursor.fetchall()
    if query_data:
        cursor.close()
        db.close()
        return render_template('register.html', error="该用户名已存在。")
    # register new user
    insert_comm = f"insert into User(Username,Password) values('{username}','{password}')"
    logging.debug(f"insert_comm: {insert_comm}")
    try:
        cursor.execute(insert_comm)
        db.commit()
    except Exception as e:
        logging.warning(f"Exception {e} occurs when register new user.")
        db.rollback()
    cursor.close()
    db.close()
    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    # post login form
    username = pymysql.converters.escape_string(request.form.get("username"))
    password = request.form.get("password")
    logging.debug(
        f"information: Username-{username} Password-{password}"
    )
    # db = pymysql.connect(
    #     host="127.0.0.1",
    #     port=3306,
    #     user="root",
    #     passwd="1234",
    #     charset="utf8",
    #     db="bank"
    # )
    # cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    db, cursor = connect_bank()
    # check if user exists
    query_comm = f"select * from User where Username = '{username}'"
    logging.debug(f"query_comm: {query_comm}")
    cursor.execute(query_comm)
    query_data = cursor.fetchall()
    cursor.close()
    db.close()
    logging.debug(f"query_data: {query_data}")
    if not query_data:
        return render_template('login.html', error_under_username="该用户不存在。")
    # dict formation is from cursor=pymysql.cursors.DictCursor
    if query_data[0]["Password"] != password:
        return render_template('login.html', error_under_password="密码错误。")
    return redirect(f"/user/list")


# TODO: 显示密码和隐藏密码
@app.route("/user/list", methods=["GET", "POST"])
def user_list():
    # db = pymysql.connect(
    #     host="127.0.0.1",
    #     port=3306,
    #     user="root",
    #     passwd="1234",
    #     charset="utf8",
    #     db="bank"
    # )
    # cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    db, cursor = connect_bank()
    if request.method == "GET":
        query_comm = "select * from User"
        cursor.execute(query_comm)
        query_data = cursor.fetchall()
        logging.debug(f"query_data: {query_data}")
        cursor.close()
        db.close()

        return render_template('user_list.html', user_list=query_data)

    username = pymysql.converters.escape_string(request.form.get("Username"))
    query_comm = f"select * from User where Username = {username}"
    logging.debug(f"query_comm: {query_comm}")
    cursor.execute(query_comm)
    query_data = cursor.fetchall()
    logging.debug(f"query_data: {query_data}")
    cursor.close()
    db.close()

    return render_template('user_list.html', user_list=query_data)


@app.route('/user/add', methods=["GET", "POST"])
def add_user():
    if request.method == "GET":
        return render_template('user_add.html')
        # return render_template('register.html')

    username = pymysql.converters.escape_string(request.form.get("username"))
    password = request.form.get("password")
    logging.debug(f"[INFO]username: {username}, password: {password}")

    # db = pymysql.connect(
    #     host="127.0.0.1",
    #     port=3306,
    #     user="root",
    #     passwd="1234",
    #     charset="utf8",
    #     db="bank"
    # )
    # cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    db, cursor = connect_bank()
    # check if username exists
    query_comm = f"select * from User where Username = '{username}'"
    logging.debug(f"query_comm: {query_comm}")
    cursor.execute(query_comm)
    query_data = cursor.fetchall()
    logging.debug(f"query_data: {query_data}")
    if query_data:
        logging.info(f"Username {username} exists.")
        cursor.close()
        db.close()
        return render_template('user_list.html')
    # register new user
    insert_comm = f"insert into User(Username,Password) values('{username}','{password}')"
    logging.debug(f"insert_comm: {insert_comm}")
    try:
        cursor.execute(insert_comm)
        db.commit()
    except Exception as e:
        logging.warning(f"Exception {e} occurs when register new user.")
        db.rollback()
    cursor.close()
    db.close()

    return redirect('/user/list')


@app.route("/user/edit/<string:username>", methods=["GET", "POST"])
def update_user(username):
    if request.method == "GET":
        return render_template('user_edit.html')

    db, cursor = connect_bank()
    password = request.form.get("password")

    update_user_comm = f"update User set Password = '{password}' where Username = '{pymysql.converters.escape_string(username)}'"
    try:
        cursor.execute(update_user_comm)
        db.commit()
    except Exception as e:
        logging.warning(f"Exception {e} occurs when edit user info.")
        db.rollback()

    cursor.close()
    db.close()
    return redirect('/user/list')


@app.route("/user/delete/<string:username>")
def delete_user(username):
    # db = pymysql.connect(
    #     host="127.0.0.1",
    #     port=3306,
    #     user="root",
    #     passwd="1234",
    #     charset="utf8",
    #     db="bank"
    # )
    # cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    db, cursor = connect_bank()
    delete_comm = f"delete from User where Username = '{username}'"
    try:
        cursor.execute(delete_comm)
        db.commit()
    except Exception as e:
        logging.warning(f"Exception {e} occurs when register new user.")
        db.rollback()
    cursor.close()
    db.close()

    return redirect('/user/list')


# Bank part
@app.route("/bank/list")
def bank_list():
    db, cursor = connect_bank()
    query_comm = "select * from Bank"
    cursor.execute(query_comm)
    query_data = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('bank_list.html', bank_list=query_data)


# Client part
@app.route("/client/list", methods=["GET", "POST"])
# def client_list(**kwargs):
def client_list():
    db, cursor = connect_bank()

    # query_client_comm = "select * from Client"
    # cursor.execute(query_client_comm)
    # client_list = cursor.fetchall()

    # query_contact_comm = "select * from Contact"
    # cursor.execute(query_contact_comm)
    # contact_list = cursor.fetchall()
    query_comm = "select * from Client, Contact where Client.Client_ID = Contact.Client_ID"
    cursor.execute(query_comm)
    client_list = cursor.fetchall()
    logging.debug(f"Client List: {client_list}")

    cursor.close()
    db.close()

    # For search
    if request.method == "POST":
        Client_ID = request.form.get("Client_ID")
        Client_Name = pymysql.converters.escape_string(request.form.get("Client_Name"))
        Client_Tel = request.form.get("Client_Tel")
        Client_Address = request.form.get("Client_Address")
        # Contact_Name = request.form.get("Contact_Name")
        # Contact_Email = request.form.get("Contact_Email")
        # Contact_Tel = request.form.get("Contact_Tel")
        # Relation = request.form.get("Relation")

        if Client_ID:
            client_list = list(
                filter(
                    lambda x: x['Client_ID'] == Client_ID,
                    client_list
                )
            )
        if Client_Name:
            client_list = list(
                filter(
                    lambda x: x['Client_Name'] == Client_Name,
                    client_list
                )
            )
        if Client_Tel:
            client_list = list(
                filter(
                    lambda x: x['Client_Tel'] == Client_Tel,
                    client_list
                )
            )
        if Client_Address:
            client_list = list(
                filter(
                    lambda x: x['Client_Address'] == Client_Address,
                    client_list
                )
            )

    # if "error1" in kwargs.keys() or "error2" in kwargs.keys():
    #     return data_list
    # else:
    #     return render_template('client_list.html', client_list=client_list)
    return render_template('client_list.html', client_list=client_list)


@app.route('/client/add', methods=["GET", "POST"])
def client_add():
    if request.method == "GET":
        return render_template('client_add.html')

    Client_ID = request.form.get("Client_ID")
    Client_Name = pymysql.converters.escape_string(request.form.get("Client_Name"))
    Client_Tel = request.form.get("Client_Tel")
    Client_Address = request.form.get("Client_Address")
    Contact_Name = pymysql.converters.escape_string(request.form.get("Contact_Name"))
    Contact_Email = request.form.get("Contact_Email")
    Contact_Tel = request.form.get("Contact_Tel")
    Relation = request.form.get("Relation")

    db, cursor = connect_bank()

    query_comm = f"select * from Client where Client_ID = '{Client_ID}'"
    cursor.execute(query_comm)
    query_data = cursor.fetchall()
    if query_data:
        cursor.close()
        db.close()
        return render_template(
            "client_add.html",
            error_msg="The Client_ID you entered already exist."
        )

    insert_client_comm = f"insert into Client(Client_ID, Client_Name, Client_Tel, Client_Address) values('{Client_ID}', '{Client_Name}', '{Client_Tel}', '{Client_Address}')"
    insert_contact_comm = f"insert into Contact(Client_ID, Contact_Name, Contact_Email, Contact_Tel, Relation) values('{Client_ID}', '{Contact_Name}', '{Contact_Email}', '{Contact_Tel}', '{Relation}')"
    logging.debug(f"insert_client_comm: {insert_client_comm}")
    logging.debug(f"insert_contact_comm: {insert_contact_comm}")
    try:
        cursor.execute(insert_client_comm)
        cursor.execute(insert_contact_comm)
        db.commit()
    except Exception as e:
        logging.warning(f"Exception {e} occurs when add client.")
        db.rollback()
    cursor.close()
    db.close()

    return redirect('/client/list')


@app.route("/client/edit/<string:client_id>", methods=["GET", "POST"])
def client_edit(client_id):
    if request.method == "GET":
        return render_template('client_edit.html')

    Client_ID = client_id
    Client_Name = pymysql.converters.escape_string(request.form.get("Client_Name"))
    Client_Tel = request.form.get("Client_Tel")
    Client_Address = request.form.get("Client_Address")
    Contact_Name = pymysql.converters.escape_string(request.form.get("Contact_Name"))
    Contact_Email = request.form.get("Contact_Email")
    Contact_Tel = request.form.get("Contact_Tel")
    Relation = request.form.get("Relation")

    db, cursor = connect_bank()

    update_client_comm = f"update client set Client_Name = '{Client_Name}', Client_Tel = '{Client_Tel}', Client_Address = '{Client_Address}' where Client_ID = '{Client_ID}'"
    update_contact_comm = f"update contact set Contact_Name = '{Contact_Name}', Contact_Email = '{Contact_Email}', Contact_Tel = '{Contact_Tel}', Relation = '{Relation}' where Client_ID = '{Client_ID}'"

    try:
        cursor.execute(update_client_comm)
        cursor.execute(update_contact_comm)
        db.commit()
    except Exception as e:
        logging.warning(f"Exception {e} occurs when update client info.")

    cursor.close()
    db.close()

    return redirect('/client/list')


@app.route("/client/delete/<string:client_id>")
def client_delete(client_id):
    db, cursor = connect_bank()

    query_own_comm = f"select * from Own where Client_ID = '{client_id}'"
    query_pay_comm = f"select * from Pay where Client_ID = '{client_id}'"

    cursor.execute(query_own_comm)
    own_data = cursor.fetchall()
    cursor.execute(query_pay_comm)
    pay_data = cursor.fetchall()

    if own_data or pay_data:
        error_msg = f"The client {client_id} is not allowed to be deleted because this client has an account."
        query_client_comm = "select * from Client, Contact where Client.Client_ID = Contact.Client_ID"
        cursor.execute(query_client_comm)
        client_list = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template('client_list.html', client_list=client_list, error=error_msg)

    delete_client_comm = f"delete from Client where Client_ID = '{client_id}'"
    delete_contact_comm = f"delete from Contact where Client_ID = '{client_id}'"
    try:
        cursor.execute(delete_contact_comm)
        cursor.execute(delete_client_comm)
        db.commit()
    except Exception as e:
        logging.warning(f"Exception {e} occurs when delete client.")
        db.rollback()

    cursor.close()
    db.close()

    return redirect('/client/list')


# Account part
@app.route("/account/list", methods=["GET", "POST"])
def account_list():
    db, cursor = connect_bank()

    query_account_comm = "select * from Account"
    cursor.execute(query_account_comm)
    account_list = cursor.fetchall()

    query_cheque_account_comm = "select * from Cheque_Account"
    cursor.execute(query_cheque_account_comm)
    cheque_account_list = cursor.fetchall()

    query_saving_account_comm = "select * from Saving_Account"
    cursor.execute(query_saving_account_comm)
    saving_account_list = cursor.fetchall()

    query_own_comm = "select * from Own"
    cursor.execute(query_own_comm)
    own_list = cursor.fetchall()

    cursor.close()
    db.close()

    if request.method == "POST":
        Account_ID = request.form.get("Account_ID")
        Bank_Name = pymysql.converters.escape_string(request.form.get("Bank_Name"))
        Balance = request.form.get("Balance")
        # For search
        if Account_ID:
            account_list = list(
                filter(lambda x: x['Account_ID'] == Account_ID, account_list))
            cheque_account_list = list(
                filter(lambda x: x['Account_ID'] == Account_ID, cheque_account_list))
            saving_account_list = list(
                filter(lambda x: x['Account_ID'] == Account_ID, saving_account_list))
        if Bank_Name:
            account_list = list(
                filter(lambda x: x['Bank_Name'] == Bank_Name, account_list))
            cheque_account_list = list(
                filter(lambda x: x['Bank_Name'] == Bank_Name, cheque_account_list))
            saving_account_list = list(
                filter(lambda x: x['Bank_Name'] == Bank_Name, saving_account_list))
        if Balance:
            account_list = list(
                filter(lambda x: x['Balance'] == float(Balance), account_list))
            cheque_account_list = list(
                filter(lambda x: x['Balance'] == float(Balance), cheque_account_list))
            saving_account_list = list(
                filter(lambda x: x['Balance'] == float(Balance), saving_account_list))

    return render_template(
        'account_list.html',
        account_list=account_list,
        cheque_account_list=cheque_account_list,
        saving_account_list=saving_account_list,
        own_list=own_list
    )


@app.route('/account/add/<string:client_id>', methods=["GET", "POST"])
def account_add(client_id):
    if request.method == "GET":
        return render_template('account_add.html')

    Account_ID = request.form.get("Account_ID")
    Bank_Name = pymysql.converters.escape_string(request.form.get("Bank_Name"))
    Balance = request.form.get("Balance")
    Opening_Date = request.form.get("Opening_Date")
    Account_Type = request.form.get("Account_Type")

    db, cursor = connect_bank()

    query_target_account_comm = f"select * from Account where Account_ID = '{Account_ID}'"
    cursor.execute(query_target_account_comm)
    target_account_data = cursor.fetchall()
    if target_account_data:
        cursor.close()
        db.close()
        return render_template('account_add.html', error_account_id="The Account_ID you entered already exist.")

    query_target_bank_comm = f"select * from Bank where Bank_Name = '{Bank_Name}'"
    cursor.execute(query_target_bank_comm)
    target_bank_data = cursor.fetchall()
    if not target_bank_data:
        cursor.close()
        db.close()
        return render_template('account_add.html', error_bank_name="The Bank_Name you entered does not exist.")

    try:
        insert_account_comm = f"insert into Account(Account_ID, Bank_Name, Balance, Opening_Date) values('{Account_ID}', '{Bank_Name}', '{Balance}', '{Opening_Date}')"
        cursor.execute(insert_account_comm)
        insert_own_comm = f"insert into Own(Client_ID, Visited_Date, Account_ID) values('{client_id}', '{datetime.datetime.now().strftime('%Y-%m-%d')}', '{Account_ID}')"
        cursor.execute(insert_own_comm)
        db.commit()
    except Exception as e:
        logging.warning(f"Exception {e} occurs when insert account.")
        db.rollback()
    if Account_Type == "Saving":
        try:
            Interest_Rate = request.form.get("Interest_Rate")
            Currency_Type = request.form.get("Currency_Type")
            insert_saving_comm = f"insert into Saving_account(Account_ID, Interest_Rate, Currency_Type) values('{Account_ID}', '{Interest_Rate}', '{Currency_Type}')"
            cursor.execute(insert_saving_comm)
            db.commit()
        except Exception as e:
            logging.warning(f"Exception {e} occurs when insert saving_account.")
            db.rollback()
    else:
        try:
            Overdraft = request.form.get("Overdraft")
            insert_cheque_comm = f"insert into Cheque_account(Account_ID, Overdraft) values('{Account_ID}', '{Overdraft}')"
            cursor.execute(insert_cheque_comm)
            db.commit()
        except Exception as e:
            logging.warning(f"Exception {e} occurs when insert cheque_account.")
            db.rollback()

    cursor.close()
    db.close()

    return redirect('/account/list')


@app.route("/account/delete/<string:account_id>")
def account_delete(account_id):
    db, cursor = connect_bank()

    delete_saving_account_comm = f"delete from Saving_account where Account_ID = '{account_id}'"
    delete_cheque_account_comm = f"delete from Cheque_account where Account_ID = '{account_id}'"
    delete_own_comm = f"delete from Own where Account_ID = '{account_id}'"
    delete_account_comm = f"delete from Account where Account_ID = '{account_id}'"

    try:
        cursor.execute(delete_saving_account_comm)
        cursor.execute(delete_cheque_account_comm)
        cursor.execute(delete_own_comm)
        cursor.execute(delete_account_comm)
        db.commit()
    except Exception as e:
        logging.warning(f"Exception {e} occurs when delete account.")
        db.rollback()

    cursor.close()
    db.close()
    return redirect('/account/list')


@app.route("/account/edit/<string:account_id>", methods=["GET", "POST"])
def account_edit(account_id):
    if request.method == "GET":
        return render_template('account_edit.html')

    # Visited_Date = request.form.get("Visited_Date")
    Visited_Date = datetime.datetime.now().strftime('%Y-%m-%d')
    Account_Type = request.form.get("Account_Type")

    db, cursor = connect_bank()

    update_own_comm = f"update Own set Visited_Date = '{Visited_Date}' where Account_ID = '{account_id}'"
    cursor.execute(update_own_comm)
    db.commit()

    if Account_Type == "Saving":
        try:
            Interest_Rate = request.form.get("Interest_Rate")
            Currency_Type = request.form.get("Currency_Type")
            update_saving_comm = f"update Saving_account set Interest_Rate = '{Interest_Rate}', Currency_Type = '{Currency_Type}' where Account_ID = '{account_id}'"
            cursor.execute(update_saving_comm)
            logging.debug(f"update_saving_comm: {update_saving_comm}")
            db.commit()
        except Exception as e:
            logging.warning(f"Exception {e} occurs when update saving_account.")
            db.rollback()
    else:
        try:
            Overdraft = request.form.get("Overdraft")
            update_cheque_comm = f"update Cheque_account set Overdraft = '{Overdraft}' where Account_ID = '{account_id}'"
            cursor.execute(update_cheque_comm)
            db.commit()
        except Exception as e:
            logging.warning(f"Exception {e} occurs when update cheque_account.")
            db.rollback()

    cursor.close()
    db.close()

    return redirect('/account/list')


# Department part
@app.route("/department/list")
def department_list():
    db, cursor = connect_bank()
    query_comm = "select * from Department"
    try:
        cursor.execute(query_comm)
        query_data = cursor.fetchall()
    except Exception as e:
        logging.warning(f"Exception {e} occurs when query department data.")
        cursor.close()
        db.close()
        return render_template("user_list.html")
    cursor.close()
    db.close()
    return render_template('department_list.html', department_list=query_data)


# Employee part
@app.route("/employee/list")
def employee_list():
    db, cursor = connect_bank()

    query_employee_comm = f"select * from Employee"
    try:
        cursor.execute(query_employee_comm)
        employee_list = cursor.fetchall()
    except Exception as e:
        logging.warning(f"Exception {e} occurs when query employee data.")
        db.rollback()
    cursor.close()
    db.close()
    return render_template("employee_list.html", employee_list=employee_list)


@app.route("/employee/add")
def employee_add():
    return render_template("error.html", error_msg="还没写哈哈。")


# Loan part
@app.route("/loan/list", methods=["GET", "POST"])
def loan_list():
    db, cursor = connect_bank()
    query_loan_comm = "select * from Loan"
    query_pay_comm = "select * from Pay"
    cursor.execute(query_loan_comm)
    loan_list = cursor.fetchall()
    # update loan_status integer to humanlly string
    _dict = {
        -1: "Not issued",
        1: "Being issued",
        0: "Issued"
    }
    for item in loan_list:
        item["Loan_Status"] = _dict[item["Loan_Status"]]
    cursor.execute(query_pay_comm)
    pay_list = cursor.fetchall()
    # For Search
    if request.method == "POST":
        Loan_ID = request.form.get("Loan_ID")
        Bank_Name = request.form.get("Bank_Name")
        Loan_Amount = request.form.get("Loan_Amount")
        Loan_Status = request.form.get("Loan_Status")
        Pay_already = request.form.get("Pay_already")
        if Loan_ID:
            loan_list = list(filter(lambda x: x["Loan_ID"] == Loan_ID, loan_list))
            pay_list = list(filter(lambda x: x["Loan_ID"] == Loan_ID, pay_list))
        if Bank_Name:
            loan_list = list(filter(lambda x: x["Bank_Name"] == Bank_Name, loan_list))
            pay_list = list(filter(lambda x: x["Bank_Name"] == Bank_Name, pay_list))
        if Loan_Amount:
            loan_list = list(filter(lambda x: x["Loan_Amount"] == Loan_Amount, loan_list))
            pay_list = list(filter(lambda x: x["Loan_Amount"] == Loan_Amount, pay_list))
        if Loan_Status:
            loan_list = list(filter(lambda x: x["Loan_Status"] == Loan_Status, loan_list))
            pay_list = list(filter(lambda x: x["Loan_Status"] == Loan_Status, pay_list))
        if Pay_already:
            loan_list = list(filter(lambda x: x["Pay_already"] == Pay_already, loan_list))
            pay_list = list(filter(lambda x: x["Pay_already"] == Pay_already, pay_list))
    return render_template("loan_list.html", loan_list=loan_list, pay_list=pay_list)


@app.route("/loan/add", methods=["GET", "POST"])
def loan_add():
    # db, cursor = connect_bank()
    # query_bank_comm = "select * from Bank"
    # cursor.execute(query_bank_comm)
    # bank_list = cursor.fetchall()
    if request.method == "GET":
        # cursor.close()
        # db.close()
        # return render_template("loan_add.html", bank_list=bank_list)
        return render_template("loan_add.html")
    Loan_ID = request.form.get("Loan_ID")
    Bank_Name = pymysql.converters.escape_string(request.form.get("Bank_Name"))
    # logging.debug(f"Bank_Name: {Bank_Name}")
    Loan_Amount = request.form.get("Loan_Amount")
    Loan_Status = -1
    Pay_already = 0.0
    # Test data
    db, cursor = connect_bank()
    query_target_loan_comm = f"select * from Loan where Loan_ID = '{Loan_ID}'"
    cursor.execute(query_target_loan_comm)
    target_loan_data = cursor.fetchall()
    if target_loan_data:
        error_msg = "The Loan_ID you entered already exists."
        cursor.close()
        db.close()
        # return render_template("loan_add.html", bank_list=bank_list, error_loan_id=error_msg)
        return render_template("loan_add.html", error_loan_id=error_msg)
    query_target_bank_comm = f"select * from Bank where Bank_Name = '{Bank_Name}'"
    cursor.execute(query_target_bank_comm)
    target_bank_data = cursor.fetchall()
    if not target_bank_data:
        error_msg = "The Bank_Name you entered doesn't exist."
        cursor.close()
        db.close()
        # return render_template("loan_add.html", bank_list=bank_list, error_bank_name=error_msg)
        return render_template("loan_add.html", error_bank_name=error_msg)
    # insert data
    try:
        insert_loan_comm = f"insert into Loan(Loan_ID, Bank_Name, Loan_Amount, Loan_Status, Pay_already, Opening_Date) values('{Loan_ID}', '{Bank_Name}', '{Loan_Amount}', '{Loan_Status}', '{Pay_already}', '{datetime.datetime.now().strftime('%Y-%m-%d')}')"
        cursor.execute(insert_loan_comm)
        db.commit()
    except Exception as e:
        logging.warning(f"Exception {e} occurs when insert new loan.")
        db.rollback()
    cursor.close()
    db.close()
    return redirect("/loan/list")


@app.route("/loan/delete/<string:loan_id>")
def loan_delete(loan_id):
    db, cursor = connect_bank()
    query_target_loan_comm = f"select Loan_Status from Loan where Loan_ID = '{loan_id}'"
    cursor.execute(query_target_loan_comm)
    target_loan_status = cursor.fetchall()
    logging.debug(f"Loan Status: {target_loan_status}")
    if not target_loan_status:
        error_msg = f"Loan with ID {loan_id} doesn't exist."
        # logging.info(f"Loan with ID {loan_id} doesn't exist.")
        cursor.close()
        db.close()
        return render_template("error.html", error_msg=error_msg)
    if target_loan_status[0]["Loan_Status"] != 1:  #    not being issued
        delete_loan_comm = f"delete from Loan where Loan_ID = '{loan_id}'"
        logging.debug(f"delete_loan_comm: {delete_loan_comm}")
        try:
            cursor.execute(delete_loan_comm)
            db.commit()
        except Exception as e:
            logging.warning(f"Exception {e} occurs when delete loan.")
            db.rollback()
    else:
        error_msg = f"The loan with ID {loan_id} is being issued and not allowed to delete."
        return render_template("error.html", error_msg=error_msg)
    cursor.close()
    db.close()
    return redirect("/loan/list")


# Pay is working with loan
@app.route("/pay/add", methods=["GET", "POST"])
def pay_add():
    if request.method == "GET":
        return render_template('pay_add.html')

    logging.debug(f"Form: {request.form}")
    Client_ID = request.form.get("Client_ID")
    Loan_ID = request.form.get("Loan_ID")
    Pay_ID = request.form.get("Pay_ID")
    Pay_Amount = request.form.get("Pay_Amount")
    Pay_Date = request.form.get("Pay_Date")

    db, cursor = connect_bank()
    query_target_pay_comm = f"select * from Pay where Client_ID = '{Client_ID}' and Loan_ID = '{Loan_ID}' and Pay_ID = '{Pay_ID}'"
    cursor.execute(query_target_pay_comm)
    pay_data = cursor.fetchall()
    if pay_data:
        error_msg = "The (Client_ID, Loan_ID, Pay_ID) you entered already exist."
        cursor.close()
        db.close()
        return render_template("pay_add.html", error=error_msg)
    # Test data
    query_target_client_comm = f"select * from Client where Client_ID = '{Client_ID}'"
    cursor.execute(query_target_client_comm)
    target_client_data = cursor.fetchall()
    query_target_loan_comm = f"select * from Loan where Loan_ID = '{Loan_ID}'"
    cursor.execute(query_target_loan_comm)
    target_loan_data = cursor.fetchall()

    error_client_msg = ""
    error_loan_msg = ""
    if not target_client_data:
        error_client_msg = "The Client_ID you entered doesn't exist."
    if not target_loan_data:
        error_loan_msg = "The Loan_ID you entered doesn't exist."
    if error_client_msg or error_loan_msg:
        return render_template("pay_add.html", error_client_id=error_client_msg, error_loan_id=error_loan_msg)
    # insert data and update loan status
    try:
        insert_pay_comm = f"insert into Pay(Client_ID, Loan_ID, Pay_ID, Pay_Amount, Pay_Date) values('{Client_ID}', '{Loan_ID}', '{Pay_ID}', '{Pay_Amount}', '{Pay_Date}')"
        cursor.execute(insert_pay_comm)
        query_target_loan_comm = f"select * from Loan where Loan_ID = '{Loan_ID}'"
        cursor.execute(query_target_loan_comm)
        logging.debug("FLAG")
        target_loan = cursor.fetchall()[0]
        Pay_already = float(target_loan["Pay_already"])
        Loan_Amount = float(target_loan["Loan_Amount"])
        Pay_already += float(Pay_Amount)
        logging.debug(f"Loan_Amount: {Loan_Amount}, Pay_already: {Pay_already}")
        # Loan_Amount
        # 防止付款比贷款多的情况发生
        if Pay_already > Loan_Amount:
            exception_msg = "Pay_already is larger than Pay_Amount."
            raise Exception(exception_msg)
        elif Pay_already == Loan_Amount:
            loan_status = 0  # Issued
        else:
            loan_status = 1  # Being issued
        # update loan status
        update_loan_comm = f"update Loan set Loan_Status = '{loan_status}', Pay_already = '{Pay_already}' where Loan_ID = '{Loan_ID}'"
        cursor.execute(update_loan_comm)
        db.commit()
    except Exception as e:
        logging.warning(f"Exception {e} occurs when insert pay data.")
        db.rollback()
    cursor.close()
    db.close()
    return redirect("/loan/list")


@app.route("/business/list")
def business_list():
    # return render_template("business_list.html")
    def get_year(date):
        return date.year

    def get_month(date):
        return str(date.year) + "-" + str(date.month)

    def get_quarter(date):
        return str(date.year) + "-" + str(int((date.month - 1) / 3) + 1)

    db, cursor = connect_bank()
    query_account_comm = "select * from Account"
    query_loan_comm = "select * from Loan"
    cursor.execute(query_account_comm)
    account_list = cursor.fetchall()
    cursor.execute(query_loan_comm)
    loan_list = cursor.fetchall()
    cursor.close()
    db.close()

    # 处理bank
    bank_dict = {}
    # bank_account_list = {}
    logging.debug(f"account list: {account_list}")
    for item in account_list:
        if item["Bank_Name"] in bank_dict.keys():
            bank_dict[item["Bank_Name"]].append({"date": item["Opening_Date"], "balance": item["Balance"]})
            # bank_account_list[item["Bank_Name"]].append({"date": item["Opening_Date"]}, "account": )
        else:
            bank_dict[item["Bank_Name"]] = [{"date": item["Opening_Date"], "balance": item["Balance"]}]
    logging.debug(f"bank_dict: {bank_dict}")

    bank_balance_year = {}
    bank_balance_quarter = {}
    bank_balance_month = {}
    bank_account_year = {}
    bank_account_quarter = {}
    bank_account_month = {}
    list_for_year = []
    list_for_quarter = []
    list_for_month = []
    for item in bank_dict:
        list_for_year = bank_dict[item]
        list_for_year = pd.DataFrame(list_for_year)
        list_for_quarter = copy.deepcopy(list_for_year)
        list_for_month = copy.deepcopy(list_for_year)

        list_for_year["date"] = list_for_year["date"].apply(get_year)
        data_dict = list_for_year.groupby('date').balance.apply(list).to_dict()
        logging.debug(f"data_dict: {data_dict}")
        account_num = {}
        for key, value in data_dict.items():
            account_num[key] = len(value)
        bank_account_year[item] = account_num
        for key in data_dict.keys():
            data_dict[key] = sum(data_dict[key])
        bank_balance_year[item] = data_dict
        logging.debug(f"bank_account_year: {bank_account_year}")
        # logging.debug(f"bank_balance_year: {bank_balance_year}")

        list_for_quarter["date"] = list_for_quarter["date"].apply(get_quarter)
        data_dict2 = list_for_quarter.groupby('date').balance.apply(list).to_dict()
        account_num = {}
        for key, value in data_dict2.items():
            account_num[key] = len(value)
        bank_account_quarter[item] = account_num
        for key in data_dict2.keys():
            data_dict2[key] = sum(data_dict2[key])
        bank_balance_quarter[item] = data_dict2

        list_for_month["date"] = list_for_month["date"].apply(get_month)
        data_dict3 = list_for_month.groupby('date').balance.apply(list).to_dict()
        account_num = {}
        for key, value in data_dict3.items():
            account_num[key] = len(value)
        bank_account_month[item] = account_num
        for key in data_dict3.keys():
            data_dict3[key] = sum(data_dict3[key])
        bank_balance_month[item] = data_dict3

    # 处理loan
    loan_dic = {}
    logging.debug(f"Loan list: {loan_list}")
    for item in loan_list:
        if item["Bank_Name"] in loan_dic.keys():
            loan_dic[item["Bank_Name"]].append({"date": item["Opening_Date"], "balance": item["Loan_Amount"]})
        else:
            loan_dic[item["Bank_Name"]] = [{"date": item["Opening_Date"], "balance": item["Loan_Amount"]}]

    loan_balance_year = {}
    loan_balance_quarter = {}
    loan_balance_month = {}
    list_for_year = []
    list_for_quarter = []
    list_for_month = []
    for item in loan_dic:
        list_for_year = loan_dic[item]
        list_for_year = pd.DataFrame(list_for_year)
        list_for_quarter = copy.deepcopy(list_for_year)
        list_for_month = copy.deepcopy(list_for_year)

        list_for_year["date"] = list_for_year["date"].apply(get_year)
        data_dict = list_for_year.groupby('date').balance.apply(list).to_dict()
        for key in data_dict.keys():
            data_dict[key] = sum(data_dict[key])
        loan_balance_year[item] = data_dict

        list_for_quarter["date"] = list_for_quarter["date"].apply(get_quarter)
        data_dict2 = list_for_quarter.groupby('date').balance.apply(list).to_dict()
        for key in data_dict2.keys():
            data_dict2[key] = sum(data_dict2[key])
        loan_balance_quarter[item] = data_dict2

        list_for_month["date"] = list_for_month["date"].apply(get_month)
        data_dict3 = list_for_month.groupby('date').balance.apply(list).to_dict()
        for key in data_dict3.keys():
            data_dict3[key] = sum(data_dict3[key])
        loan_balance_month[item] = data_dict3

    return render_template(
        'business_list.html',
        bank_balance_year=bank_balance_year,
        bank_balance_quarter=bank_balance_quarter,
        bank_balance_month=bank_balance_month,
        loan_balance_year=loan_balance_year,
        loan_balance_quarter=loan_balance_quarter,
        loan_balance_month=loan_balance_month,
        bank_account_year=bank_account_year
    )



if __name__ == "__main__":
    app.run(debug=True, port=4000)
