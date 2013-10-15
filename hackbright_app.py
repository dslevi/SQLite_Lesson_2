import sqlite3

DB = None
CONN = None

def get_all_projects():
    query = """SELECT title FROM Projects"""
    DB.execute(query)
    return DB.fetchall()

def make_new_student(first_name, last_name, github):
    query = """INSERT INTO Students VALUES (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()

def make_new_project(title, max_grade, description):
    query = """INSERT INTO Projects VALUES (?, ?, ?)"""
    DB.execute(query, (title, description, max_grade))

    CONN.commit()
    print "Successfully added project: %s" % (title)

def get_student_by_github(github):
    print github
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    return row

def get_project_title(title):
    query = """SELECT * FROM Projects WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    print """\
Title: %s
Description: %s
Max Grade: %s""" % (row[0], row[1], row[2])

def get_all_students(project):
    query = """SELECT Students.first_name, Students.last_name, github, grade FROM ReportCardView INNER JOIN Students ON (Students.first_name = ReportCardView.first_name) WHERE title = ?"""
    DB.execute(query, (project, ))
    row = DB.fetchall()
    return row

def get_project_grade(student, project):
    query = """SELECT * FROM Grades WHERE student_github = ? AND project_title = ?"""
    DB.execute(query, (student, project,))
    row = DB.fetchone()
    return row

def give_student_grade(student, title, grade):
    query = """SELECT * FROM Grades WHERE student_github = ? AND project_title = ?"""
    DB.execute(query, (student, title,))
    row = DB.fetchone()
    if row == None:
        query = """INSERT INTO Grades VALUES (?, ?, ?)"""
        DB.execute(query, (student, title, grade))
        CONN.commit()
        print "Successfully added grade to: %s" % (grade)

def get_all_grades(student):
    query = """SELECT project_title, grade FROM Grades WHERE student_github = ?"""
    DB.execute(query, (student,))
    projects_grades = DB.fetchall()
    pg_list = []
    for x in projects_grades:
       pg_list.append(x[0])
       pg_list.append(x[1])
    return pg_list

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "project_title":
            get_project_title(*args)
        elif command == "new_project":
            description = " ".join(args[2:])
            make_new_project(args[0], args[1], description)
        elif command == "project_grade":
            get_project_grade(args[0], args[1])
        elif command == "give_grade":
            give_student_grade(*args)
        elif command == "show_grades":
            get_all_grades(*args)

    CONN.close()

if __name__ == "__main__":
    main()
