from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

User_model = User

class Subject(models.Model):
    subject_name = models.CharField(max_length = 20)
    compulsory = models.BooleanField(default = False)
    def __str__(self):
        return self.subject_name

class Stream(models.Model):
    stream_name = models.CharField(max_length = 20)
    def __str__(self):
        return self.stream_name
        
class Form(models.Model):
    form = models.IntegerField()
    
    def form_name(self):
        return f"form {self.form}"
    def __str__(self):
        return "form_" + str(self.form)


class Student(models.Model):
    student_name = models.CharField(max_length=30)
    student_photo = models.ImageField(null = True, blank= True)
    form = models.ForeignKey(Form, on_delete = models.CASCADE)
    stream = models.ForeignKey(Stream, on_delete = models.CASCADE)
    age = models.IntegerField(null = True, blank= True)
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return self.student_name

class Timestamp(models.Model):
    status = models.BooleanField(null = True, default = True)
    exam_name = models.CharField(max_length = 20)
    period = models.CharField(max_length = 10, null = True)
    year = models.CharField(max_length = 10, null = True)
    date_created = models.DateField(auto_now_add = True)
    results = models.TextField(null = True)

    class Meta:
        ordering = ["id"]
    def __str__(self):
        return self.exam_name

    def get_absolute_url(self):
        return reverse('generate_reports', kwargs={
            'id':self.id
        })


class Report(models.Model):
    student = models.ForeignKey(Student, on_delete = models.CASCADE)
    subjects = models.ManyToManyField(Subject)
    timestamp = models.ForeignKey(Timestamp, on_delete = models.CASCADE)
    mathematics= models.IntegerField(null = True)
    english= models.IntegerField(null = True)
    kiswahili= models.IntegerField(null = True)
    chemistry= models.IntegerField(null = True)
    biology= models.IntegerField(null = True)
    physics= models.IntegerField(null = True)
    history= models.IntegerField(null = True)
    cre= models.IntegerField(null = True)
    geography= models.IntegerField(null = True)
    computer_studies= models.IntegerField(null = True)
    bussiness= models.IntegerField(null = True)
    agriculture= models.IntegerField(null = True)
    
    form = models.ForeignKey(Form, on_delete = models.CASCADE, null = True)
    stream = models.ForeignKey(Stream, on_delete = models.CASCADE, null = True)

    def total_score(self):
        total = 0
        if self.english:
            total += self.english
        if self.mathematics:
            total += self.mathematics
        return total
    def __str__(self):
        return self.student.student_name

class Teacher_subject(models.Model):
    form = models.ForeignKey(Form, on_delete = models.CASCADE, null = True)
    stream =  models.ForeignKey(Stream, on_delete = models.CASCADE, null = True)
    subject = models.ForeignKey(Subject, on_delete = models.CASCADE, null = True)
    
    def __str__(self):
        return f"{self.form} {self.stream} {self.subject}"
    

class Teacher(models.Model):
    user = models.OneToOneField(User_model, on_delete = models.CASCADE)
    class_teacher_form = models.ForeignKey(Form, on_delete = models.CASCADE, null  = True, blank = True)
    class_teacher_stream = models.ForeignKey(Stream, on_delete = models.CASCADE, null = True, blank = True)
    teacher_photo = models.ImageField()
    teacher_subject_list = models.ManyToManyField(Teacher_subject)
    selectedDatabase = models.ForeignKey(Timestamp, on_delete = models.CASCADE, null = True, blank = True)
    selectedSubject = models.ForeignKey(Subject, on_delete = models.CASCADE, null = True, blank = True)
    is_exam_staff = models.BooleanField(default = False)
    is_principal = models.BooleanField(default = False)

    def __str__(self):
        return f"teacher {self.user.username}"
    def class_teacher(self):
        if self.class_teacher_form is not None and self.class_teacher_stream is not None:
            return f"{self.class_teacher_form.form} {self.class_teacher_stream.stream_name}"
        else:
            return ""
class GradingSystem(models.Model):
    grade = models.CharField(max_length = 2)
    upper_limit = models.IntegerField()
    lower_limit = models.IntegerField()
