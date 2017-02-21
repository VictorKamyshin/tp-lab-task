from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseBadRequest
from models import Film, Appraisal, Profile, Comment, User
from django.db.models import Avg
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from forms import RegistrationForm, EditProfileForm, AuthorisationForm, CreateFilmForm, FilmCommentForm, FilmVoteForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate as dj_authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout
import json
from django.db.models import Count
# Create your views here.


def test(request):
    response = "all film appraisal cleared "
    films = Film.objects.all()
    for film in films:
        rating = Appraisal.customManager.film_appraisal(film.id).aggregate(Avg('value'))
        film.count_of_comments = Comment.customManager.filter(film=film).count()
        if rating.get('value__avg') is None:
            film.rating = 0
        else:
            film.rating = rating.get('value__avg')
        print film.rating
        film.save()
    return HttpResponse(response)


def api_film_card(request):
    if request.method:
        param = request.GET.get('film_id')
        try:
            film_id = int(param)
        except:
            return HttpResponseBadRequest("Id is not a number")
        film = Film.objects.get(id=film_id)
        appraisals = Appraisal.customManager.film_appraisal(film_id)
        appraisals_json = []
        for appraisal in appraisals:
            appraisals_json.append(appraisal.json_format())
        film_json = film.json_format()
        return HttpResponse(json.dumps({'film': film_json, 'appraisals': appraisals_json}, 2),
                            content_type='application/json')
    else:
        return HttpResponseBadRequest("Method not supported")


def api_film_list(request):
    if request.method == 'GET':
        sort = request.GET.get('sort_by')
        if (sort is None) or (sort not in ['rating', 'popularity', 'date', 'title']):
            return HttpResponseBadRequest('unexpected sort type')
        order = request.GET.get('order')
        if (order is None) or (order not in ['asc', 'desc']):
            order = 'asc'
        films = []
        if sort == 'rating':
            if order == 'asc':
                films = list(Film.objects.all().order_by('rating'))
            else:
                films = list(Film.objects.all().order_by('-rating'))
        if sort == 'popularity':
            if order == 'asc':
                films = list(Film.objects.all().order_by('count_of_comments'))
            else:
                films = list(Film.objects.all().order_by('-count_of_comments'))
        if sort == 'date':
            if order == 'asc':
                films = list(Film.objects.all().order_by('date_of_addition'))
            else:
                films = list(Film.objects.all().order_by('-date_of_addition'))
        if sort == 'title':
            if order == 'asc':
                films = list(Film.objects.all().order_by('title'))
            else:
                films = list(Film.objects.all().order_by('-title'))
        json_films = []
        for film in films:
            json_films.append(film.json_format())
        return HttpResponse(json.dumps(json_films, 2), content_type='application/json')
    else:
        return HttpResponseBadRequest("Method not supported")


def main_page(request):
    if request.method == 'GET':
        sort = request.GET.get('sort')
        if (sort is None) or (sort not in ['rating', 'popularity', 'date', 'title']):
            sort = 'title'
        films = []
        if sort == 'rating':
            films = list(Film.objects.all().order_by('rating'))
        if sort == 'popularity':
            films = list(Film.objects.all().order_by('count_of_comments'))
        if sort == 'date':
            films = list(Film.objects.all().order_by('date_of_addition'))
        if sort == 'title':
            films = list(Film.objects.all().order_by('title'))
        films = paginate(films, request)
        last_comments = Comment.customManager.get_last()
        user = request.user.username
        return render(request, 'main-page.html', {'films': films, 'last_comments': last_comments, 'username': user})
    else:
        return HttpResponse('Method does not allowed')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/main/')


def film_card_page(request):
    param = request.GET.get('film_id')
    try:
        film_id = int(param)
    except:
        return HttpResponse("Not a number")
    film_card = Film.objects.get(id=film_id)
    if film_card is None:
        return HttpResponse("There are no such film")
    comments = Comment.customManager.filter(film_id=film_card.id).order_by('material_path')
    for comment in comments:
        print comment.material_path
    user = request.user.username
    last_comments = Comment.customManager.get_last()
    appraisal_distr = get_appraisal_distr(film_id)
    comment_form = FilmCommentForm
    film_vote_form = FilmVoteForm
    return render(request, 'film-card.html', {'film_card': film_card, 'comments': comments,
                                              'last_comments': last_comments, 'comment_form': comment_form,
                                              'film_vote': film_vote_form, 'username': user,
                                              'appraisals_distr': appraisal_distr})


def registration_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            name = form.cleaned_data.get('name')
            surname = form.cleaned_data.get('surname')
            patronymic = form.cleaned_data.get('patronymic')
            password = form.cleaned_data.get('password1')
            avatar = form.cleaned_data.get('avatar')
            user = User.objects.create_user(username=username, email=email, password=password)
            Profile.objects.create(user=user, email=email, name=name, surname=surname, patronymic=patronymic,
                                   avatar=avatar)
            return HttpResponseRedirect('/main/')
    else:
        form = RegistrationForm
        user = request.user.username
    last_comments = Comment.customManager.get_last()
    return render(request, 'registration.html', {'last_comments': last_comments, 'form': form, 'username': user})


def profile_page(request):
    last_comments = generate_last_comments()
    form = EditProfileForm
    user = request.user.username
    return render(request, 'profile.html', {'last_comments':last_comments,'form':form,'username':user})


def authorisation_page(request):
    if request.method == 'POST':
        form = AuthorisationForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = dj_authenticate(username = username, password = password)
            if user:
                auth_login(request, user)
                return HttpResponseRedirect('/main/')
    else:
        form = AuthorisationForm
    last_comments = generate_last_comments()
    return render(request, 'authorisation.html', {'last_comments': last_comments, 'form':form})


def create_edit_film(request):
    if request.method == 'POST':
        form = CreateFilmForm(request.POST)
        if form.is_valid():
            title = request.POST.get('title', '')
            producer = request.POST.get('producer', '')
            country = request.POST.get('country', '')
            description = request.POST.get('description', '')
            premiere = request.POST.get('premiere', '')
            film = Film.objects.create(title=title, producer=producer, country=country, description=description,
                                       premiere=premiere)
            return HttpResponseRedirect('/main/')
    else:
        form = CreateFilmForm
    last_comments = Comment.customManager.get_last()
    user = request.user.username
    return render(request, 'create-edit-film.html', {'last_comments':last_comments,'form':form,'username':user})


def film_card_appraisal(request):
    if request.method == 'POST':
        value = request.POST.get('appraisal')
        film_id = request.POST.get('film_id')
        user = request.user
        film = Film.objects.get(id=film_id)
        try:
            appraisal = Appraisal.customManager.get(author__user=user, film__id=film_id)
            print appraisal.value
            appraisal.value = value
            appraisal.save()
        except:
            print 'Appraisal didnt exist'
            author = Profile.objects.get(user = user)
            Appraisal.customManager.create(value = value, author = author, film = film)

        rating = Appraisal.customManager.film_appraisal(film_id).aggregate(Avg('value'))
        film.rating = rating.get('value__avg')
        film.save()
        return HttpResponse(json.dumps({'text':'Got your appraisal', 'rating': film.rating}), content_type='application/json')
    return HttpResponseBadRequest('Method not supported')


def film_comment(request):
    if request.method == 'POST':
        film_id = request.POST.get('film_id')
        comment_id = request.POST.get('commented_comment_id')
        print comment_id
        print film_id
        text = request.POST.get('text')
        film = Film.objects.get(id=film_id)
        print type(comment_id)
        if comment_id is not None:
            if comment_id.isdigit():
                parent_comment = Comment.customManager.get(id = comment_id)
            else:
                return HttpResponseBadRequest('Wrong parent id format')
        else:
            parent_comment = None
        author = Profile.objects.get(user = request.user)
        comment = Comment.customManager.create_comment(text=text, author=author, parent=parent_comment, film=film)
        return HttpResponse(json.dumps({'text': 'Hello!', 'level': comment.level,
                                        'reverse_level': 12 - comment.level, 'comment_id': comment.id,
                                        'username':request.user.username}), content_type='application/json')
    else:
        return HttpResponseBadRequest('Unsupported request method')


def get_appraisal_distr(film_id):
    existing_appraisal_distr = Appraisal.customManager.filter(film__id=film_id).values('value')\
        .annotate(value_count=Count('value'))
    appraisal_distr = []
    j = 0
    for i in xrange(0,11):
        if j < len(existing_appraisal_distr):
            if existing_appraisal_distr[j].get('value') == i:
                appraisal_distr.append({'value':i,'count':existing_appraisal_distr[j].get('value_count')})
                j+=1
            else:
                appraisal_distr.append({'value':i,'count':0})
        else:
            appraisal_distr.append({'value':i,'count':0})
    return appraisal_distr


def generate_last_comments():
    comments = []
    for i in xrange(0,4):
        comments.append({'film_title':u'Commented film title' + str(i),'text_part':u'Part of comment...'})
    return comments


def generate_comment(count):
    comments = []
    for i in xrange(0, count):
        comments.append({'username':u'username' + str(i),
                         'text':u'Lorem ipsum dolor sit amet , consectetur adipiscing elit. Ut posuere quam eget arcu '
                                u'venenatis, in suscipit neque finibus. Nulla facilisi. Aenean et nisl vitae lectus '
                                u'ultrices placerat. Praesent eu auctor ligula. Praesent posuere nec nunc at rutrum. '
                                u'Suspendisse potenti. Morbi eu elementum dui. Phasellus aliquet euismod libero vitae '
                                u'vestibulum. Nunc et maximus est. Nulla facilisi.', 'level':i, 'reverse_level': 12 - i})
    return comments


def generate_films(count):
    films = []
    for i in xrange(0, count ):
        films.append({'rating': 5+i, 'count_of_comments': 2+i, 'title': u'AWESOME FILM ' + str(i),
                      'description':u'Lorem ipsum dolor sit amet , consectetur adipiscing elit. Ut posuere quam eget '
                                    u'arcu venenatis, in suscipit neque finibus. Nulla facilisi. Aenean et nisl vitae '
                                    u'lectus ultrices placerat. Praesent eu auctor ligula. Praesent posuere nec nunc at '
                                    u'rutrum. Suspendisse potenti. Morbi eu elementum dui. Phasellus aliquet euismod '
                                    u'libero vitae vestibulum. Nunc et maximus est. Nulla facilisi. ' + str(i)})
    return films


def paginate(object_list, request):
    paginator = Paginator(object_list, 2)  # Show 2 contacts per page

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return contacts