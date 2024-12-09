from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from datetime import datetime
from home.models import Contact, Diet
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Main page view with authentication check
@login_required(login_url='login')  # Redirect to login if not authenticated
@require_http_methods(["GET"])  # Only allow GET requests
def index(request):
    return render(request, 'index.html')

# Contact form view
@require_http_methods(["GET", "POST"])  # Allow GET and POST requests
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        queries = request.POST.get('queries')
        contact = Contact(name=name, email=email, phone=phone, queries=queries, date=datetime.today())
        contact.save()
        messages.success(request, "Your form is submitted.")
    return render(request, 'contact.html')

# Login view
@require_http_methods(["GET", "POST"])  # Allow GET and POST requests
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('main')  # Redirect to the main page after login
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

# Register view
@require_http_methods(["GET", "POST"])  # Allow GET and POST requests
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        if password == password_confirm:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email is already registered")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, "Registration successful! You can now log in.")
                return redirect('login')  # Redirect to login page after registration
        else:
            messages.error(request, "Passwords do not match")
    return render(request, 'register.html')

# Logout view
@require_http_methods(["POST"])  # Allow POST requests only for logout
def logout_view(request):
    logout(request)  # Logs out the user
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')  # Redirects to the login page after logging out

# View a specific diet
@require_http_methods(["GET"])  # Only allow GET requests
def view_diet(request, diet_id):
    diet = get_object_or_404(Diet, id=diet_id)
    return render(request, 'view_diet.html', {'diet': diet})

# Edit a specific diet
@require_http_methods(["GET", "POST"])  # Allow GET and POST requests
def edit_diet(request, diet_id):
    diet = get_object_or_404(Diet, id=diet_id)
    
    if request.method == 'POST':
        # Update the diet details
        diet.name = request.POST['name']
        diet.description = request.POST['description']
        diet.category = request.POST['category']
        diet.calories = request.POST['calories']
        diet.save()

        messages.success(request, "Diet updated successfully!")
        return redirect('view_diet', diet_id=diet.id)

    return render(request, 'edit_diet.html', {'diet': diet})

# Delete a specific diet
@require_http_methods(["POST"])  # Allow POST requests only for deletion
def delete_diet(request, diet_id):
    # Prevent deleting the diet with ID 1
    if diet_id == 1:
        messages.error(request, "Diet with ID 1 cannot be deleted.")
        return redirect('main')  # Redirect to the main page (or wherever you want)
    # If not diet ID 1, proceed to delete
    diet = get_object_or_404(Diet, id=diet_id)
    diet.delete()
    messages.success(request, "Diet deleted successfully!")
    return redirect('main')
