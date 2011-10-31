from django import forms
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from money import Money, CURRENCY
from decimal import Decimal

class CurrencyTextInput(forms.TextInput):

    def render(self, name, value, attrs=None):
        if value is None:
            return super(CurrencyTextInput, self).render(name, value, attrs)
        rendered = super(CurrencyTextInput, self).render(name, value.amount, attrs)
        return mark_safe('<span class="money"><span class="currency">%s</span>%s</span>' % (value.currency.symbol, rendered))

    def _has_changed(self, initial, data):
        """
        Return True if data differs from initial.
        """
        # For purposes of seeing whether something has changed, None is
        # the same as an empty string, if the data or inital value we get
        # is None, replace it w/ u''.
        if data is None:
            data_value = u''
        else:
            data_value = data
        if initial is None:
            initial_value = u''
        else:
            initial_value = initial.amount
        if force_unicode(initial_value) != force_unicode(data_value):
            return True
        return False

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
