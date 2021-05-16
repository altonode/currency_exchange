from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from .models import Currency
from .forms import ConverterForm
from .converter import ConverterMixin


class ConverterView(ConverterMixin, TemplateView, FormView):
    template_name = 'pages/home.html'
    form_class = ConverterForm

    def get_context_data(self, **kwargs):
        # Add a list of all currencies to render
        kwargs['currencies'] = Currency.objects.all()
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return kwargs

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        return self.render_converter_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


converter_view = ConverterView.as_view()
