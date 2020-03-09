from django.shortcuts import render
from main.forms import LectureForm, CourseForm, QuestionForm, CommentForm, ReplyForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from main.models import Course, Lecture, Question, Reply, Comment, Tutor, Student, Upvote, Enrollment


# DISPLAY VIEWS


def index(request):
    context_dict = {'message': 'Message sent from the view'}
    return render(request, 'main/index-mainpage.html', context=context_dict)


def user_profile_page(request):
    return render(request)


def show_course(request, selected_course):
    context_dict = {}

    try:
        course = Course.objects.get(selected_course)
        context_dict['course'] = course

    except Course.DoesNotExist:
        context_dict['course'] = None

    return render(request, context=context_dict)


def show_question(request, selected_question):
    context_dict = {}

    try:
        question = Question.objects.get(selected_question)
        context_dict['question'] = question

    except Question.DoesNotExist:
        context_dict['question'] = None

    return render(request, context=context_dict)


def show_lecture(request, selected_lecture):
    context_dict = {}

    try:
        lecture = Lecture.objects.get(selected_lecture)
        context_dict['lecture'] = lecture

    except Lecture.DoesNotExist:
        context_dict['lecture'] = None

    return render(request, context=context_dict)


def show_comment(request, selected_comment):
    context_dict = {}

    try:
        comment = Comment.objects.get(selected_comment)
        context_dict['comment'] = comment

    except Comment.DoesNotExist:
        context_dict['comment'] = None

    return render(request, context=context_dict)


def contact_page(request):
    return


def profile(request):
    return render(request, 'registration/profiles.html')


# CREATION VIEWS


def create_course(request):
    form = CourseForm()

    # If user inputs comment
    if request.method == 'POST':
        form = CourseForm(request.POST)
        # If input is valid
        if form.is_valid():
            # Save the form
            form.save(commit=True)

            return # Needs redirect

        else:

            print(form.errors)


def create_lecture(request):
    form = LectureForm()

    # If user inputs comment
    if request.method == 'POST':
        form = LectureForm(request.POST)
        # If input is valid
        if form.is_valid():
            # Save the form
            form.save(commit=True)

            return # Needs redirect

        else:

            print(form.errors)


def create_reply(request):
    form = ReplyForm()

    # If user inputs comment
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        # If input is valid
        if form.is_valid():
            # Save the form
            form.save(commit=True)

            return # Needs redirect

        else:

            print(form.errors)


def create_comment(request):
    form = CommentForm()

    # If user inputs comment
    if request.method == 'POST':
        form = CommentForm(request.POST)
        # If input is valid
        if form.is_valid():
            # Save the form
            form.save(commit=True)

            return # Needs redirect

        else:

            print(form.errors)


def user_login(request):
    # If request is HTTP POST, get relevant data
    if request.method == 'POST':
        # Get username and password
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if username/password combination is valid
        user = authenticate(username=username, password=password)

        # If authentication passed check if the account is active
        if user:
            if user.is_active:
                # If account has not been disabled
                login(request, user)
            else:
                return HttpResponse("Your account has been disabled, please contact a system administrator")
        else:
            return HttpResponse("Invalid login details, please try again!")
    else:
        return render(request,)

