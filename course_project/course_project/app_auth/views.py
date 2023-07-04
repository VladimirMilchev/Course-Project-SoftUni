from django.shortcuts import render

from course_project.app_auth.forms import RegistrationForm


def index(request):
    context = {'form': RegistrationForm()}
    return render(request, 'base.html', context=context)


def register_page(request):
    context = {
        "form": RegistrationForm()
    }
    return render(request, 'register-page.html', context=context)
