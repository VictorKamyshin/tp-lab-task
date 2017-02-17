from django.shortcuts import render
from django.http import HttpResponse
from models import Film
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the filmApp index.")


def main_page(request):
    films = generate_films(2)
    return render(request, 'main-page.html', {'films':films})


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
    return render(request, 'film-card.html',{'film_card': film_card, 'comments':comments})


def registration_page(request):
    return render(request, 'registration.html')


def authorisation_page(request):
    return render(request, 'authorisation.html')

def create_edit_film_page(request):
    return render(request, 'create-edit-film.html')



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