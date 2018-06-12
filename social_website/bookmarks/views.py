from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm


# Create your views here.
def user_login(request):
    if request.method == "GET":
        form = LoginForm()
        error = request.session.get("error", False)
        msg = request.session.get("msg", "")
        if error:
            del request.session["error"]
            del request.session["msg"]
        return render(request, 'login.html', {'form': form, 'error': error, 'msg': msg})
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = authenticate(username=cleaned_data["username"],
                                password=cleaned_data["password"])
            if user:
                if user.is_active:
                    login(request, user)
                    request.session["user"] = cleaned_data["username"]
                    return HttpResponseRedirect("/bookmarks/dashboard/")
                else:
                    msg = "Your account has been disabled. Please contact support."
                    request.session["error"] = True
                    request.session["msg"] = msg
                    return HttpResponseRedirect("/bookmarks/")
            else:
                msg = "Invalid Log-in."
                request.session["error"] = True
                request.session["msg"] = msg
                return HttpResponseRedirect("/bookmarks/")
        else:
            msg = "Invalid Log-in."
            request.session["error"] = True
            request.session["msg"] = msg
            return HttpResponseRedirect("/bookmarks/")


@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request,
                          'registration/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        return render(request,
                      'registration/register.html',
                      {'user_form': user_form})
