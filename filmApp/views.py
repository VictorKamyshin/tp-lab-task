from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the filmApp index.")


def test(request):
    return render(request, 'main-page.html', { })
