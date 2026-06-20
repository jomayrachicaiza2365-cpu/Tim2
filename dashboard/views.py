from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_vista(request):
    return render(request, 'private/dashboard.html')
