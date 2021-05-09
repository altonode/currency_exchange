from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from django.views.generic.edit import FormView

from currency_exchange.users.forms import UserProfileForm
from currency_exchange.users.models import UserProfile

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = UserProfile
    fields = ["user", "picture"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        return self.request.user.get_absolute_url()  # type: ignore [union-attr]

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class RegisterProfileView(FormView):
    form_class = UserProfileForm
    template_name = "users/profile_registration.html"
    success_url = "/redirect/"

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


register_profile_view = RegisterProfileView.as_view()

@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')

    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm(
        {'currency': userprofile.currency, 'picture': userprofile.picture})

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('users:profile', user.username)
        else:
            print(form.errors)
    return render(request, 'pages/profile.html',
                  {'userprofile': userprofile, 'selecteduser': user, 'form': form})
