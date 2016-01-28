from ..models import *
from django import template
register = template.Library()
from django.db.models import Sum

@register.filter
def sum_vrecaja(value):
	pago_total = Pago.objects.filter(predio = value).aggregate(Sum('v_recaja'))
	if pago_total['v_recaja__sum'] is None:
		pago_total['v_recaja__sum'] = 0
	return pago_total['v_recaja__sum']