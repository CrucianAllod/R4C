from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from robots.forms import RobotForm
from robots.models import Robot


def register_robot(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = RobotForm(request.POST)

        if form.is_valid():
            model = form.cleaned_data['model']
            version = form.cleaned_data['version']
            created = form.cleaned_data['created']

            serial = f'{model}-{version}'

            robot = Robot(serial=serial, model=model, version=version, created=created)
            robot.save()

            return redirect('success')
    else:
        form = RobotForm()

    return render(request, 'robots/register_robot.html', {'form':form })

def success(request: HttpRequest) -> HttpResponse:
    return render(request, 'robots/success.html')