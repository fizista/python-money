from django.utils.translation import ugettext_lazy as _
from django import forms
from widgets import CurrencySelectWidget, CurrencyTextInput
from money import Money, CURRENCY

class MoneyField(forms.MultiValueField):
    """
    A MultiValueField to represent both the quantity of money and the currency
    """

    def __init__(self, choices=None, decimal_places=2, max_digits=12, *args, **kwargs):
        # Note that we catch args and kwargs that must only go to one field
        # or the other. The rest of them pass onto the decimal field.
        choices = choices or list(( (u"%s" % (c.code,), u"%s - %s" % (c.code, c.name)) for i, c in sorted(CURRENCY.items()) if c.code != 'XXX'))

        self.widget = CurrencySelectWidget(choices)

        fields = (
            forms.DecimalField(*args,
                decimal_places=decimal_places,
                max_digits=max_digits,
                **kwargs),
            forms.ChoiceField(choices=choices)
        )
        super(MoneyField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        """
        Take the two values from the request and return a single data value
        """
        if data_list:
            return Money(*data_list)
        return None


class SimpleMoneyField(forms.DecimalField):

    def __init__(self, decimal_places=2, max_digits=12, *args, **kwargs):
        self.currency = kwargs.pop('currency')
        self.widget = CurrencyTextInput()
        super(SimpleMoneyField, self).__init__(*args, decimal_places=2, max_digits=12, **kwargs)
        self.initial = Money(amount=self.initial, currency=self.currency)

    def prepare_value(self, value):
        if isinstance(value, Money):
            return value
        return Money(amount=value, currency=self.currency)

    def clean(self, value):
        value = super(SimpleMoneyField, self).clean(value)
        return Money(amount=value, currency=self.currency)
