from django.shortcuts import render
from django.http import (
    HttpResponseServerError, HttpResponseNotFound, HttpResponseForbidden)
from django.views.generic import TemplateView


class AboutView(TemplateView):
    template_name = 'pages/about.html'


class RulesView(TemplateView):
    template_name = 'pages/rules.html'


def page_not_found(request, exception):
    return HttpResponseNotFound(render(request, 'pages/404.html'))


def server_error(request):
    return HttpResponseServerError(render(request, 'pages/500.html'))


def csrf_failure(request, reason=""):
    return HttpResponseForbidden(render(request, 'pages/403csrf.html'))
