from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from datetime import datetime
from home.models import Contact, Diet
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect

# Main page view with authentication check
@login_required(login_url='login')  # Redirect to login if not authenticated
@require_http_methods(["GET"])  # Allow only GET requests
def index(request):
    return render(request, 'index.html')

# Contact form view
@csrf_protect  # CSRF protection for POST requests
@require_http_methods(["GET", "POST"])  # Allow only GET and POST methods
def contact(request):
    if request.method == "POST":
        # Validate input data
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        queries = request.POST.get('queries', '').strip()

        if not name or not email or not phone or not queries:
            messages.error(request, "All fields are required.")
            return render(request, 'contact.html')

        try:
            contact = Contact(name=name, email=email, phone=phone, queries=queries, date=datetime.today())
            contact.save()
            messages.success(request, "Your form has been submitted successfully.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return render(request, 'contact.html')

    return render(request, 'contact.html')

# Login view
@csrf_protect
@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')  # Redirect to main page after login
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

# Registration view
@csrf_protect
@require_http_methods(["GET", "POST"])
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        password_confirm = request.POST.get('password_confirm', '').strip()

        if password == password_confirm:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email is already registered")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, "Registration successful! You can now log in.")
                return redirect('login')
        else:
            messages.error(request, "Passwords do not match")
    return render(request, 'register.html')

# Logout view
@require_http_methods(["GET"])
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')

# View a specific diet
@login_required(login_url='login')
@require_http_methods(["GET"])
def view_diet(request, diet_id):
    diet = get_object_or_404(Diet, id=diet_id)
    return render(request, 'view_diet.html', {'diet': diet})

# Edit a specific diet
@login_required(login_url='login')
@csrf_protect
@require_http_methods(["GET", "POST"])
def edit_diet(request, diet_id):
    diet = get_object_or_404(Diet, id=diet_id)

    if request.method == 'POST':
        diet.name = request.POST.get('name', '').strip()
        diet.description = request.POST.get('description', '').strip()
        diet.category = request.POST.get('category', '').strip()
        diet.calories = request.POST.get('calories', '').strip()
        diet.save()

        messages.success(request, "Diet updated successfully!")
        return redirect('view_diet', diet_id=diet.id)

    return render(request, 'edit_diet.html', {'diet': diet})

# Delete a specific diet
@login_required(login_url='login')
@csrf_protect
@require_http_methods(["POST"])  # Only allow POST requests for delete
def delete_diet(request, diet_id):
    if diet_id == 1:
        messages.error(request, "Diet with ID 1 cannot be deleted.")
        return redirect('main')

    diet = get_object_or_404(Diet, id=diet_id)
    diet.delete()
    messages.success(request, "Diet deleted successfully!")
    return redirect('main')
