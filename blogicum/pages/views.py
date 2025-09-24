from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseServerError, HttpResponseNotFound, HttpResponseForbidden


def about(request):
    return render(request, 'pages/about.html')


def rules(request):
    return render(request, 'pages/rules.html')


def page_not_found(request, exception):
    return HttpResponseNotFound(render(request, 'pages/404.html'))


def server_error(request):
    return HttpResponseServerError(render(request, 'pages/500.html'))


def csrf_failure(request, reason=""):
    return HttpResponseForbidden(render(request, 'pages/403csrf.html'))