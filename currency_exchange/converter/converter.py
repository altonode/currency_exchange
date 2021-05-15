from .models import Currency, ConversionRate


class ConverterMixin(object):

    def render_converter_response(self, kwargs, **response_kwargs):
        form = kwargs['form']
        from_currency = form.cleaned_data['currency_from']
        to_currency = form.cleaned_data['currency_to']
        sent_amount = form.cleaned_data['amount_from']

        sender_currency = Currency.objects.get(currency_name=from_currency)
        sender_rate_obj = ConversionRate.objects.get(currency=sender_currency)

        receiver_currency = Currency.objects.get(currency_name=to_currency)
        receiver_rate_obj = ConversionRate.objects.get(currency=receiver_currency)

        sender_rate = sender_rate_obj.rate
        sender_symbol = sender_currency.currency_symbol
        receiver_rate = receiver_rate_obj.rate
        receiver_symbol = receiver_currency.currency_symbol

        received_amount = sent_amount*receiver_rate/sender_rate

        kwargs['sent_amount'] = sent_amount
        kwargs['received_amount'] = round(received_amount, 2)
        kwargs['sender_symbol'] = sender_symbol
        kwargs['receiver_symbol'] = receiver_symbol
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=kwargs,
            using=self.template_engine,
            **response_kwargs
        )

