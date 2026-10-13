from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "employees.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            department TEXT NOT NULL,
            position TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = get_db_connection()

    employees = conn.execute(
        "SELECT * FROM employees ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template("index.html", employees=employees)


@app.route("/add", methods=["GET", "POST"])
def add_employee():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        department = request.form["department"]
        position = request.form["position"]

        conn = get_db_connection()

        conn.execute("""
            INSERT INTO employees
            (name, email, department, position)
            VALUES (?, ?, ?, ?)
        """, (name, email, department, position))

        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    return render_template("add_employee.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_employee(id):

    conn = get_db_connection()

    employee = conn.execute(
        "SELECT * FROM employees WHERE id = ?",
        (id,)
    ).fetchone()

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        department = request.form["department"]
        position = request.form["position"]

        conn.execute("""
            UPDATE employees
            SET name = ?, email = ?, department = ?, position = ?
            WHERE id = ?
        """, (name, email, department, position, id))

        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    conn.close()

    return render_template(
        "edit_employee.html",
        employee=employee
    )


@app.route("/delete/<int:id>")
def delete_employee(id):

    conn = get_db_connection()

    conn.execute(
        "DELETE FROM employees WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("index"))


if __name__ == "__main__":

    init_db()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )