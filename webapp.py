from flask import Flask, render_template, request
import hackbright_app

app = Flask(__name__)

@app.route("/")
def get_github():
    return render_template("get_github.html")

@app.route("/student")
def get_student():
    hackbright_app.connect_to_db()
    student_github = request.args.get("github")
    row = hackbright_app.get_student_by_github(student_github)
    student_grades = hackbright_app.get_all_grades(student_github)
    projects = hackbright_app.get_all_projects()
    return render_template("student_info.html", first_name=row[0],
                                                last_name=row[1],
                                                github=row[2],
                                                grades=student_grades,
                                                projects = projects)

@app.route("/project_grades")
def get_project_grades():
    hackbright_app.connect_to_db()
    project = request.args.get("project")
    rows = hackbright_app.get_all_students(project)
    return render_template("project_grades.html", project_name = project,
                                            row = rows)

@app.route("/new_student")
def new_student():
    return render_template("new_student.html")

@app.route("/view_student")
def view_new_student():
    hackbright_app.connect_to_db()
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    github = request.args.get("github")
    hackbright_app.make_new_student(first_name, last_name, github)
    return render_template("view_student.html", first = first_name,
                                                last = last_name,
                                                github = github)

@app.route("/new_project")
def new_project():
    return render_template("new_project.html")

@app.route("/view_project")
def view_new_project():
    hackbright_app.connect_to_db()
    title = request.args.get("title")
    description = request.args.get("desc")
    max_grade = request.args.get("max")
    hackbright_app.make_new_project(title, max_grade, description)
    return render_template("view_project.html", title = title,
                                                desc = description,
                                                max = max_grade)

@app.route("/new_grade")
def new_grade():
    return render_template("new_grade.html")

@app.route("/view_grade")
def view_new_grade():
    hackbright_app.connect_to_db()
    student = request.args.get("student")
    title = request.args.get("title")
    grade = request.args.get("grade")
    hackbright_app.give_student_grade(student, title, grade)
    return render_template("view_grade.html", student = student,
                                                title = title,
                                                grade = grade)

if __name__ == "__main__":
    app.run(debug=True)