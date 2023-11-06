"""Code for a flask API2 to Create, Read, Update, Delete different units linked to users"""
import os
from flask import jsonify, request, Flask
from flaskext.mysql import MySQL

app = Flask2(__name__)

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
            resp = jsonify("User created successfully!")
            resp.status_code = 200
            return resp
        except Exception as exception:
            return jsonify(str(exception))
    else:
        return jsonify("Please provide name, grade and department")


@app.route("/unit", methods=["GET"])
def unit():
    """Function to retrieve all users from the MySQL database"""
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


@app.route("/unit/<int:grade>", methods=["GET"])
def unit(grade):
    """Function to get information of a specific user in the MSQL database"""
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM unit WHERE grade=%s", grade)
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as exception:
        return jsonify(str(exception))


@app.route("/update", methods=["POST"])
def update_grade():
    """Function to update a user in the MYSQL database"""
    json = request.json
    name = json["name"]
    grade = json["grade"]
    department = json["department"]
    user_id = json["user_id"]
    if name and grade and department and user_id and request.method == "POST":
        # save edits
        sql = "UPDATE unit SET user_name=%s, user_grade=%s, " \
              "user_department=%s WHERE user_id=%s"
        data = (name, grade, department, user_id)
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify("Unit updated successfully!")
            resp.status_code = 200
            cursor.close()
            conn.close()
            return resp
        except Exception as exception:
            return jsonify(str(exception))
    else:
        return jsonify("Please provide id, name, grade and department")


@app.route("/delete/<int:grade>")
def delete_user(grade):
    """Function to delete a user from the MySQL database"""
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM unit WHERE grade=%s", grade)
        conn.commit()
        cursor.close()
        conn.close()
        resp = jsonify("User deleted successfully!")
        resp.status_code = 200
        return resp
    except Exception as exception:
        return jsonify(str(exception))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)
