from datetime import timedelta
from io import BytesIO

from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from robots.forms import RobotForm
from robots.models import Robot

import pandas as pd


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

def summary_robots(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':

        end_date = timezone.now()
        start_date = end_date - timedelta(days=30)

        robots = (
            Robot.objects.filter(created__range=(start_date, end_date))
            .values('model', 'version')
            .annotate(count=Count('id'))
        )

        model_dataframes = {}

        for robot in robots:
            print(robot)
            model = robot['model']
            version = robot['version']
            count = robot['count']

            if model not in model_dataframes:
                model_dataframes[model] = {
                    'Модель': [],
                    'Версия': [],
                    'Количество за неделю': []
                }

            model_dataframes[model]['Модель'].append(model)
            model_dataframes[model]['Версия'].append(version)
            model_dataframes[model]['Количество за неделю'].append(count)

        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            for model, data in model_dataframes.items():
                df = pd.DataFrame(data)
                df.to_excel(writer, sheet_name=model,  index=False, engine='openpyxl')

        output.seek(0)

        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="robots_summary.xlsx"'

        return response

def success(request: HttpRequest) -> HttpResponse:
    return render(request, 'robots/success.html')