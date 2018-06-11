from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm


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


def dashboard(request):
    user = request.session.get("user", False)
    return render(request, 'dashboard.html', {'user': user})
