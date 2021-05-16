from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.shortcuts import render, redirect

from currency_exchange.users.models import UserProfile
from currency_exchange.users.forms import UserProfileForm


User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    fields = ["username"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()

@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')

    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm(
        {'picture': userprofile.picture, 'preferred_currency': userprofile.preferred_currency})

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('users:profile', user.username)
        else:
            print(form.errors)
    return render(request, 'pages/profile.html',
                  {'userprofile': userprofile, user: 'user', 'username': username, 'form': form})


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = UserProfile
    fields = ["picture", "preferred_currency"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        return reverse('users:profile',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        return self.request.user


profile_update_view = ProfileUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class RegisterProfile(FormView):
    form_class = UserProfileForm
    template_name = "users/profile_registration.html"

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.username = request.user
            user_profile.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        username = self.request.user.username
        self.success_url = "/users/{}/".format(username)
        if self.success_url:
            url = self.success_url
        else:
            raise improperlyConfigured(
                "No URL to redirect to. Provide a success URL"
                )
        return url


register_profile = RegisterProfile.as_view()


@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')

    userprofile = UserProfile.objects.get_or_create(username=user)[0]
    form = UserProfileForm(
        {'username': userprofile.username, 'picture': userprofile.picture,
         'preferred_currency': userprofile.preferred_currency})

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('users:profile', user.username)
        else:
            print(form.errors)
    return render(request, 'pages/profile.html',
                  {'userprofile': userprofile, 'user': user, 'form': form,})
