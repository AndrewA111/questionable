from django.shortcuts import redirect, render
from main.forms import LectureForm, CourseForm, QuestionForm, CommentForm, ReplyForm, UserForm, ProfileForm, ForumForm, \
    PostForm
from main.models import Course, Lecture, Question, Reply, Comment, Upvote, Enrollment, Post, Student, Tutor, Forum
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from django.views import View

# Sandbox views


# test for ajax, should receive a parameter, double it and return it
class DoubleResponseView(View):

    def get(self, request):
        info_id = request.GET['info_id']

        return HttpResponse(info_id*5)

# DISPLAY VIEWS


def index(request):
    context_dict = {'message': 'Message sent from the view'}
    return render(request, 'main/index.html', context=context_dict)


def show_courses(request):
    context_dict = {}
    courses = Course.objects.all()
    context_dict['courses'] = courses
    return render(request, 'main/courses.html', context=context_dict)


def show_course(request):
    context_dict = {}

    try:
        course = Course.objects.get(request.course)
        lecture_list = Lecture.objects.filter(course=course)
        forum_list = Forum.objects.filter(course=course)
        context_dict['course'] = course
        context_dict['lectures'] = lecture_list
        context_dict['forums'] = forum_list

    except Course.DoesNotExist:
        context_dict['course'] = None
        context_dict['lectures'] = None
        context_dict['forums'] = None
    return render(request, 'main/course.html', context=context_dict)


# @login_required
# @permission_required('main.view_lecture')
# def show_lectures(request):
#     context_dict = {}
#     lectures = Lecture.objects.all()
#     context_dict['lectures'] = lectures
#
#     return render(request, 'main/lectures.html', context=context_dict)


def show_lecture(request):
    context_dict = {}

    try:
        lecture = Lecture.objects.get(request.lecture)
        question_list = Question.objects.filter(lecture=lecture)
        context_dict['lecture'] = lecture
        context_dict['questions'] = question_list

    except Lecture.DoesNotExist:
        context_dict['lecture'] = None
        context_dict['questions'] = None
    return render(request, 'main/course/lecture.html', context=context_dict)


def show_question(request):
    context_dict = {}

    try:
        question = request.question
        reply_list = Reply.objects.filter(question=question)
        upvotes = Upvote.objects.filter(question=question)
        context_dict['question'] = question
        context_dict['replies'] = reply_list
        context_dict['upvotes'] = upvotes

    except Question.DoesNotExist:
        context_dict['question'] = None
        context_dict['replies'] = None
        context_dict['upvotes'] = None

    return render(request, 'main/course/lecture/question.html', context=context_dict)


# def show_reply(request):
#     context_dict = {}
#
#     try:
#         reply = request.reply
#         context_dict['reply'] = reply
#
#     except Reply.DoesNotExist:
#         context_dict['reply'] = None
#
#     return render(request, 'main/course/lecture/question/reply.html', context=context_dict)


def show_forum(request):
    context_dict = {}
    try:
        forum = request.forum
        post_list = Post.objects.filter(forum=forum)
        context_dict['forum'] = forum
        context_dict['posts'] = post_list
    except Forum.DoesNotExist:
        context_dict['forum'] = None
        context_dict['posts'] = None
    return render(request, 'main/course/forum.html', context=context_dict)


def show_post(request):
    context_dict = {}

    try:
        question = request.question
        comment_list = Reply.objects.filter(question=question)
        upvotes = Upvote.objects.filter(question=question)
        context_dict['forum'] = question
        context_dict['comments'] = comment_list
        context_dict['upvotes'] = upvotes

    except Post.DoesNotExist:
        context_dict['forum'] = None
        context_dict['comments'] = None
        context_dict['upvotes'] = None

    return render(request, 'main/course/forum/post.html', context=context_dict)


# def show_comment(request):
#     context_dict = {}
#
#     try:
#         comment = request.comment
#         context_dict['comment'] = comment
#
#     except Comment.DoesNotExist:
#         context_dict['comment'] = None
#
#     return render(request, 'main/course/lecture/question/comment.html', context=context_dict)

def contact_page(request):
    return render(request, 'main/contact_page.html')

# View to generate profile page for logged in user (requires login)
@login_required(login_url='/accounts/login/')
def profile(request):

    current_user = request.user
    check_user(current_user)
    # context_dict = {}
    
    # try:
    #     student = Student.objects.get(user=current_user)
    #     questions = Question.objects.filter(user=student)
    #     posts = Post.objects.filter(user=student)
    #     context_dict['questions'] = questions
    #     context_dict['student'] = True
    #     context_dict['posts'] = posts

    # except:
    #     context_dict = {}

    return render(request, 'main/profile.html')


# CREATION VIEWS


@login_required
def create_course(request):
    form = CourseForm()

    # If user inputs comment
    if request.method == 'POST':
        form = CourseForm(request.POST)
        # If input is valid
        if form.is_valid():
            # Save the form
            form.save(commit=True)
            return redirect('/main/courses')

        else:

            print(form.errors)

    return render(request, 'main/courses/', {'form': form})


@login_required
def create_lecture(request):
    form = LectureForm()

    # If user inputs comment
    if request.method == 'POST':
        form = LectureForm(request.POST)
        # If input is valid
        if form.is_valid():
            # Save the form
            lecture = form.save(commit=True)
            lecture.course = request.course

            return redirect('/main/course')

        else:

            print(form.errors)

    return render(request, 'main/course/', {'form': form})


@login_required
def create_question(request):
    form = QuestionForm()

    # If user inputs comment
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        # If input is valid
        if form.is_valid():
            # Save the form
            question = form.save(commit=True)
            question.lecture = request.lecture
            question.user = request.user

            return redirect('/main/course/lecture')

        else:

            print(form.errors)

    return render(request, 'main/course/lecture/', {'form': form})


@login_required
def create_reply(request):
    form = ReplyForm()

    # If user inputs comment
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        # If input is valid
        if form.is_valid():
            # Save the form
            reply = form.save(commit=True)
            reply.user = request.user
            reply.question = request.question
            return redirect('/main/course/lecture/question')

        else:

            print(form.errors)

    return render(request, 'main/course/lecture/question/', {'form': form})


@login_required
def create_forum(request):
    form = ForumForm()

    # If user inputs comment
    if request.method == 'POST':
        form = ForumForm(request.POST)
        # If input is valid
        if form.is_valid():
            # Save the form
            forum = form.save(commit=True)
            forum.course = request.course

            return redirect('/main/course')

        else:

            print(form.errors)

    return render(request, 'main/course/', {'form': form})


@login_required
def create_post(request):
    form = PostForm()

    # If user inputs comment
    if request.method == 'POST':
        form = PostForm(request.POST)
        # If input is valid
        if form.is_valid():
            # Save the form
            post = form.save(commit=True)
            post.forum = request.forum
            post.user = request.user

            return redirect('/main/course/forum')

        else:

            print(form.errors)

    return render(request, 'main/course/forum/', {'form': form})


@login_required
def create_comment(request):
    form = CommentForm()

    # If user inputs comment
    if request.method == 'POST':
        form = CommentForm(request.POST)
        # If input is valid
        if form.is_valid():
            # Save the form
            comment = form.save(commit=True)
            comment.post = request.post
            comment.user = request.user

            return redirect('/main/course/forum/post')

        else:

            print(form.errors)

    return render(request, 'main/course/forum/post/', {'form': form})


@login_required
def create_upvote(request):

    upvote = None

    # If user upvotes question
    if request.method == 'POST':
        upvote = Upvote()
        upvote.question = request.question
        upvote.user = request.user

    return render(request, 'main/course/lecture/question', {'upvote': upvote})


@login_required
def enroll_user(request):

    enroll = None

    # If user enrolls in course
    if request.method == 'POST':
        enroll = Enrollment()
        enroll.course = request.course
        enroll.user = request.user

    return render(request, 'main/courses', {'enrollment': enroll})

@login_required
@transaction.atomic
def update_user(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was sucessfull updated!'))
        else:
            messages.error(request, ('Please correct the error(s) below:'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'main/update_user.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def check_user(current_user):
    try:
        Student.objects.get(user=current_user)
        print(1)
        return 1
    except:
        try:
            Tutor.objects.get(user=current_user)
            print(2)
            return 2
        except:
            print(-1)
            return -1

    
    