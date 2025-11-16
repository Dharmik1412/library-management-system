from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Book, Student, IssueBook

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if username == 'admin' and password == 'admin123':
            request.session['is_admin'] = True
            request.session['is_student'] = False
            return redirect('admin_dashboard')

        student = Student.objects.filter(enrollment=username).first()
        if student and student.user.check_password(password):
            request.session['is_student'] = True
            request.session['is_admin'] = False
            request.session['student_username'] = student.user.username
            return redirect('student_dashboard')

        messages.error(request, "Invalid username or password")
        return redirect('login')
    
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        enrollment = request.POST.get('enrollment')
        branch = request.POST.get('branch')

        user = User.objects.create_user(username=username, password=password)
        Student.objects.create(user=user, enrollment=enrollment, branch=branch)
        messages.success(request, "Signup successful! Please login.")
        return redirect('login')
    return render(request, 'signup.html')

def admin_dashboard(request):
    if not request.session.get('is_admin'):
        return redirect('login')

    books = Book.objects.all()
    students = Student.objects.all()
    return render(request, 'admin_dashboard.html', {'books': books, 'students': students})

def student_dashboard(request):
    if not request.session.get('is_student'):
        return redirect('login')

    books = Book.objects.all()
    student_username = request.session.get('student_username', 'Student')

    return render(request, 'student_dashboard.html', {
        'books': books,
        'student_username': student_username
    })


def add_book(request):
    if not request.session.get('is_admin'):
        return redirect('login')

    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        isbn = request.POST.get('isbn')
        quantity = request.POST.get('quantity')
        Book.objects.create(title=title, author=author, isbn=isbn, quantity=quantity)
        messages.success(request, "Book added successfully!")
        return redirect('admin_dashboard')

    return render(request, 'add_book.html')

def add_student(request):
    if not request.session.get('is_admin'):
        return redirect('login')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        enrollment = request.POST.get('enrollment')
        branch = request.POST.get('branch')

        user = User.objects.create_user(username=username, password=password)
        Student.objects.create(user=user, enrollment=enrollment, branch=branch)
        messages.success(request, "Student added successfully!")
        return redirect('admin_dashboard')

    return render(request, 'add_student.html')

def issue_book(request):
    if not request.session.get('is_admin'):
        return redirect('login')

    students = Student.objects.all()
    books = Book.objects.all()

    if request.method == 'POST':
        student_id = request.POST.get('student')
        book_id = request.POST.get('book')
        student = Student.objects.get(id=student_id)
        book = Book.objects.get(id=book_id)
        IssueBook.objects.create(student=student, book=book)
        messages.success(request, "Book issued successfully!")
        return redirect('admin_dashboard')

    return render(request, 'issue_book.html', {'students': students, 'books': books})

def logout_view(request):
    request.session.flush()
    return redirect('login')
