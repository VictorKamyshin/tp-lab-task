from django.shortcuts import render
from django.http import HttpResponse
from models import Film, Appraisal, Profile, Comment
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


def test(request):
    response = "appraisals of user1 : "
    film = Film.objects.get(title='AWESOME FILM TITLE')
    profile = Profile.objects.get(name='user1')
    tmp = Appraisal.myManager.user_appraisal_distribution(profile.id)
    for dist in tmp:
        response += (str(dist.get('value'))+' '+str(dist.get('count'))+' ')

    parent_comment = Comment.customManager.get(id=5)

    Comment.customManager.create_comment('Yp! Really awesome!', profile,parent_comment,film)
    return HttpResponse(response)


def main_page(request):
    films = generate_films(2)
    last_comments = generate_last_comments()
    return render(request, 'main-page.html', {'films':films, 'last_comments':last_comments})


def film_card_page(request):
    param = request.GET.get('film_id')
    try:
        film_id = int(param)
    except:
        return HttpResponse("Not a number")
    film_card = {'rating': 5, 'title': u'AWESOME FILM ' + str(film_id),
                 'description':u'Lorem ipsum dolor sit amet , consectetur adipiscing elit. Ut posuere quam eget '
                                    u'arcu venenatis, in suscipit neque finibus. Nulla facilisi. Aenean et nisl vitae '
                                    u'lectus ultrices placerat. Praesent eu auctor ligula. Praesent posuere nec nunc at '
                                    u'rutrum. Suspendisse potenti. Morbi eu elementum dui. Phasellus aliquet euismod '
                                    u'libero vitae vestibulum. Nunc et maximus est. Nulla facilisi. ',
                 'producer' : u'Awesome producer', 'country':u'USA', 'premiere':datetime.now}
    comments = generate_comment(4)
    last_comments = generate_last_comments()
    return render(request, 'film-card.html', {'film_card': film_card, 'comments':comments, 'last_comments':last_comments})


def registration_page(request):
    last_comments = generate_last_comments()
    return render(request, 'registration.html', {'last_comments':last_comments})


def authorisation_page(request):
    last_comments = generate_last_comments()
    return render(request, 'authorisation.html', {'last_comments':last_comments})


def create_edit_film_page(request):
    last_comments = generate_last_comments()
    return render(request, 'create-edit-film.html', {'last_comments':last_comments})


def generate_last_comments():
    comments = []
    for i in xrange(0,4):
        comments.append({'film_title':u'Commented film title' + str(i),'text_part':u'Part of comment...'})
    return comments


def generate_comment(count):
    comments = []
    for i in xrange(0, count) :
        comments.append({'username':u'username' + str(i),
                         'text':u'Lorem ipsum dolor sit amet , consectetur adipiscing elit. Ut posuere quam eget arcu '
                                u'venenatis, in suscipit neque finibus. Nulla facilisi. Aenean et nisl vitae lectus '
                                u'ultrices placerat. Praesent eu auctor ligula. Praesent posuere nec nunc at rutrum. '
                                u'Suspendisse potenti. Morbi eu elementum dui. Phasellus aliquet euismod libero vitae '
                                u'vestibulum. Nunc et maximus est. Nulla facilisi.', 'level':i, 'reverse_level': 12 - i})
    return comments

def generate_films(count):
    films = []
    for i in xrange(0, count ) :
        films.append({'rating': 5+i, 'count_of_comments': 2+i, 'title': u'AWESOME FILM ' + str(i),
                      'description':u'Lorem ipsum dolor sit amet , consectetur adipiscing elit. Ut posuere quam eget '
                                    u'arcu venenatis, in suscipit neque finibus. Nulla facilisi. Aenean et nisl vitae '
                                    u'lectus ultrices placerat. Praesent eu auctor ligula. Praesent posuere nec nunc at '
                                    u'rutrum. Suspendisse potenti. Morbi eu elementum dui. Phasellus aliquet euismod '
                                    u'libero vitae vestibulum. Nunc et maximus est. Nulla facilisi. ' + str(i)})
    return films


def paginate(object_list, request):
    paginator = Paginator(object_list, 2)  # Show 3 contacts per page

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