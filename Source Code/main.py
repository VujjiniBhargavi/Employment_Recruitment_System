import datetime
import os
import re

from bson import ObjectId
from flask import Flask, render_template, request, session, redirect
import pymongo

myClient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myClient["EmployeeRecruitmentSystem"]
vendor_col = mydb["Vendor"]
client_col = mydb["Client"]
candidate_col = mydb["Candidate"]
jobRequirement_col = mydb['JobRequirement']
jobPost_col = mydb['JobPosts']
test_col = mydb['Test']
test_question_col = mydb['TestQuestions']
job_application_col = mydb['JobApplication']
exam_result_col = mydb['ExamResult']
interview_col = mydb['Interview']

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_ROOT = APP_ROOT + "/static"

app = Flask(__name__)
app.secret_key = "yedghbnikulhn"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/aLogin")
def aLogin():
    return render_template("aLogin.html")


@app.route("/clLogin")
def clLogin():
    return render_template("clLogin.html")


@app.route("/vLogin")
def vLogin():
    return render_template("vLogin.html")


@app.route("/jsLogin")
def jsLogin():
    return render_template("jsLogin.html")


@app.route("/aLogin1", methods=['post'])
def aLogin1():
    Username = request.form.get("Username")
    Password = request.form.get("Password")
    if Username == 'admin' and Password == 'admin':
        session['role'] = 'admin'
        return render_template("ahome.html")
    return render_template("message.html", msg='Invalid Login Details', color='bg-danger')


@app.route("/ahome")
def ahome():
    return render_template("ahome.html")


@app.route("/clientRegistration")
def clientRegistration():
    return render_template("clientRegistration.html")


@app.route("/clientReg1", methods=['post'])
def clientReg1():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    address = request.form.get("address")
    password = request.form.get("password")
    employee_count = request.form.get("employee_count")
    logo = request.files['logo']
    path = APP_ROOT + "/Logo/" + logo.filename
    logo.save(path)
    description = request.form.get("description")
    total_count = client_col.count_documents({'$or': [{"email": email}, {"phone": phone}]})
    if total_count > 0:
        return render_template("message.html", msg='Client Details Already exists', color='bg-danger')
    else:
        client_col.insert_one({"name": name, "email": email, "phone": phone, "address": address, "password": password,
                               "employee_count": employee_count, "logo": logo.filename, "description": description,
                               "status": 'UnAuthorized'})
        return render_template('message.html', msg='Client Registered Successfully', color='bg-success')


@app.route("/viewClients")
def viewClients():
    clients = client_col.find()
    return render_template("viewClients.html", clients=clients)


@app.route("/authorizedClient")
def authorizedClient():
    client_id = request.args.get('client_id')
    query = {'_id': ObjectId(client_id)}
    query1 = {"$set": {"status": "Authorized"}}
    client_col.update_one(query, query1)
    return redirect("/viewClients")


@app.route("/vendorRegistration")
def vendorRegistration():
    return render_template("vendorRegistration.html")


@app.route("/vendorReg1", methods=['post'])
def vendorReg1():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    address = request.form.get("address")
    password = request.form.get("password")
    experience = request.form.get("experience")
    description = request.form.get("description")
    total_count = vendor_col.count_documents({'$or': [{"email": email}, {"phone": phone}]})
    if total_count > 0:
        return render_template("message.html", msg='Vendor Details Already exists', color='bg-danger')
    else:
        vendor_col.insert_one({"name": name, "email": email, "phone": phone, "address": address, "password": password,
                               "experience": experience, "description": description, "status": 'UnAuthorized'})
        return render_template('message.html', msg='Vendor Registered Successfully', color='bg-success')


@app.route("/viewVendors")
def viewVendors():
    vendors = vendor_col.find()
    return render_template("viewVendors.html", vendors=vendors)


@app.route("/authorizedVendor")
def authorizedVendor():
    vendor_id = request.args.get('vendor_id')
    query = {'_id': ObjectId(vendor_id)}
    query1 = {"$set": {"status": "Authorized"}}
    vendor_col.update_one(query, query1)
    return redirect("/viewVendors")


@app.route("/candidateRegistration")
def candidateRegistration():
    return render_template("candidateRegistration.html")


@app.route("/candidateReg1", methods=['post'])
def candidateReg1():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    resume = request.files.get("resume")
    path = APP_ROOT + "/Resume/" + resume.filename
    resume.save(path)
    password = request.form.get("password")
    experience = request.form.get("experience")
    photo = request.files['photo']
    path = APP_ROOT + "/Profile/" + photo.filename
    photo.save(path)
    qualification = request.form.get('qualification')
    skills = request.form.get('skills')
    about = request.form.get("about")
    total_count = candidate_col.count_documents({'$or': [{"email": email}, {"phone": phone}]})
    if total_count > 0:
        return render_template("message.html", msg='Candidate Details Already exists', color='bg-danger')
    else:
        candidate_col.insert_one(
            {"name": name, "email": email, "phone": phone, "resume": resume.filename, "password": password,
             "experience": experience, "photo": photo.filename, "qualification": qualification, "skills": skills,
             "about": about})
        return render_template('message.html', msg='Candidate Registered Successfully', color='bg-success')


@app.route("/jsLogin1", methods=['post'])
def jsLogin1():
    email = request.form.get("email")
    password = request.form.get("password")
    myquery = {"email": email, "password": password}
    count = candidate_col.count_documents(myquery)
    if count > 0:
        results = candidate_col.find(myquery)
        for result in results:
            session['Candidate_id'] = str(result['_id'])
            session['role'] = 'Candidate'
            session['photo'] = str(result['photo'])
            session['name'] = str(result['name'])
            session['phone'] = str(result['phone'])
            return render_template("cHome.html")

    else:
        return render_template("message.html", msg="Invalid login details", color='text-danger')


@app.route("/vLogin1", methods=['post'])
def vLogin1():
    email = request.form.get("email")
    password = request.form.get("password")
    myquery = {"email": email, "password": password}
    count = vendor_col.count_documents(myquery)
    if count > 0:
        result = vendor_col.find_one(myquery)
        if result["status"] == "Authorized":
            session['vendor_id'] = str(result['_id'])
            session['role'] = 'Vendor'
            return render_template("vHome.html")
        else:
            return render_template("message.html", msg="Vendor is Unauthorized", color='text-danger')
    else:
        return render_template("message.html", msg="Invalid login details", color='text-danger')


@app.route("/clLogin1", methods=['post'])
def clLogin1():
    email = request.form.get("email")
    password = request.form.get("password")
    myquery = {"email": email, "password": password}
    count = client_col.count_documents(myquery)
    if count > 0:
        result = client_col.find_one(myquery)
        if result["status"] == "Authorized":
            session['client_id'] = str(result['_id'])
            session['role'] = 'Client'
            session['logo'] = str(result['logo'])
            return render_template("clHome.html")
        else:
            return render_template("message.html", msg="Client is Unauthorized", color='text-danger')
    else:
        return render_template("message.html", msg="Invalid login details", color='text-danger')


@app.route("/clHome")
def clHome():
    return render_template("clHome.html")


@app.route("/vHome")
def vHome():
    return render_template("vHome.html")


@app.route("/cHome")
def cHome():
    return render_template("cHome.html")


@app.route("/jobRequirement")
def jobRequirement():
    vendors = vendor_col.find()
    return render_template("jobRequirement.html", vendors=vendors)


@app.route("/jobRequirement1", methods=['post'])
def jobRequirement1():
    client_id = session['client_id']
    job_title = request.form.get('job_title')
    job_description = request.form.get('job_description')
    experience_needed = request.form.get('experience_needed')
    number_of_positions = request.form.get('number_of_positions')
    skills = request.form.get('skills')
    vendor_ids = request.form.getlist('vendor_id')
    vendor_ids2 = []
    for vendor_id in vendor_ids:
        vendor_ids2.append(ObjectId(vendor_id))
    status = "Requirement Published"
    query = {"client_id": ObjectId(client_id), "vendor_ids": vendor_ids2, "job_title": job_title,
             "job_description": job_description, "experience_needed": experience_needed,
             "number_of_positions": number_of_positions, "skills": skills, "status": status}
    jobRequirement_col.insert_one(query)
    return render_template("message.html", msg="Job Requirement Added Successfully", color="bg-success text-white")


def get_client_id(client_id):
    query = {"_id": ObjectId(client_id)}
    client = client_col.find_one(query)
    return client


def get_vendor_id(vendor_id):
    query = {"_id": vendor_id}
    vendor = vendor_col.find_one(query)
    return vendor


def get_requirement_id(requirement_id):
    query = {"_id": requirement_id}
    requirement = jobRequirement_col.find_one(query)
    return requirement


def get_test_id(test_id):
    query = {"_id": test_id}
    test = test_col.find_one(query)
    return test


def get_test_question_id(test_question_id):
    query = {"_id": test_question_id}
    test_question = test_question_col.find_one(query)
    return test_question


def get_customer_id(Candidate_id):
    query = {"_id": Candidate_id}
    candidate = candidate_col.find_one(query)
    return candidate


def get_jobDetails(jobpost_id):
    query = {"_id": jobpost_id}
    jobpost = jobPost_col.find_one(query)
    query = {"_id": jobpost['requirement_id']}
    job_requirement = jobRequirement_col.find_one(query)
    return jobpost, job_requirement


@app.route("/viewJobRequirements")
def viewJobRequirements():
    if session['role'] == 'Client':
        client_id = session['client_id']
        query = {"client_id": ObjectId(client_id)}
    elif session['role'] == 'Vendor':
        vendor_id = session['vendor_id']
        query = {"vendor_ids": {"$elemMatch": {"$eq": ObjectId(vendor_id)}}}
    requirements = jobRequirement_col.find(query)
    return render_template("viewJobRequirements.html", requirements=requirements, get_client_id=get_client_id,
                           get_vendor_id=get_vendor_id)


@app.route("/publishRequirement")
def publishRequirement():
    requirement_id = request.args.get('requirement_id')
    return render_template("publishRequirement.html", requirement_id=requirement_id)


@app.route("/publishRequirement1", methods=['get'])
def publishRequirement1():
    vendor_id = session['vendor_id']
    requirement_id = request.args.get('requirement_id')
    date = datetime.datetime.now()
    status = "Requirement Posted"
    query = {"vendor_id": ObjectId(vendor_id), "requirement_id": ObjectId(requirement_id), "date": date,
             "status": status}
    jobPost_col.insert_one(query)
    return render_template("message.html", msg="Job Posted Successfully", color="bg-success text-white")


@app.route("/viewJobPosts")
def viewJobPosts():
    if session['role'] == 'Vendor':
        vendor_id = session['vendor_id']
        query = {"vendor_id": ObjectId(vendor_id)}
    elif session['role'] == 'Candidate':
        Candidate_id = session['Candidate_id']
        query = {"_id": ObjectId(Candidate_id)}
        candidate = candidate_col.find_one(query)
        skills = str(candidate['skills']).strip()
        skills = skills.replace(",", " ")
        skills = skills.replace("  ", " ")
        print(skills)
        skills = skills.split(" ")
        print(skills)
        skills2 = []
        for skill in skills:
            rgx = re.compile(".*" + skill + ".*", re.IGNORECASE)
            skills2.append({"skills": rgx})
        query = {"$or": skills2}
        job_requirements = jobRequirement_col.find(query)
        job_requirement_ids = []
        for job_requirement in job_requirements:
            job_requirement_ids.append({"requirement_id": job_requirement['_id']})
        if len(job_requirement_ids) == 0:
            return render_template("message.html", msg="No Job Posts are Available", color="bg-danger text-white")
        query = {"$or": job_requirement_ids}
        print(query)
    jobposts = jobPost_col.find(query)
    jobposts = list(jobposts)
    jobposts.reverse()
    return render_template("viewJobPosts.html", jobposts=jobposts, get_vendor_id=get_vendor_id,
                           get_requirement_id=get_requirement_id)


@app.route("/addTest")
def addTest():
    return render_template("addTest.html")


@app.route("/addTest1", methods=['post'])
def addTest1():
    vendor_id = session['vendor_id']
    test_title = request.form.get('test_title')
    cut_of_percentage = request.form.get('cut_of_percentage')
    test_description = request.form.get('test_description')
    query = {"vendor_id": ObjectId(vendor_id), "test_title": test_title, "cut_of_percentage": cut_of_percentage,
             "test_description": test_description}
    result = test_col.insert_one(query)
    test = result.inserted_id
    return redirect("/addQuestion?test_id=" + str(test))


@app.route("/addQuestion")
def addQuestion():
    test_id = request.args.get('test_id')
    query = {"test_id": ObjectId(test_id)}
    count = test_question_col.count_documents(query)
    question_number = count + 1
    return render_template("addQuestion.html", test_id=test_id, question_number=question_number)


@app.route("/addQuestion1", methods=['post'])
def addQuestion1():
    test_id = request.form.get('test_id')
    question = request.form.get('question')
    option1 = request.form.get('option1')
    Option2 = request.form.get('Option2')
    Option3 = request.form.get('Option3')
    Option4 = request.form.get('Option4')
    answer = request.form.get('answer')
    query = {"test_id": ObjectId(test_id), "question": question, "option1": option1, "option2": Option2,
             "option3": Option3, "option4": Option4, "answer": answer}
    test_question_col.insert_one(query)
    return redirect("/addQuestion?test_id=" + str(test_id))


@app.route("/viewTest")
def viewTest():
    vendor_id = session['vendor_id']
    query = {"vendor_id": ObjectId(vendor_id)}
    tests = test_col.find(query)
    return render_template("viewTest.html", tests=tests, get_vendor_id=get_vendor_id)


@app.route("/viewTestQuestions")
def viewTestQuestions():
    test_id = request.args.get('test_id')
    query = {"test_id": ObjectId(test_id)}
    test_questions = test_question_col.find(query)
    count = test_question_col.count_documents(query)
    query = {"_id": ObjectId(test_id)}
    test = test_col.find_one(query)

    return render_template("viewTestQuestions.html", test_questions=test_questions, test=test, count=count)


@app.route("/jobApplication")
def jobApplication():
    jobpost_id = request.args.get('jobpost_id')
    Candidate_id = session['Candidate_id']
    status = "Applied Successfully"
    date = datetime.datetime.now()
    query = {"jobpost_id": ObjectId(jobpost_id), "Candidate_id": ObjectId(Candidate_id), "date": date, "status": status}
    job_application_col.insert_one(query)
    return render_template("message.html", msg="Applied Successfully", color="bg-success text-white")


@app.route("/viewJobApplications")
def viewJobApplications():
    jobpost_id = request.args.get('jobpost_id')
    if session['role'] == 'Candidate':
        jobpost_id = None
        Candidate_id = session['Candidate_id']
        query = {"Candidate_id": ObjectId(Candidate_id)}
    elif session['role'] == 'Vendor':
        jobpost_id = request.args.get('jobpost_id')
        query = {"jobpost_id": ObjectId(jobpost_id)}
    elif session['role'] == 'Client':
        requirement_id = request.args.get('requirement_id')
        vendor_id = request.args.get('vendor_id')
        query = {"requirement_id": ObjectId(requirement_id),"vendor_id": ObjectId(vendor_id)}
        jobpost = jobPost_col.find_one(query)
        if jobpost == None:
            return render_template("message.html", msg="This Vendor Not Published the Job Requirements", color="bg-danger text-white")
        query = {"jobpost_id": jobpost['_id']}
        jobposts = jobPost_col.find(query)
        jobpost_ids = []
        for jobpost in jobposts:
            jobpost_ids.append({"jobpost_id": jobpost['_id'], "$or": [{"status": "Test Cleared"},{"status": "Interview Scheduled"}, {"status": "Interview Schedule Accepted"},{"status": "Candidate Selected by Client"}, {"status": "interview Schedule Cancelled"},{"status": "Candidate Rejected by Client"}]})
            if len(jobpost_ids) == 0:
                return render_template("message.html", msg="No Applications Founded", color="bg-danger text-white")
            else:
                query = {"$or": jobpost_ids}
    job_applications = job_application_col.find(query)
    return render_template("viewJobApplications.html", job_applications=job_applications, get_jobDetails=get_jobDetails,
                           get_customer_id=get_customer_id, jobpost_id=jobpost_id)


@app.route("/assignTest")
def assignTest():
    job_application_id = request.args.get('job_application_id')
    jobpost_id = request.args.get('jobpost_id')
    query = {"vendor_id": ObjectId(session['vendor_id'])}
    tests = test_col.find(query)
    return render_template("assignTest.html", tests=tests, job_application_id=job_application_id, jobpost_id=jobpost_id,
                           get_vendor_id=get_vendor_id)


@app.route("/assignTest1", methods=['post'])
def assignTest1():
    jobpost_id = request.form.get('jobpost_id')
    job_application_id = request.form.get('job_application_id')
    test_id = request.form.get('test_id')
    query = {"_id": ObjectId(job_application_id)}
    query2 = {"$set": {"test_id": ObjectId(test_id), "status": "Test Assigned"}}
    job_application_col.update_one(query, query2)
    return redirect("/viewJobApplications?jobpost_id=" + str(jobpost_id))


@app.route("/writeTest")
def writeTest():
    job_application_id = request.args.get('job_application_id')
    test_id = request.args.get('test_id')
    query = {"_id": ObjectId(test_id)}
    tests = test_col.find(query)
    return render_template("writeTest.html", tests=tests, job_application_id=job_application_id, test_id=test_id,
                           get_vendor_id=get_vendor_id)


@app.route("/writeTest1", methods=['post'])
def writeTest1():
    job_application_id = request.form.get('job_application_id')
    test_id = request.form.get('test_id')
    query = {"test_id": ObjectId(test_id)}
    test_questions = test_question_col.find(query)
    return render_template("writeTest1.html", test_id=test_id, job_application_id=job_application_id,
                           test_questions=test_questions)


@app.route("/writeTest2", methods=['post'])
def writeTest2():
    job_application_id = request.form.get('job_application_id')
    test_id = request.form.get('test_id')
    query = {"test_id": ObjectId(test_id)}
    test_questions = test_question_col.find(query)
    total_count = 0
    correct_count = 0
    wrong_count = 0
    not_answered_count = 0
    for test_question in test_questions:
        test_question_id = test_question['_id']
        candidate_answer = request.form.get(str(test_question_id))
        print(test_question_id)
        print(candidate_answer)
        total_count = total_count + 1
        if candidate_answer == None:
            not_answered_count = not_answered_count + 1
            status = "Not Answered"
        elif candidate_answer == test_question['answer']:
            correct_count = correct_count + 1
            status = "Correct Answer"
        elif candidate_answer != test_question['answer']:
            wrong_count = wrong_count + 1
            status = "Wrong Answer"
        query = {"job_application_id": ObjectId(job_application_id), "test_id": ObjectId(test_id), "test_question_id": test_question_id, "candidate_answer": candidate_answer, "status": status}
        exam_result_col.insert_one(query)
    percentage = (correct_count/total_count)*100
    query = {"_id": ObjectId(test_id)}
    print(query)
    test = test_col.find_one(query)
    print(test)
    if float(test['cut_of_percentage']) > percentage:
        status = "Failed To Clear The Test"
    else:
        status = "Test Cleared"
    query = {"_id": ObjectId(job_application_id)}
    query2 = {"$set": {"status": status}}
    job_application_col.update_one(query, query2)
    return redirect("/viewResult?job_application_id="+str(job_application_id)+"&test_id="+str(test_id))


@app.route("/viewResult")
def viewResult():
    job_application_id = request.args.get('job_application_id')
    test_id = request.args.get('test_id')
    query = {"job_application_id": ObjectId(job_application_id), "test_id": ObjectId(test_id)}
    exam_results = exam_result_col.find(query)
    query = {"_id": ObjectId(test_id)}
    test = test_col.find_one(query)
    return render_template("viewResult.html", exam_results=exam_results, test=test,  get_test_question_id=get_test_question_id)


@app.route("/interviewSchedule")
def interviewSchedule():
    job_application_id = request.args.get('job_application_id')
    return render_template("interviewSchedule.html", job_application_id=job_application_id)


@app.route("/interviewSchedule1", methods=['post'])
def interviewSchedule1():
    job_application_id = request.form.get('job_application_id')
    interview_date = request.form.get('interview_date')
    interview_time = request.form.get('interview_time')
    description = request.form.get('description')
    status = "Interview Scheduled"
    query = {"job_application_id": ObjectId(job_application_id), "interview_date": interview_date, "interview_time": interview_time, "description": description, "status": status}
    interview_col.insert_one(query)
    query = {"_id": ObjectId(job_application_id)}
    query2 = {"$set": {"status": status}}
    job_application_col.update_one(query, query2)
    return render_template("message.html", msg="Interview Schedule Added Successfully", color="bg-success text-white")


@app.route("/viewInterviewSchedule")
def viewInterviewSchedule():
    interviews = interview_col.find()
    return render_template("viewInterviewSchedule.html", interviews=interviews)


@app.route("/acceptInterview")
def acceptInterview():
    job_application_id = request.args.get('job_application_id')
    query = {'_id': ObjectId(job_application_id)}
    query1 = {"$set": {"status": "Interview Schedule Accepted"}}
    job_application_col.update_one(query, query1)
    query = {'job_application_id': ObjectId(job_application_id)}
    query1 = {"$set": {"status": "Interview Schedule Accepted"}}
    interview_col.update_one(query, query1)
    return render_template("message.html", msg="Interview Schedule Accepted", color="bg-success text-white")


@app.route("/cancelledInterview")
def cancelledInterview():
    job_application_id = request.args.get('job_application_id')
    query = {'_id': ObjectId(job_application_id)}
    query1 = {"$set": {"status": "Interview Schedule Cancelled"}}
    job_application_col.update_one(query, query1)
    query = {'job_application_id': ObjectId(job_application_id)}
    query1 = {"$set": {"status": "Interview Schedule Cancelled"}}
    interview_col.update_one(query, query1)
    return render_template("message.html", msg="Interview Schedule Cancelled", color="bg-danger text-white")


@app.route("/clientAccept")
def clientAccept():
    job_application_id = request.args.get('job_application_id')
    query = {'_id': ObjectId(job_application_id)}
    query1 = {"$set": {"status": "Candidate Selected by Client"}}
    job_application_col.update_one(query, query1)
    query = {'job_application_id': ObjectId(job_application_id)}
    query1 = {"$set": {"status": "Candidate Selected by Client"}}
    interview_col.update_one(query, query1)
    return render_template("message.html", msg="Candidate Selected by Client", color="bg-success text-white")


@app.route("/clientReject")
def clientReject():
    job_application_id = request.args.get('job_application_id')
    query = {'_id': ObjectId(job_application_id)}
    query1 = {"$set": {"status": "Candidate Rejected by Client"}}
    job_application_col.update_one(query, query1)
    query = {'job_application_id': ObjectId(job_application_id)}
    query1 = {"$set": {"status": "Candidate Rejected by Client"}}
    interview_col.update_one(query, query1)
    return render_template("message.html", msg="Candidate Rejected by Client", color="bg-danger text-white")


@app.route("/logout")
def logout():
    session.clear()
    return render_template("index.html")


app.run(debug=True)
