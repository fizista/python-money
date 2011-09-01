from django import forms
from django.utils.safestring import mark_safe
from money import Money, CURRENCY
from decimal import Decimal

class CurrencyTextInput(forms.TextInput):

    def render(self, name, value, attrs=None):
        if value is None:
            return super(CurrencyTextInput, self).render(name, value, attrs)
        rendered = super(CurrencyTextInput, self).render(name, value.amount, attrs)
        return mark_safe('<span class="currency">%s</span>%s' % (value.currency.symbol, rendered))

class CurrencySelectWidget(forms.MultiWidget):
    """
    Custom widget for entering a value and choosing a currency
    """
    def __init__(self, choices=None, attrs=None):
        widgets = (
            CurrencyTextInput(attrs=attrs),
            forms.Select(attrs=attrs, choices=choices),
        )
        super(CurrencySelectWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        #print "CurrencySelectWidget decompress %s" % value
        if value:
            return [value, value.currency]
        return [None,None]
