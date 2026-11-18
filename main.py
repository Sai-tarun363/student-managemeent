
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
import sqlite3

app = FastAPI()

templates = Jinja2Templates(directory="templates")


# STUDENT MODEL
class student(BaseModel):
    name: str
    age: int
    gender: str
    marks: int
    course: str
    status: int


# DATABASE CONNECTION
def get_connection():
    connection = sqlite3.connect("student.db")
    return connection


# CREATE TABLE
def create_table():
    connection = get_connection()
    cursor = connection.cursor()

    q = """
    CREATE TABLE IF NOT EXISTS STUDENT (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        NAME TEXT NOT NULL,
        AGE INTEGER,
        GENDER TEXT,
        MARKS INTEGER,
        COURSE TEXT,
        STATUS INTEGER
    )
    """

    cursor.execute(q)
    connection.commit()
    connection.close()


create_table()


# HOME - DISPLAY ALL STUDENTS
@app.get("/")
def home(req: Request):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM STUDENT ORDER BY ID DESC")
    students = cursor.fetchall()

    connection.close()

    return templates.TemplateResponse(
        request=req,
        name="home.html",
        context={"students": students}
    )


# ADD - SHOW STUDENT FORM
@app.get("/student/add")
def send_std_data(req: Request):

    return templates.TemplateResponse(
        request=req,
        name="add-student.html",
        context={}
    )


# ADD - INSERT STUDENT
@app.post("/student/add")
def create_std(
    name: str = Form(...),
    age: int = Form(...),
    course: str = Form(...),
    gender: str = Form(...),
    marks: int = Form(...),
    status: int = Form(...)
):

    std = student(
        name=name,
        age=age,
        course=course,
        gender=gender,
        marks=marks,
        status=status
    )

    values = (
        std.name,
        std.age,
        std.gender,
        std.marks,
        std.course,
        std.status
    )

    connection = get_connection()
    cursor = connection.cursor()

    q = """
    INSERT INTO STUDENT
    (NAME, AGE, GENDER, MARKS, COURSE, STATUS)
    VALUES (?, ?, ?, ?, ?, ?)
    """

    cursor.execute(q, values)

    connection.commit()
    connection.close()

    return RedirectResponse(url="/", status_code=303)


# VIEW - SINGLE STUDENT
@app.get("/student/{std_id}")
def single_std(req: Request, std_id: int):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM STUDENT WHERE ID = ?",
        (std_id,)
    )

    std = cursor.fetchone()
    connection.close()

    if std is None:
        return RedirectResponse(url="/", status_code=303)

    return templates.TemplateResponse(
        request=req,
        name="single_std.html",
        context={"std": std}
    )


# UPDATE - SHOW EXISTING DETAILS
@app.get("/student/update/{std_id}")
def update_std_form(req: Request, std_id: int):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM STUDENT WHERE ID = ?",
        (std_id,)
    )

    std = cursor.fetchone()
    connection.close()

    if std is None:
        return RedirectResponse(url="/", status_code=303)

    return templates.TemplateResponse(
        request=req,
        name="update_student.html",
        context={"std": std}
    )


# UPDATE - SAVE STUDENT DETAILS
@app.post("/student/update/{std_id}")
def update_std(
    std_id: int,
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    marks: int = Form(...),
    course: str = Form(...),
    status: int = Form(...)
):

    connection = get_connection()
    cursor = connection.cursor()

    q = """
    UPDATE STUDENT
    SET NAME = ?,
        AGE = ?,
        GENDER = ?,
        MARKS = ?,
        COURSE = ?,
        STATUS = ?
    WHERE ID = ?
    """

    values = (
        name, age, gender, marks,
        course, status, std_id
    )

    cursor.execute(q, values)

    connection.commit()
    connection.close()

    return RedirectResponse(url="/", status_code=303)


# DELETE - REMOVE STUDENT
@app.post("/student/delete/{std_id}")
def delete_std(std_id: int):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM STUDENT WHERE ID = ?",
        (std_id,)
    )

    connection.commit()
    connection.close()

    return RedirectResponse(url="/", status_code=303)
