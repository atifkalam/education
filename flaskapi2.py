"""Code for a flask API2 to Create, Read, Update, Delete different units linked to users"""
import os
from flask import jsonify, request, Flask
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = os.getenv("db_root_password")
app.config["MYSQL_DATABASE_DB"] = os.getenv("db_name")
app.config["MYSQL_DATABASE_HOST"] = os.getenv("MYSQL_SERVICE_HOST")
app.config["MYSQL_DATABASE_PORT"] = int(os.getenv("MYSQL_SERVICE_PORT"))
mysql.init_app(app)


@app.route("/")
def index():
    """Function to test the functionality of the API"""
    return "API-2 initialized Sucessfully with Unit details"


@app.route("/create", methods=["POST"])
def add_user():
    """Function to create a unit to the MySQL database"""
    json = request.json
    name = json["name"]
    grade = json["grade"]
    department = json["department"]
    if name and grade and department and request.method == "POST":
        sql = "INSERT INTO unit(user_name, user_grade, user_department) " \
              "VALUES(%s, %s, %s)"
        data = (name, grade, department)
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            cursor.close()
            conn.close()
            resp = jsonify("Department created successfully!")
            resp.status_code = 200
            return resp
        except Exception as exception:
            return jsonify(str(exception))
    else:
        return jsonify("Please provide name, grade and department")


@app.route("/unit", methods=["GET"])
def unit():
    """Function to retrieve all units from the MySQL database"""
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM unit")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as exception:
        return jsonify(str(exception))


@app.route("/unit/<int:user_name>", methods=["GET"])
def unit(user_name):
    """Function to get information of a specific user in the MSQL database"""
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM unit WHERE user_name=%s", user_name)
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as exception:
        return jsonify(str(exception))


@app.route("/delete/<int:user_name>")
def delete_user(user_name):
    """Function to delete a user from the MySQL database"""
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM unit WHERE user_name=%s", user_name)
        conn.commit()
        cursor.close()
        conn.close()
        resp = jsonify("Department deleted successfully!")
        resp.status_code = 200
        return resp
    except Exception as exception:
        return jsonify(str(exception))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)
