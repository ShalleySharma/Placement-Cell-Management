import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import *
import datetime
import mysql.connector as connector

mycon = connector.connect(
    host='localhost',
    user='Khushi',
    passwd='kritika#2009',
    database='PLACEMENT',
    charset='utf8'
)
cursor = mycon.cursor()
mycon.autocommit = True

# t = "CREATE TABLE Students (Students_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50),s_password VARCHAR(10), date_of_birth DATE, email VARCHAR(100), phone_number VARCHAR(10), department VARCHAR(10), Year INT, cgpa DECIMAL(3, 2), backlogs INT)"
# cursor.execute(t)

# t = "create table Administrators(admin_id int(20) primary key, name varchar(50), a_password VARCHAR(10), email varchar(100),phone_number int, department varchar(20))"
# cursor.execute(t)

# t = "CREATE TABLE Recruiters (recruiter_id INT PRIMARY KEY, name VARCHAR(50), r_password VARCHAR(10), company_name VARCHAR(50), email VARCHAR(100), phone_number VARCHAR(10))"
# cursor.execute(t)

# t = "CREATE TABLE Jobs (job_id INT PRIMARY KEY, job_title VARCHAR(50), job_description TEXT, job_category VARCHAR(20) , last_date_to DATE, recruiter_id INT, Students_id INT, FOREIGN KEY (recruiter_id) REFERENCES recruiters(recruiter_id), FOREIGN KEY (Students_id) REFERENCES Students(Students_id))"
# cursor.execute(t)

# t = "CREATE TABLE Applications (application_id INT PRIMARY KEY, Students_id INT, job_id INT, resume_url VARCHAR(255), status VARCHAR(20), FOREIGN KEY (Students_id) REFERENCES Students(Students_id), FOREIGN KEY (job_id) REFERENCES Jobs(job_id))"
# cursor.execute(t)

# t = "CREATE TABLE interviews (interview_id INT PRIMARY KEY, job_id INT, recruiter_id INT, interview_date DATE, result VARCHAR(50), FOREIGN KEY (job_id) REFERENCES jobs(job_id), FOREIGN KEY (recruiter_id) REFERENCES recruiters(recruiter_id))"
# cursor.execute(t)


def make_scrollable(root, width=1600, height=800):  # Set default width and height
    canvas = Canvas(root, width=width, height=height)  # Set canvas size
    scrollbar = Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, width=width, height=height)  # Set frame size

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    return scrollable_frame


class PlacementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Placement Cell Management System")
        self.geometry("1600x800")
        self.configure(background="lightgrey")  # Set background color for the entire window
        self.main_frame = tk.Frame(self, bg="lightgrey")  # Set background color for the main frame
        self.main_frame.pack(fill="both", expand=True)
        self.scrollable_frame = make_scrollable(self.main_frame, width=1600, height=800)  # Create a scrollable frame
        self.menu()

    def menu(self):
        self.clear_frame()
        scrollable_frame = make_scrollable(self.main_frame, width=1600, height=800)

        Label(scrollable_frame, text="WELCOME TO PLACEMENT CELL MANAGEMENT SYSTEM", font=('Helvetica', 14), bg="lightblue").pack(pady=20)
        Button(scrollable_frame, text="STUDENT", command=self.s_main, font=('Helvetica', 12), bg="lightblue").pack(pady=20)
        Button(scrollable_frame, text="ADMINISTRATOR", command=self.a_main, font=('Helvetica', 12), bg="lightblue").pack(pady=20)
        Button(scrollable_frame, text="RECRUITER", command=self.r_main, font=('Helvetica', 12), bg="lightblue").pack(pady=20)
        Button(scrollable_frame, text="EXIT", command=self.quit, font=('Helvetica', 12), bg="lightblue").pack(pady=20)

    def s_main(self):
        self.clear_frame()
        scrollable_frame = make_scrollable(self.main_frame, width=1600, height=800)

        Label(scrollable_frame, text="WELCOME TO Student Login", font=('Helvetica', 14), bg="lightblue").pack(pady=20)
        Button(scrollable_frame, text="SIGN IN", command=self.student_signin, font=('Helvetica', 12), bg="lightblue").pack(pady=10)
        Button(scrollable_frame, text="SIGN UP", command=self.student_signup, font=('Helvetica', 12), bg="lightblue").pack(pady=10)
        Button(scrollable_frame, text="MODIFY ACCOUNT", command=self.student_account, font=('Helvetica', 12), bg="lightblue").pack(pady=10)
        Button(scrollable_frame, text="BACK", command=self.menu, font=('Helvetica', 12), bg="lightblue").pack(pady=10)

    def student_signin(self):
        self.clear_frame()
        signin_frame = make_scrollable(self.main_frame, width=1600, height=800)

        Label(signin_frame, text="STUDENT SIGN IN", font=('Helvetica', 14), bg="lightblue").pack(pady=20)
        Label(signin_frame, text="USER NAME:", bg="lightblue").pack(pady=5)
        user_name = Entry(signin_frame)
        user_name.pack(pady=5)

        Label(signin_frame, text="PASSWORD:", bg="lightblue").pack(pady=5)
        password = Entry(signin_frame, show='*')
        password.pack(pady=5)

        def check_student_signin():
            a = user_name.get()
            b = password.get()
            try:
                query = "SELECT students_id, name FROM Students WHERE name=%s AND s_password=%s"
                cursor.execute(query, (a, b))
                data = cursor.fetchone()
                if data and data[1] == a:
                    messagebox.showinfo("Success", "Welcome " + data[1])
                    self.student(data[0])  # Pass the students_id to the student method
                else:
                    messagebox.showerror("Error", "Invalid Credentials")
            except Exception as e:
                messagebox.showerror("Error", "Account does not exist")

        Button(signin_frame, text="Sign In", command=check_student_signin, bg="lightblue").pack(pady=10)
        Button(signin_frame, text="BACK", command=self.s_main, bg="lightblue").pack(pady=10)

    def student_signup(self):
        self.clear_frame()
        signup_frame = make_scrollable(self.main_frame)

        Label(signup_frame, text="STUDENT SIGN UP", font=('Helvetica', 14), bg="lightblue").pack(pady=20)
        labels = [
            "STUDENT ID", "STUDENT NAME", "PASSWORD", "RE-ENTER YOUR PASSWORD",
            "MAIL ID", "PHONE NUMBER", "DEPARTMENT",
            "YEAR", "CGPA", "NUMBER OF BACKLOGS"
        ]
        self.student_entries = {}

        for label in labels:
            Label(signup_frame, text=label, bg="lightblue").pack(pady=5)
            entry = Entry(signup_frame)
            entry.pack(pady=5)
            self.student_entries[label] = entry

        # Separate entries for date of birth
        Label(signup_frame, text="DATE OF BIRTH", bg="lightblue").pack(pady=5)
        dob_frame = Frame(signup_frame)
        dob_frame.pack(pady=5)

        Label(dob_frame, text="Day", bg="lightblue").pack(side=LEFT, padx=5)
        day_entry = Entry(dob_frame, width=3)
        day_entry.pack(side=LEFT, padx=5)

        Label(dob_frame, text="Month", bg="lightblue").pack(side=LEFT, padx=5)
        month_entry = Entry(dob_frame, width=3)
        month_entry.pack(side=LEFT, padx=5)

        Label(dob_frame, text="Year", bg="lightblue").pack(side=LEFT, padx=5)
        year_entry = Entry(dob_frame, width=5)
        year_entry.pack(side=LEFT, padx=5)

        def check_student_signup():
            student_data = {
                'students_id': self.student_entries["STUDENT ID"].get(),
                'name': self.student_entries["STUDENT NAME"].get(),
                'password': self.student_entries["PASSWORD"].get(),
                'date_of_birth': f"{year_entry.get()}-{month_entry.get()}-{day_entry.get()}",
                'mail_id': self.student_entries["MAIL ID"].get(),
                'phone_number': self.student_entries["PHONE NUMBER"].get(),
                'department': self.student_entries["DEPARTMENT"].get(),
                'year': self.student_entries["YEAR"].get(),
                'cgpa': self.student_entries["CGPA"].get(),
                'backlogs': self.student_entries["NUMBER OF BACKLOGS"].get()
            }
            re_password = self.student_entries["RE-ENTER YOUR PASSWORD"].get()
        
            if student_data['password'] == re_password:
                try:
                    query = '''INSERT INTO Students 
                            (students_id, name, s_password, date_of_birth, email, phone_number, department, year, cgpa, backlogs) 
                            VALUES (%(students_id)s, %(name)s, %(password)s, %(date_of_birth)s, %(mail_id)s, %(phone_number)s, 
                                %(department)s, %(year)s, %(cgpa)s, %(backlogs)s)'''
                    cursor.execute(query, student_data)
                    mycon.commit()
                    messagebox.showinfo("Success", "Account created successfully")
                    self.student(student_data['students_id'])  # Pass the students_id to the student method
                except connector.Error as err:
                    messagebox.showerror("Error", f"Error: {err}")
            else:
                messagebox.showerror("Error", "Passwords do not match")

        Button(signup_frame, text="Sign Up", command=check_student_signup, bg="lightblue").pack(pady=10)
        Button(signup_frame, text="BACK", command=self.s_main, bg="lightblue").pack(pady=10)

    def student_account(self):
        self.clear_frame()
        account_frame = make_scrollable(self.main_frame)

        Label(account_frame, text="STUDENT ACCOUNT DETAILS", font=('Helvetica', 14), bg="lightblue").pack(pady=20)
        Label(account_frame, text="USER NAME:", bg="lightblue").pack(pady=5)
        user_name = Entry(account_frame)
        user_name.pack(pady=5)

        Label(account_frame, text="PASSWORD:", bg="lightblue").pack(pady=5)
        password = Entry(account_frame, show='*')
        password.pack(pady=5)

        def check_student_account():
            a = user_name.get()
            b = password.get()
            try:
                query = "SELECT name FROM Students WHERE s_password=%s"
                cursor.execute(query, (b,))
                data = cursor.fetchone()
                if data and data[0] == a:
                    x = ['STUDENT ID', 'NAME', 'PASSWORD', 'DATE OF BIRTH', 'MAIL ID', 'PHONE NUMBER', 'DEPARTMENT', 'YEAR', 'CGPA', 'BACKLOGS']
                    query = "SELECT * FROM Students WHERE s_password=%s"
                    cursor.execute(query, (b,))
                    student_data = cursor.fetchone()

                    details_win = Toplevel(account_frame)
                    details_win.title("Student Account Details")
                    details_win.geometry("400x400")

                    for i in range(len(x)):
                        Label(details_win, text=f"{x[i]} ::: {student_data[i]}").pack(pady=5)
                else:
                    messagebox.showerror("Error", "Account does not exist")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        Button(account_frame, text="Check Account", command=check_student_account, bg="lightblue").pack(pady=10)
        Button(account_frame, text="BACK", command=self.s_main, bg="lightblue").pack(pady=10)

    def student(self, students_id):
        self.clear_frame()
        scrollable_frame = make_scrollable(self.main_frame)

        Label(scrollable_frame, text="STUDENT MAIN MENU", font=('Helvetica', 14), bg="lightblue").pack(pady=20)
        Button(scrollable_frame, text="SEARCH JOBS", command=lambda: self.jobs(students_id), font=('Helvetica', 12), bg="lightblue").pack(pady=10)
        Button(scrollable_frame, text="APPLY FOR JOBS", command=lambda: self.apply_for_jobs(students_id), font=('Helvetica', 12), bg="lightblue").pack(pady=10)
        Button(scrollable_frame, text="MODIFY APPLICATION", command=lambda: self.modify_application(students_id), font=('Helvetica', 12), bg="lightblue").pack(pady=10)
        Button(scrollable_frame, text="SHOW STATUS OF THE APPLICATION", command=lambda: self.status(students_id), font=('Helvetica', 12), bg="lightblue").pack(pady=10)
        Button(scrollable_frame, text="SHOW INTERVIEW DETAILS", command=lambda: self.interview(students_id), font=('Helvetica', 12), bg="lightblue").pack(pady=10)
        Button(scrollable_frame, text="BACK", command=self.s_main, font=('Helvetica', 12), bg="lightblue").pack(pady=10)

    def jobs(self, students_id):
        self.clear_frame()
        job_frame = make_scrollable(self.main_frame)

        try:
            c1 = "SELECT * FROM Jobs"
            cursor.execute(c1)
            data = cursor.fetchall()

            if data:
                Label(job_frame, text="Available Jobs", font=('Helvetica', 14, 'bold'), bg="lightblue").pack(pady=10)

                for job in data:
                    Label(job_frame, text=f"Job ID: {job[0]}", font=('Helvetica', 12)).pack(anchor=W)
                    Label(job_frame, text=f"Job Title: {job[1]}", font=('Helvetica', 12)).pack(anchor=W)
                    Label(job_frame, text=f"Job Description: {job[2]}", font=('Helvetica', 12)).pack(anchor=W)
                    Label(job_frame, text=f"Job Category: {job[3]}", font=('Helvetica', 12)).pack(anchor=W)
                    Label(job_frame, text=f"Last Date to Apply: {job[4]}", font=('Helvetica', 12)).pack(anchor=W)
                    Label(job_frame, text=f"Recruiter ID: {job[5]}", font=('Helvetica', 12)).pack(anchor=W)
                    Label(job_frame, text='-----------------------------------', font=('Helvetica', 12)).pack(anchor=W)
            else:
                Label(job_frame, text="No jobs available at the moment.", font=('Helvetica', 12)).pack(pady=10)

        except Exception as e:
            Label(job_frame, text=f"Error: {e}", font=('Helvetica', 12)).pack(pady=10)

        Button(job_frame, text="BACK", command=lambda: self.student(students_id)).pack(pady=10)

    def modify_application(self, students_id):
        self.clear_frame()
        modify_app_window = make_scrollable(self.main_frame)

        Label(modify_app_window, text="Enter Application ID:", bg="lightblue").pack(pady=5)
        app_id_entry = Entry(modify_app_window)
        app_id_entry.pack(pady=5)

        new_resume_url_label = Label(modify_app_window, text="New Resume URL:", bg="lightblue")
        new_resume_url_label.pack(pady=5)
        new_resume_url_entry = Entry(modify_app_window)
        new_resume_url_entry.pack(pady=5)

        def modify_application():
            try:
                application_id = int(app_id_entry.get())
                query = "SELECT job_id, resume_url, status FROM Applications WHERE application_id = %s"
                cursor.execute(query, (application_id,))
                application_details = cursor.fetchone()

                if not application_details:
                    messagebox.showerror("Error", "Invalid Application ID.")
                    return

                new_resume_url = new_resume_url_entry.get()
                query = "UPDATE Applications SET resume_url = %s WHERE application_id = %s"
                cursor.execute(query, (new_resume_url, application_id))
                mycon.commit()
                messagebox.showinfo("Success", "Resume URL updated successfully.")

            except Exception as e:
                messagebox.showerror("Error", str(e))

        Button(modify_app_window, text="MODIFY APPLICATION", command=modify_application, font=('Helvetica', 16), bg="lightblue").pack(pady=20)
        Button(modify_app_window, text="BACK", command=lambda: self.student(students_id), bg="lightblue").pack(pady=10)

    def status(self, students_id):
        self.clear_frame()
        status_frame = make_scrollable(self.main_frame)

        Label(status_frame, text="Enter Application ID:", bg="lightblue").pack(pady=5)
        status_entry = Entry(status_frame)
        status_entry.pack(pady=5)

        def show_status():
            application_id = int(status_entry.get())
            try:
                query = "SELECT a.job_id, j.job_title, a.status FROM Applications a JOIN Jobs j ON a.job_id = j.job_id WHERE a.application_id = %s AND a.Students_id = %s"
                cursor.execute(query, (application_id, students_id))
                applications = cursor.fetchall()

                if applications:
                    Label(status_frame, text="Status of Your Applications:", font=('Helvetica', 14, 'bold'), bg="lightblue").pack(pady=10)

                    for job in applications:
                        Label(status_frame, text=f"Application ID: {job[0]}", font=('Helvetica', 12)).pack(anchor=W)
                        Label(status_frame, text=f"Job ID: {job[0]}", font=('Helvetica', 12)).pack(anchor=W)
                        Label(status_frame, text=f"Job Title: {job[1]}", font=('Helvetica', 12)).pack(anchor=W)
                        Label(status_frame, text=f"Status: {job[2]}", font=('Helvetica', 12)).pack(anchor=W)

                else:
                    Label(status_frame, text="You haven't applied for any jobs yet.", font=('Helvetica', 12), bg="lightblue").pack(pady=10)

            except Exception as e:
                Label(status_frame, text=f"An error occurred while fetching application status: {e}", font=('Helvetica', 12), bg="lightblue").pack(pady=10)

        Button(status_frame, text="SHOW STATUS OF THE APPLICATION", command=show_status, font=('Helvetica', 16), bg="lightblue").pack(pady=20)
        Button(status_frame, text="BACK", command=lambda: self.student(students_id)).pack(pady=10)

    def apply_for_jobs(self, students_id):
        self.clear_frame()
        apply_frame = make_scrollable(self.main_frame)

        Label(apply_frame, text="Enter Job ID:", bg="lightblue").pack(pady=5)
        job_id_entry = Entry(apply_frame)
        job_id_entry.pack(pady=5)

        Label(apply_frame, text="Resume URL:", bg="lightblue").pack(pady=5)
        resume_url_entry = Entry(apply_frame)
        resume_url_entry.pack(pady=5)

        def submit_application():
            try:
                job_id = int(job_id_entry.get())
                resume_url = resume_url_entry.get()

                query = "SELECT last_date_to FROM Jobs WHERE job_id = %s"
                cursor.execute(query, (job_id,))
                result = cursor.fetchone()
                if result is None:
                    messagebox.showinfo("Error", "No job found with the given Job ID.")
                    return

                last_date = result[0]
                current_date = datetime.datetime.now().date()
                if current_date > last_date:
                    messagebox.showinfo("Error", "Applications for this job have been closed.")
                    return

                status = 'Pending'  # Set initial status as Pending
                query = "INSERT INTO Applications (Students_id, job_id, resume_url, status) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (students_id, job_id, resume_url, status))
                mycon.commit()
                messagebox.showinfo("Success", "Application submitted successfully!")
                apply_frame.destroy()  # Close the apply window after successful submission
            except Exception as e:
                messagebox.showerror("Error", str(e))

        Button(apply_frame, text="Submit", command=submit_application, bg="lightblue").pack(pady=10)
        Button(apply_frame, text="BACK", command=lambda: self.student(students_id), bg="lightblue").pack(pady=10)


    def interview(self, students_id):
        self.clear_frame()
        scrollable_frame = make_scrollable(self.main_frame)

        interview_frame = Frame(scrollable_frame)
        interview_frame.pack(fill=BOTH, expand=TRUE)

        try:
            query = "SELECT * FROM interviews WHERE Students_id = %s"
            cursor.execute(query, (students_id,))
            interviews = cursor.fetchall()

            if interviews:
                Label(interview_frame, text="Interview Details", font=('Helvetica', 14, 'bold'), bg="lightblue").pack(pady=10)

                for job in interviews:
                    Label(interview_frame, text=f"Interview ID: {job[0]}", font=('Helvetica', 12)).pack(anchor=W)
                    Label(interview_frame, text=f"Job ID: {job[1]}", font=('Helvetica', 12)).pack(anchor=W)
                    Label(interview_frame, text=f"Recruiter ID: {job[2]}", font=('Helvetica', 12)).pack(anchor=W)
                    Label(interview_frame, text=f"Interview Date: {job[3]}", font=('Helvetica', 12)).pack(anchor=W)
                    Label(interview_frame, text=f"Result: {job[4]}", font=('Helvetica', 12)).pack(anchor=W)

            else:
                Label(interview_frame, text="You don't have any interview scheduled.", font=('Helvetica', 12), bg="lightblue").pack(pady=10)

        except Exception as e:
            Label(interview_frame, text=f"An error occurred while fetching interview details: {e}", font=('Helvetica', 12), bg="lightblue").pack(pady=10)

        Button(interview_frame, text="BACK", command=lambda: self.student(students_id), bg="lightblue").pack(pady=10)
        
    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def a_main(self):
        self.clear_frame()
        scrollable_frame = make_scrollable(self.main_frame)
        Label(scrollable_frame, text="ADMINISTRATOR MENU", font=('Helvetica', 14), bg="lightblue").pack(pady=20)
        Button(scrollable_frame, text="ADMIN LOGIN", command=self.admin_login, font=('Helvetica', 12), bg="lightblue").pack(pady=10)
        Button(scrollable_frame, text="BACK", command=self.menu, font=('Helvetica', 12), bg="lightblue").pack(pady=10)

    def admin_login(self):
        self.clear_frame()
        login_frame = make_scrollable(self.main_frame)
        Label(login_frame, text="ADMIN LOGIN", font=('Helvetica', 14), bg="lightblue").pack(pady=20)

        Label(login_frame, text="ADMIN ID:", bg="lightblue").pack(pady=5)
        admin_id_entry = Entry(login_frame)
        admin_id_entry.pack(pady=5)

        Label(login_frame, text="PASSWORD:", bg="lightblue").pack(pady=5)
        admin_password_entry = Entry(login_frame, show='*')
        admin_password_entry.pack(pady=5)

        def check_admin_login():
            admin_id = admin_id_entry.get()
            admin_password = admin_password_entry.get()
            try:
                query = "SELECT name FROM administrators WHERE admin_id=%s AND a_password=%s"
                cursor.execute(query, (admin_id, admin_password))
                data = cursor.fetchone()
                if data:
                    messagebox.showinfo("Success", "Welcome " + data[0])
                    self.admin()
                else:
                    messagebox.showerror("Error", "Invalid Credentials")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        Button(login_frame, text="Login", command=check_admin_login, bg="lightblue").pack(pady=10)
        Button(login_frame, text="BACK", command=self.a_main, bg="lightblue").pack(pady=10)

    def admin(self):
        self.clear_frame()
        scrollable_frame = make_scrollable(self.main_frame)
        Label(scrollable_frame, text="ADMIN MAIN MENU", font=('Helvetica', 14), bg="lightblue").pack(pady=20)
        Button(scrollable_frame, text="ADD JOB", command=self.add_job, font=('Helvetica', 12), bg="lightblue").pack(pady=10)
        Button(scrollable_frame, text="MODIFY JOB", command=self.modify_job, font=('Helvetica', 12), bg="lightblue").pack(pady=10)
        Button(scrollable_frame, text="BACK", command=self.a_main, font=('Helvetica', 12), bg="lightblue").pack(pady=10)

    def add_job(self):
        self.clear_frame()
        job_frame = make_scrollable(self.main_frame)
        Label(job_frame, text="ADD JOB", font=('Helvetica', 14), bg="lightblue").pack(pady=20)

        labels = ["job_id", "job_title", "job_description", "job_category", "last_date_to", "recruiter_id", "students_id"]
        self.job_entries = {}

        for label in labels:
            Label(job_frame, text=label.upper(), bg="lightblue").pack(pady=5)
            entry = Entry(job_frame)
            entry.pack(pady=5)
            self.job_entries[label] = entry

        def save_job():
            job_data = {
                'job_id': self.job_entries["job_id"].get(),
                'job_title': self.job_entries["job_title"].get(),
                'job_description': self.job_entries["job_description"].get(),
                'job_category': self.job_entries["job_category"].get(),
                'last_date_to': self.job_entries["last_date_to"].get(),
                'recruiter_id': self.job_entries["recruiter_id"].get(),
                'students_id': self.job_entries["students_id"].get(),
            }
            try:
                # Assuming cursor and mycon are already defined and available in this scope
                query = '''INSERT INTO Jobs (`job_id`, `job_title`, `job_description`, `job_category`, `last_date_to`, `recruiter_id`, `students_id`) 
                        VALUES (%(job_id)s, %(job_title)s, %(job_description)s, %(job_category)s, %(last_date_to)s, %(recruiter_id)s, %(students_id)s )'''
                cursor.execute(query, job_data)
                mycon.commit()
                messagebox.showinfo("Success", "Job added successfully")
                self.admin()
            except connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")

        Button(job_frame, text="Save Job", command=save_job, bg="lightblue").pack(pady=10)
        Button(job_frame, text="BACK", command=self.admin, bg="lightblue").pack(pady=10)


    def modify_job(self):
        self.clear_frame()
        modify_frame = make_scrollable(self.main_frame)
        Label(modify_frame, text="MODIFY JOB", font=('Helvetica', 14), bg="lightblue").pack(pady=20)

        Label(modify_frame, text="ENTER JOB ID:", bg="lightblue").pack(pady=5)
        job_id_entry = Entry(modify_frame)
        job_id_entry.pack(pady=5)

        labels = ["JOB TITLE", "JOB DESCRIPTION", "JOB CATEGORY", "LAST DATE TO", "RECRUITER ID", "STUDENTS ID"]
        self.modify_entries = {}

        for label in labels:
            Label(modify_frame, text=label, bg="lightblue").pack(pady=5)
            entry = Entry(modify_frame)
            entry.pack(pady=5)
            self.modify_entries[label] = entry

        def update_job():
            job_id = job_id_entry.get()
            job_data = {
                'job_title': self.modify_entries["JOB TITLE"].get(),
                'job_description': self.modify_entries["JOB DESCRIPTION"].get(),
                'job_category': self.modify_entries["JOB CATEGORY"].get(),
                'last_date_to': self.modify_entries["LAST DATE TO"].get(),
                'recruiter_id': self.modify_entries["RECRUITER ID"].get(),
                'students_id': self.modify_entries["STUDENTS ID"].get(),
            }
            try:
                query = '''UPDATE Jobs 
                        SET job_title=%(job_title)s, 
                            job_description=%(job_description)s, 
                            job_category=%(job_category)s, 
                            last_date_to=%(last_date_to)s, 
                            recruiter_id=%(recruiter_id)s, 
                            students_id=%(students_id)s 
                        WHERE job_id=%(job_id)s'''
                cursor.execute(query, {**job_data, 'job_id': job_id})
                mycon.commit()
                messagebox.showinfo("Success", "Job updated successfully")
                self.admin()
            except connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")

        Button(modify_frame, text="Update Job", command=update_job, bg="lightblue").pack(pady=10)
        Button(modify_frame, text="BACK", command=self.admin, bg="lightblue").pack(pady=10)


    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # Recruiter methods
    def r_main(self):
        self.clear_frame()
        scrollable_frame = make_scrollable(self.main_frame)

        Label(scrollable_frame, text="RECRUITER MENU", font=('Helvetica', 14), bg="lightblue").pack(pady=20)
        Button(scrollable_frame, text="RECRUITER LOGIN", command=self.recruiter_login, font=('Helvetica', 12), bg="lightblue").pack(pady=10)
        Button(scrollable_frame, text="BACK", command=self.menu, font=('Helvetica', 12), bg="lightblue").pack(pady=10)

    def recruiter_login(self):
        self.clear_frame()
        login_frame = make_scrollable(self.main_frame)

        Label(login_frame, text="RECRUITER LOGIN", font=('Helvetica', 14), bg="lightblue").pack(pady=20)
        Label(login_frame, text="RECRUITER NAME:", bg="lightblue").pack(pady=5)
        recruiter_name = Entry(login_frame)
        recruiter_name.pack(pady=5)

        Label(login_frame, text="PASSWORD:", bg="lightblue").pack(pady=5)
        recruiter_password = Entry(login_frame, show='*')
        recruiter_password.pack(pady=5)

        def check_recruiter_login():
            a = recruiter_name.get()
            b = recruiter_password.get()
            try:
                query = "SELECT name FROM Recruiters WHERE r_password=%s"
                cursor.execute(query, (b,))
                data = cursor.fetchone()
                if data and data[0] == a:
                    messagebox.showinfo("Success", "Welcome " + data[0])
                    self.recruiter()
                else:
                    messagebox.showerror("Error", "Invalid Credentials")
            except Exception as e:
                messagebox.showerror("Error", "Account does not exist")

        Button(login_frame, text="Login", command=check_recruiter_login, bg="lightblue").pack(pady=10)
        Button(login_frame, text="BACK", command=self.r_main, bg="lightblue").pack(pady=10)

    def recruiter(self):
        self.clear_frame()
        scrollable_frame = make_scrollable(self.main_frame)

        Label(scrollable_frame, text="RECRUITER MAIN MENU", font=('Helvetica', 14), bg="lightblue").pack(pady=20)
        Button(scrollable_frame, text="MODIFY STATUS OF STUDENTS APPLICATION", command=self.recruiter_modify_status, font=('Helvetica', 12), bg="lightblue").pack(pady=10)
        Button(scrollable_frame, text="SET INTERVIEW DETAILS", command=self.recruiter_insert_interview, font=('Helvetica', 12), bg="lightblue").pack(pady=10)
        Button(scrollable_frame, text="BACK", command=self.r_main, font=('Helvetica', 12), bg="lightblue").pack(pady=10)

    
    def recruiter_modify_status(self):
        self.clear_frame()
        status_frame = make_scrollable(self.main_frame)
        Label(status_frame, text="MODIFY APPLICATION STATUS", font=('Helvetica', 14), bg="lightblue").pack(pady=20)

        Label(status_frame, text="ENTER APPLICATION ID:", bg="lightblue").pack(pady=5)
        application_id_entry = Entry(status_frame)
        application_id_entry.pack(pady=5)

        Label(status_frame, text="NEW STATUS:", bg="lightblue").pack(pady=5)
        new_status_entry = Entry(status_frame)
        new_status_entry.pack(pady=5)

        def modify_status():
            application_id = application_id_entry.get()
            new_status = new_status_entry.get()
            try:
                query = "UPDATE Applications SET status = %s WHERE application_id = %s"
                cursor.execute(query, (new_status, application_id))
                mycon.commit()

                if cursor.rowcount > 0:
                    messagebox.showinfo("Success", "Status updated successfully.")
                else:
                    messagebox.showwarning("Error", "Application ID not found.")
                self.recruiter()
            except connector.Error as err:
                messagebox.showerror("Error", str(err))

        Button(status_frame, text="Update Status", command=modify_status, bg="lightblue").pack(pady=10)
        Button(status_frame, text="BACK", command=self.recruiter, bg="lightblue").pack(pady=10)

    def recruiter_insert_interview(self):
        self.clear_frame()
        interview_frame = make_scrollable(self.main_frame)
        Label(interview_frame, text="INSERT INTERVIEW DETAILS", font=('Helvetica', 14), bg="lightblue").pack(pady=20)

        labels = ["INTERVIEW ID", "JOB ID", "RECRUITER ID", "INTERVIEW DATE (YYYY-MM-DD)", "RESULT"]
        self.interview_entries = {}

        for label in labels:
            Label(interview_frame, text=label, bg="lightblue").pack(pady=5)
            entry = Entry(interview_frame)
            entry.pack(pady=5)
            self.interview_entries[label] = entry

        def save_interview():
            interview_data = {
                'interview_id': self.interview_entries["INTERVIEW ID"].get(),
                'job_id': self.interview_entries["JOB ID"].get(),
                'recruiter_id': self.interview_entries["RECRUITER ID"].get(),
                'interview_date': self.interview_entries["INTERVIEW DATE (YYYY-MM-DD)"].get(),
                'result': self.interview_entries["RESULT"].get(),
            }
            try:
                query = '''INSERT INTO Interviews (interview_id, job_id, recruiter_id, interview_date, result) 
                           VALUES (%(interview_id)s, %(job_id)s, %(recruiter_id)s, %(interview_date)s, %(result)s)'''
                cursor.execute(query, interview_data)
                mycon.commit()
                messagebox.showinfo("Success", "Interview details added successfully")
                self.recruiter()
            except connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")

        Button(interview_frame, text="Save Interview Details", command=save_interview, bg="lightblue").pack(pady=10)
        Button(interview_frame, text="BACK", command=self.recruiter, bg="lightblue").pack(pady=10)

    def recruiter_student_interview(self):
        self.clear_frame()
        student_interview_frame = make_scrollable(self.main_frame)
        Label(student_interview_frame, text="STUDENTS SELECTED FOR INTERVIEW", font=('Helvetica', 14), bg="lightblue").pack(pady=20)

        try:
            query = '''
                SELECT Students.name, Students.email, Students.phone_number, Jobs.job_title, Interviews.interview_date, Interviews.result
                FROM Students
                JOIN Applications ON Students.Students_id = Applications.Students_id
                JOIN Interviews ON Applications.job_id = Interviews.job_id
                JOIN Jobs ON Interviews.job_id = Jobs.job_id
                WHERE Applications.status = 'Selected'
            '''
            cursor.execute(query)
            results = cursor.fetchall()

            for row in results:
                Label(student_interview_frame, text=f"Name: {row[0]}, Email: {row[1]}, Phone: {row[2]}, Job: {row[3]}, Interview Date: {row[4]}, Result: {row[5]}").pack(pady=5)

            if not results:
                Label(student_interview_frame, text="No students selected for interviews.", font=('Helvetica', 12), bg="lightblue").pack(pady=10)
        except connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")

        Button(student_interview_frame, text="BACK", command=self.recruiter, bg="lightblue").pack(pady=10)

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = PlacementApp()
    app.mainloop()
