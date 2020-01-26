import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import numpy as np
from zipfile import ZipFile
from .utils import generate_pdf_report
from weasyprint import HTML
from django.template.loader import get_template
import json
from django.core import serializers
from django.shortcuts import render
from datetime import date, datetime
from .models import Timestamp, Report, Student, Teacher_subject, Stream, Form, Teacher, Subject, GradingSystem
from django.shortcuts import redirect, get_object_or_404, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user, logout as log_out
from collections import OrderedDict


from.fusioncharts import FusionCharts

def chartArea(caption, xAxisName, yAxisName, theme):
    chartConfig = OrderedDict()
    chartConfig['caption'] = caption
    chartConfig['xAxisName'] = xAxisName
    chartConfig['yAxisName'] = yAxisName
    chartConfig['theme'] = theme
    return chartConfig

#generating a pdf from a html template rendered with some context
def student_pdf_report(request, xlist, ylist, student_name):
    index = np.arange(len(xlist))
    graph = plt.bar(index, ylist)
    for y in ylist:
        graph[ylist.index(y)].set_color("grey")
    graph[len(ylist) - 1].set_color("black")
    plt.xlabel('exam name')
    plt.ylabel('average score')
    plt.xticks(index, xlist)
    plt.title(f"{student_name} performance trend")
    buf = BytesIO()
    plt.savefig(buf, format = 'png', dpi = 300)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    context = {
        'image_base64':image_base64,
    }
    html = get_template("report_card.html").render(context)
    pdf_file = HTML(string = html, base_url = request.build_absolute_uri()).write_pdf()
    return pdf_file
    



def homepage(request):
    active_user = False
    teacher_queryset = Teacher.objects.all()
    chartConfig = OrderedDict()
    chartConfig['caption'] = 'school average marks based on the last few exams'
    chartConfig['subCaption'] = 'these results are based on total marks'
    chartConfig['xAxisName'] = 'exam'
    chartConfig['yAxisName'] = 'average marks'
    chartConfig['theme'] = 'fusion'
    chartData = OrderedDict()
    chartData['chart'] = chartConfig
    chartData['data'] = []
    for x in Timestamp.objects.all():
        if x.results is not None:
            results = json.loads(x.results)
            total_marks = 0
            for y in results:
                total_marks += int(y['total_score'])
            chartData['data'].append({'label':x.exam_name, 'value':total_marks})
    column2D = FusionCharts('column2d','first chart','100%', '400', 'chart-area','json',chartData)

    if request.user.is_authenticated:
        active_user = True
        user = request.user
        context = {
            "user":user,
            "active_user":active_user,
            "teacher_queryset": teacher_queryset,
            'chart': column2D.render()
        }
        return render(request, 'homepage.html', context)
    context = {
        "active_user":active_user,
        "teacher_queryset": teacher_queryset,
        'chart': column2D.render()
    }
    return render(request, "homepage.html", context)
def student_registration(request):
    context = {
        'subject_queryset':Subject.objects.all(),
        'form_queryset':Form.objects.all(),
        'stream_queryset':Stream.objects.all(),
    }
    return render(request, 'student_registration.html', context)

def contact(request):
    return render(request, 'contact.html', {})
def view_reports(request):
    active_user = False
    if request.user.is_authenticated:
        active_user = True
        user = request.user
    else:
        return redirect('login')
    timestamp_queryset = Timestamp.objects.exclude(results__isnull=True).exclude(results__exact = '')

    context = {
        'user':user,
        'active_user': active_user,
        'object_list':timestamp_queryset,
    }
    return render(request, 'view_reports.html', context)

def timestamp_list(request):
    if request.method == "POST":
        timestamp = get_object_or_404(Timestamp, id = request.POST.get("timestamp_id"))
        if timestamp.status:
            timestamp.status = False
            timestamp.save()
        else:
            timestamp.status = True
            timestamp.save()
    queryset = Timestamp.objects.all()
    context = {
        "object_list": queryset,
    }
    return render(request, "timestamp/timestamp_list.html", context)


def timestamp(request):
    if request.user.is_authenticated:
        user = request.user
        active_user = True
    else:
        return redirect('login')
    message = False
    if request.method == "POST":
        if request.POST.get('year') and request.POST.get("exam_name") and request.POST.get("period"):
            exam_name = request.POST.get("exam_name")
            period = request.POST.get("period")
            year = request.POST.get("year")
            timestamp = Timestamp.objects.create(exam_name = exam_name, year= year, period = period, status=False)
            student_queryset = Student.objects.all()
            for student in student_queryset:
                Report.objects.create(student = student, timestamp = timestamp, form = student.form, stream= student.stream).subjects.set(student.subjects.all())
            return redirect('timestamp_list')

    today = date.today()
    year = today.year
    context = {
        "active_user": active_user,
        "user":user,
        "message": message,
        "year":year,
    }
    return render(request, 'timestamp/timestamp.html', context)

def logout(request):
    log_out(request)
    return redirect('homepage')
    
def login(request):
    if request.method == "POST":
        if request.POST.get("pass") and request.POST.get("username"):
            username = request.POST.get("username")
            password = request.POST.get("pass")
            user = authenticate(request, username = username, password = password)
            if user is not None:
                #the login_user function sets the user in session with the browser
                login_user(request, user = user)
                return redirect("dashboard")


    context = {

    }
    return render(request, 'login.html', context)

def profile(request):
    if request.user.is_authenticated:
        active_user = True
        user = request.user
    else:
        return redirect('login')
    
    context = {
        'active_user': active_user,
        'user': user
    }
    return render(request, 'profile.html', context)

def dashboard(request):
    if request.user.is_authenticated:
        active_user = True
        user = request.user
    else:
        return redirect('login')
    if request.GET.get("request"):
        timestamp_queryset = Timestamp.objects.filter(status = True)
        context = {
            'user': user,
            'active_user': active_user,
            "object_list":timestamp_queryset,
        }
        return render(request, "dashboard_templates/timestamp_selection.html", context)
    if request.GET.get("timestamp"):
        timestamp_id =  request.GET.get("timestamp")
        timestamp = get_object_or_404(Timestamp, id = timestamp_id)
        user = request.user
        user.teacher.selectedDatabase = timestamp
        user.teacher.save()
        teacher_subject_list = user.teacher.teacher_subject_list.all()
        context = {
            'user':user,
            'active_user': active_user,
            "teacher_subject_list":teacher_subject_list,
            "timestamp":timestamp,
        }
        timestamp = False
        return render(request, 'dashboard_templates/teacher_subject_list.html', context)

    if request.GET.get("score_sheet"):
        if request.method == "POST":
            report_keys_list = []
            for x in request.POST.keys():
                report_keys_list.append(x)
            report_keys_list.remove("csrfmiddlewaretoken")
            subject = request.user.teacher.selectedSubject.subject_name
            for subject_mark_id in report_keys_list:
                report = get_object_or_404(Report, id = int(subject_mark_id))
                if subject == "mathematics":
                    report.mathematics = request.POST.get(subject_mark_id)
                    report.save()
                if subject == "english":
                    report.english = request.POST.get(subject_mark_id)
                    report.save()
                if subject == "kiswahili":
                    report.kiswahili = request.POST.get(subject_mark_id)
                    report.save()
                if subject == "chemistry":
                    report.chemistry = request.POST.get(subject_mark_id)
                    report.save()
                if subject == "biology":
                    report.biology = request.POST.get(subject_mark_id)
                    report.save()
                if subject == "physics":
                    report.physics = request.POST.get(subject_mark_id)
                    report.save()
                if subject == "history":
                    report.history = request.POST.get(subject_mark_id)
                    report.save()
                if subject == "geography":
                    report.geography = request.POST.get(subject_mark_id)
                    report.save()
                if subject == "cre":
                    report.cre = request.POST.get(subject_mark_id)
                    report.save()
                if subject == "computer_studies":
                    report.computer_studies = request.POST.get(subject_mark_id)
                    report.save()
                if subject == "bussiness":
                    report.bussiness = request.POST.get(subject_mark_id)
                    report.save()
                if subject == "agriculture":
                    report.agriculture = request.POST.get(subject_mark_id)
                    report.save()

        teacher_subject = get_object_or_404(Teacher_subject, id = request.GET.get("score_sheet"))
        subject = teacher_subject.subject
        request.user.teacher.selectedSubject = subject
        request.user.teacher.save()
        # student_queryset = subject.student_set.all().filter(timestamp = request.user.teacher.selectedDatabase ,stream = teacher_subject.stream, form=teacher_subject.form)
        # student_queryset = Report.objects.filter(timestamp = request.user.teacher.selectedDatabase ,stream = teacher_subject.stream, form=teacher_subject.form)
        student_queryset = subject.report_set.all().filter(timestamp = request.user.teacher.selectedDatabase ,stream = teacher_subject.stream, form=teacher_subject.form)
        context = {
            "user": user,
            "active_user": active_user,
            "subject": request.user.teacher.selectedSubject.subject_name,
            "timestamp":request.user.teacher.selectedDatabase,
            "object_list":student_queryset,
            "teacher_subject":teacher_subject,
        }
        return render(request, "dashboard_templates/score_sheet.html", context)
    context = {
        'user':user,
        'active_user':active_user,
    }
    return render(request, "dashboard_templates/dashboard.html", context)

def generate_results(request):
    active_user = False
    if request.user.is_authenticated:
        user = request.user
        active_user = True
    else:
        return redirect('login')
    if request.method != 'POST':
        timestamp_queryset = Timestamp.objects.filter(status = True)
        context = {
            'user': user,
            'active_user': active_user,
            'object_list': timestamp_queryset
        }
        return render(request, 'timestamp/timestamp_list_results.html', context)
    ts = get_object_or_404(Timestamp, id = int(request.POST.get('timestamp'))) 
    reports = Report.objects.filter(timestamp = ts)
    reports_json = serializers.serialize('json', reports)
    reports_list =json.loads(reports_json)
    results = []
    #calculating the total_score for every report generated
    for report in reports_list:
        if report['fields']['mathematics'] == None:
            report['fields']['mathematics'] = 0
        if report['fields']['english'] == None:
            report['fields']['english'] = 0
        if report['fields']['kiswahili'] == None:
            report['fields']['kiswahili'] = 0
        if report['fields']['chemistry'] == None:
            report['fields']['chemistry'] = 0
        if report['fields']['biology'] == None:
            report['fields']['biology'] = 0
        if report['fields']['physics'] == None:
            report['fields']['physics'] = 0
        if report['fields']['history'] == None:
            report['fields']['history'] = 0
        if report['fields']['geography'] == None:
            report['fields']['geography'] = 0
        if report['fields']['cre'] == None:
            report['fields']['cre'] = 0
        if report['fields']['computer_studies'] == None:
            report['fields']['computer_studies'] = 0
        if report['fields']['bussiness'] == None:
            report['fields']['bussiness'] = 0
        if report['fields']['agriculture'] == None:
            report['fields']['agriculture'] = 0
        report['total_score'] = report['fields']['mathematics'] + report['fields']['english'] + report['fields']['kiswahili'] + report['fields']['chemistry']+ report['fields']['biology'] +report['fields']['physics'] + report['fields']['history'] + report['fields']['cre'] + report['fields']['geography'] + report['fields']['computer_studies'] + report['fields']['bussiness'] + report['fields']['agriculture']
    for form in Form.objects.all():
        reports = []
        for x in reports_list:
            if int(x['fields']['form']) == int(form.id):
                reports.append(x)
        reports = sorted(reports, key = lambda i: i['total_score'], reverse = True)
        for report in reports:
            report['class_rank'] = reports.index(report) + 1
        for y in reports:
            for z in reports:
                if y['total_score'] == z['total_score']:
                    if int(y['class_rank']) > int(z['class_rank']):
                        y['class_rank'] = z['class_rank']
                    if int(y['class_rank']) < int(z['class_rank']):
                        z['class_rank'] = y['class_rank']
        for stream in Stream.objects.all():
            stream_reports = []
            for report in reports:
                if int(report['fields']['stream']) == int(stream.id):
                    stream_reports.append(report) 
            stream_reports = sorted(stream_reports, key = lambda i: i['total_score'], reverse = True)
            for report in stream_reports:
                report['stream_rank'] = stream_reports.index(report) + 1
            for y in stream_reports:
                for z in stream_reports:
                    if y['total_score'] == z['total_score']:
                        if int(y['stream_rank']) > int(z['stream_rank']):
                            y['stream_rank'] = z['stream_rank']
                        if int(y['stream_rank']) < int(z['stream_rank']):
                            z['stream_rank'] = y['stream_rank']
            for report in stream_reports:
                results.append(report)
    #results list contain the results for the entire school
    print(results)
    ts.results = json.dumps(results)
    ts.save()
    return redirect('view_reports')

def generate_reports(request, id):
    active_user = False
    if request.user.is_authenticated:
        user = request.user
        active_user = True
    else:
        return redirect('login')
    chartConfig = OrderedDict()
    chartConfig['caption'] = 'comparison of average marks per class'
    chartConfig['theme'] = 'fusion'
    chartConfig['xAxisName']= 'form/class'
    chartConfig['yAxisName'] = 'average_marks'
    chartData = OrderedDict()
    chartData['chart'] = chartConfig
    chartData['data'] = []    

    results = json.loads(get_object_or_404(Timestamp, id = id).results)
    for form in Form.objects.all():
        form_total_score = 0
        form_no_students = 0
        for result in results:
            if result['fields']['form'] == form.id:
                form_total_score += int(result['total_score'])
                form_no_students += 1
        if form_total_score != 0 and form_no_students != 0:
            average_score = form_total_score/form_no_students
        else:
            average_score = 0
        chartData['data'].append({'label':'form '+ str(form.form), 'value':average_score})
    first_graph = FusionCharts('column3d', 'first_graph', '100%', '300','first-graph','json', chartData)
    chart_list = []
    #this code checks how subjects performed against each other in every stream
    for form in Form.objects.all():
        chartConfig = chartArea(f"how form {form.form} subjects performed against each other ",'subject', 'marks','fusion')
        chartData = OrderedDict()
        chartData['chart'] = chartConfig
        chartData['data'] = []
        for subject in Subject.objects.all():
            subject_total = 0
            students_no = 0
            for result in results:  
                if int(result['fields']['form']) == form.id:
                    subject_total += result['fields'][subject.subject_name]
                    students_no += 1
            if subject_total != 0 and students_no != 0:
                subject_average = subject_total/students_no
            else:
                subject_average = 0
            chartData['data'].append({'label':subject.subject_name, 'value':subject_average})
        chart_container = []
        chart_container.append(form)
        chart_container.append(FusionCharts("column2d", f"form-{form.form}",'100%', '300', f"form_{form.form}",'json',chartData).render())
        chart_list.append(chart_container)
    #this code compares how streams performed against each other
    chart_list2 = []
    for form in Form.objects.all():
        chart_plane = chartArea(f"How form {form.form} streams performed against each other","stream","average_score","fusion")
        chartData = OrderedDict()
        chartData['chart'] = chart_plane
        chartData['data'] = []

        for stream in Stream.objects.all():
            total_stream_score = 0
            total_students_stream = 0
            for result in results:
                if int(result['fields']['form']) == form.id and int(result['fields']['stream']) == stream.id:
                    total_stream_score += result['total_score']
                    total_students_stream += 1
            if total_stream_score != 0 and total_students_stream != 0:
                average_score = total_stream_score/total_students_stream
            else:
                average_score = 0
            chartData['data'].append({'label': stream.stream_name, 'value':average_score})
        chart_list2.append([f"form__{form.form}",FusionCharts('column2d', f"form--{form.form}", "100%", "400",f"form__{form.form}", 'json', chartData).render()])
    if request.GET.get("stream") and request.GET.get("form"):
        stream = get_object_or_404(Stream , id = request.GET.get("stream"))
        form = get_object_or_404(Form , id = request.GET.get("form"))
        timestamp = get_object_or_404(Timestamp, id = id)

    context = {
        'chart_list2':chart_list2,
        'chart_list': chart_list,
        'first_graph': first_graph,
        'user':user,
        'active_user': active_user,
        'form_queryset': Form.objects.all(),
        'stream_queryset':Stream.objects.all()
    }

    return render(request, 'generated_reports.html', context)

def report_card(request):
    if request.user.is_authenticated:
        user = request.user
        active_user = True
    else:
        return redirect('login')

    pdf_file = student_pdf_report(request, ['opener', 'jesma 1', 'jesma 2', 'endterm'],[230, 320, 300, 350], 'mungai hosea')
    response = HttpResponse(content_type= 'application/zip')
    zf = ZipFile(response, 'w')
    zf.writestr("reportcard.pdf", pdf_file)
    response['Content-Disposition'] = "filename = form1_yellow_report_cards.zip"
    return response



def addstuff(request):
    for form in Form.objects.all():
        for stream in Stream.objects.all():
            for subject in Subject.objects.all():
                Teacher_subject.objects.create(form = form , stream = stream, subject = subject)
    return HttpResponse("<h1> contents added sucessfully </h1>")



def buttons(request):
    return render(request, "extras/buttons.html", {})
def icons(request):
    return render(request, "extras/icons.html", {})
def form(request):
    return render(request, 'extras/form.html', {})
def table(request):
    return render(request, 'extras/table.html', {})
