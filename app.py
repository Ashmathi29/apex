from flask import Flask, render_template, request, redirect, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "your_secret_key"

# MySQL Configuration
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "billing"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

# Home Page - Enter Consumer Details
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        consumer_id = request.form['consumer_id']
        consumer_name = request.form['consumer_name']
        
        # Redirect to billing page with consumer details
        return redirect(f"/billing?consumer_id={consumer_id}&consumer_name={consumer_name}")
    
    return render_template("index.html")

@app.route("/billing", methods=["GET", "POST"])
def billing():
    con = mysql.connection.cursor()

    # Get consumer details from URL parameters
    consumer_id = request.args.get('consumer_id')
    consumer_name = request.args.get('consumer_name')

    # Fetch the last billing details from the database for the given consumer_id
    con.execute("SELECT billing_date, due_date FROM elec_billing WHERE consumer_id = %s ORDER BY billing_date DESC LIMIT 1", [consumer_id])
    billing_info = con.fetchone()

    if billing_info:
        # If billing info exists, set the billing_date and due_date
        billing_date = billing_info['billing_date']
        due_date = billing_info['due_date']
    else:
        # Set default values if no previous billing information exists
        billing_date = "2024-11-01"  # Example default date
        due_date = "2024-11-15"  # Example default due date

    if request.method == "POST":
        # Retrieve form data and calculate bill_amount, due_date, etc.
        units = request.form['units']
        bill_amount = float(units) * 10  # Example calculation for bill amount

        # Insert billing into the database
        sql_insert = "INSERT INTO elec_billing (consumer_id, consumer_name, units, bill_amount, billing_date, due_date) VALUES (%s, %s, %s, %s, %s, %s)"
        con.execute(sql_insert, [consumer_id, consumer_name, units, bill_amount, billing_date, due_date])
        mysql.connection.commit()
        flash('Billing added successfully!')
        return redirect("/billing")

    # Pass consumer details and billing dates to the template
    return render_template("billing.html", consumer_id=consumer_id, consumer_name=consumer_name, billing_date=billing_date, due_date=due_date)


# Payment Page - Enter Payment Details
@app.route("/payment", methods=["GET", "POST"])
def payment():
    con = mysql.connection.cursor()
    
    if request.method == "POST":
        # Retrieve form data
        consumer_id = request.form['consumer_id']
        gpay_id = request.form['gpay_id']
        upi_id = request.form['upi_id']
        
        # Insert payment into the payments table
        sql_insert = "INSERT INTO elec_billing (consumer_id, gpay_id, upi_id) VALUES (%s, %s, %s)"
        con.execute(sql_insert, (consumer_id, gpay_id, upi_id))
        mysql.connection.commit()
        flash('Payment details added successfully!')
        return redirect("/payment")
    
    # Fetch all payments from the database
    sql_select = "SELECT * FROM elec_billing"
    con.execute(sql_select)
    payments_data = con.fetchall()
    con.close()
    return render_template("payment.html", payments=payments_data)

# Receipt Page - Receipt Details
@app.route("/receipt", methods=["GET", "POST"])
def receipt():
    con = mysql.connection.cursor()
    if request.method == "POST":
        # Retrieve form data
        consumer_id = request.form['consumer_id']
        consumer_name = request.form['consumer_name']
        units = request.form['units']
        bill_amount = request.form['bill_amount']
        billing_date = request.form['billing_date']
        due_date = request.form['due_date']
        paid = request.form['paid']
        
        # Insert receipt into the receipts table
        sql_insert = "INSERT INTO elec_billing (consumer_id, consumer_name, units, bill_amount, billing_date, due_date, paid) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        con.execute(sql_insert, (consumer_id, consumer_name, units, bill_amount, billing_date, due_date, paid))
        mysql.connection.commit()
        flash('Receipt details added successfully!')
        return redirect("/receipt")

    # Fetch all receipts from the database
    sql_select = "SELECT * FROM elec_billing"
    con.execute(sql_select)
    receipts_data = con.fetchall()
    con.close()
    return render_template("receipt.html", receipts=receipts_data)

if __name__ == "__main__":
    app.run(debug=True)
