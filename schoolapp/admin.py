from django.contrib import admin
from .models import Student, Report, Timestamp, Teacher_subject, Subject, Form, Stream, Teacher, GradingSystem

admin.site.register(Student)
admin.site.register(Report)
admin.site.register(Teacher_subject)
admin.site.register(Subject)
admin.site.register(Form)
admin.site.register(Stream)
admin.site.register(Timestamp)
admin.site.register(Teacher)
admin.site.register(GradingSystem)
