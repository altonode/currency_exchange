from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from .models import Currency
from .forms import ConverterForm


class ConverterView(TemplateView,FormView):
    template_name = 'pages/home.html'
    form_class = ConverterForm

    def get_context_data(self, **kwargs):
        # Create proxy object for the template context
        context = super(ConverterView, self).get_context_data(**kwargs)
        context['currencies'] = Currency.objects.all()
        if 'form' not in context:
            context['form'] = self.get_form()
        return context


converter_view = ConverterView.as_view()
