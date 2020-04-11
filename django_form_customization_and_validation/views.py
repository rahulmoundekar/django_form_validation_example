from django.shortcuts import render
from django.contrib import messages

from django_form_customization_and_validation.forms import StudentForm


def indexView(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            messages.success(request, 'The form is valid.')
        else:
            messages.error(request, 'The form is invalid.')

        return render(request, 'index.html', {'form': form})

    else:
        form = StudentForm()
        return render(request, 'index.html', {'form': form})
