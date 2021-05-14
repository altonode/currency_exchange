from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from currency_exchange.converter.models import Currency


class ConverterView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        # Create proxy object for the template context
        context = super(ConverterView, self).get_context_data(**kwargs)
        context['currencies'] = Currency.objects.all()
        return context


converter_view = ConverterView.as_view()
