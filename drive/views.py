from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponseForbidden
from .models import UploadedFile
from .forms import FileUploadForm

# check if user is admin
def is_admin(user):
    return user.is_superuser

# signup view
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# user dashboard
@login_required
def dashboard(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded = form.save(commit=False)
            uploaded.user = request.user
            uploaded.save()
            return redirect('dashboard')
    else:
        form = FileUploadForm()
    files = UploadedFile.objects.filter(user=request.user).order_by('-uploaded_at')
    return render(request, 'drive/dashboard.html', {'form': form, 'files': files})

# delete file
@login_required
def delete_file(request, file_id):
    file_obj = get_object_or_404(UploadedFile, pk=file_id)
    if file_obj.user != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to delete this file.")
    file_obj.file.delete(save=False)
    file_obj.delete()
    return redirect('dashboard')

# admin dashboard
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    files = UploadedFile.objects.all().order_by('-uploaded_at')
    return render(request, 'drive/admin_dashboard.html', {'files': files})
