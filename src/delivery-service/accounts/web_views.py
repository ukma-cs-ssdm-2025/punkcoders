from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import CustomAuthenticationForm, CustomUserCreationForm


def register_view(request):
    """
    Handles user registration.
    """
    if request.user.is_authenticated:
        return redirect("dish_list")

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # This saves the user with the default 'CUSTOMER' role
            login(request, user)  # Log them in immediately
            messages.success(request, "Registration successful.")
            return redirect("restaurant:dish_list")  # Redirect to your main dish list page
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = CustomUserCreationForm()

    return render(request, "register.html", {"form": form})


def login_view(request):
    """
    Handles user login.
    """
    if request.user.is_authenticated:
        return redirect("dish_list")

    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)  # This creates the session!
                messages.info(request, f"You are now logged in as {username}.")

                # Redirect managers to a special dashboard, others to home
                if user.role == "MANAGER":
                    # We'll create this 'manager_dashboard' URL soon
                    return redirect("manager_dashboard")
                else:
                    return redirect("restaurant:dish_list")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    form = CustomAuthenticationForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    """
    Handles user logout.
    """
    logout(request)  # This clears the session
    messages.info(request, "You have successfully logged out.")
    return redirect("restaurant:dish_list")  # Redirect to home
