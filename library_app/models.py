from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enrollment = models.CharField(max_length=50)
    branch = models.CharField(max_length=50)

class Book(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=20, default='N/A')  
    quantity = models.IntegerField(default=1)


class IssueBook(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
