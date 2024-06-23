from django.shortcuts import redirect, render
from userauths.forms import UserRegisterForm, ProfileForm, UserUpdateForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings
from userauths.models import Profile, User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

# User = settings.AUTH_USER_MODEL


def register_view(request):

    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            print(new_user)
            full_name = form.cleaned_data.get("full_name")
            messages.success(
                request, f"{full_name}, ваш  аккаунт було успішно створенно."
            )
            new_user = authenticate(
                username=form.cleaned_data["telephone"],
                password=form.cleaned_data["password1"],
            )
            login(request, new_user)
            return redirect("core:index")
    else:
        form = UserRegisterForm()

    context = {
        "form": form,
    }
    return render(request, "userauths/sign-up.html", context)


def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, f"Ви вже увійшли в обліковий запис!")
        return redirect("core:index")

    if request.method == "POST":
        telephone = request.POST.get("telephone")  # peanuts@gmail.com
        password = request.POST.get("password")  # getmepeanuts

        try:
            user = User.objects.get(telephone=telephone)
            user = authenticate(request, telephone=telephone, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Ви  увійшли в особистий обліковий запис!")
                return redirect("core:index")
            else:
                messages.warning(
                    request, "Користувача не існує, створіть обліковий запис."
                )

        except:
            messages.warning(request, f"Користувача з {telephone} не існує")

    return render(request, "userauths/sign-in.html")


def logout_view(request):

    logout(request)
    messages.success(request, "Ви вийшли з облікового запису!")
    return redirect("userauths:sign-in")


def profile_update(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            messages.success(request, "Профіль було успішно оновленно!")
            return redirect("core:dashboard")
    else:
        form = ProfileForm(instance=profile)

    context = {
        "form": form,
        "profile": profile,
    }

    return render(request, "userauths/profile-edit.html", context)


@login_required
def update_account_details(request):
    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "Нові паролі не співпадають.")
        elif not request.user.check_password(current_password):
            messages.error(request, "Наданий існуючий пароль не вірний.")
        else:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, "Пароль успішно оновленно.")

    return redirect("core:dashboard")
