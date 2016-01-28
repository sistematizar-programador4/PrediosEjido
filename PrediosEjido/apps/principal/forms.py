# -*- encoding: utf-8 -*-
from django.contrib.auth.models import User
from django.forms import *
from django import forms
from .models import *
import datetime

class PredioForm(forms.ModelForm):
	class Meta:
		model = Predio
		fields = '__all__'
		exclude = ('c_recaja', 'f_recaja', 'v_recaja', 'propieta_predio')
		widgets = {
			'c_catastral': TextInput(attrs = {'class': 'form-control number-val', 'maxlength': '15', 'required': True}),
			't_ord': TextInput(attrs = {'class': 'form-control number-val', 'maxlength': '3', 'required': True}),
			't_tot': TextInput(attrs = {'class': 'form-control number-val', 'maxlength': '3', 'required': True}),
			'propieta': TextInput(attrs = {'class': 'form-control', 'maxlength': '9', 'required': True}),
			'e': TextInput(attrs = {'class': 'form-control', 'maxlength': '1'}),
			'd': TextInput(attrs = {'class': 'form-control', 'maxlength': '1'}),
			'id_propietario': TextInput(attrs = {'class': 'form-control', 'maxlength': '15', 'required': True}),
			'dir_predio': TextInput(attrs = {'class': 'form-control', 'maxlength': '30', 'required': True}),
			'hectarea': TextInput(attrs = {'class': 'form-control number-val'}),
			'met2': TextInput(attrs = {'class': 'form-control number-val', 'required': True}),
			'area_con': TextInput(attrs = {'class': 'form-control number-val'}),
			'avaluo_catastral': TextInput(attrs = {'class': 'form-control number-val', 'maxlength': '9', 'required': True})
		}
		labels = {
			'c_catastral': 'Código Catastral',
			't_ord': 'ORD',
			't_tot': 'TOT',
			'propieta': 'Nombre del Propietario',
			'e': 'E',
			'd': 'D',
			'id_propietario': 'Identificación del Propietario',
			'dir_predio': 'Dirección del Predio',
			'hectarea': 'Tamaño en Hectárea',
			'met2': 'Tamaño en Metros',
			'area_con': 'Tamaño de Área Construida',
			'avaluo_catastral': 'Valor Avaluo Catastral'
		}

class PropietarioVentaForm(forms.Form):
	predio = forms.ModelChoiceField(queryset = Predio.objects.all(), widget = forms.Select(attrs = {'class': 'form-control hide-form', 'required': True}))

	def __init__(self, *args, **kwargs):
		propieta = kwargs.pop('propieta_exclude')
		super(PropietarioVentaForm, self).__init__(*args, **kwargs)
		self.fields['propieta'] = forms.ChoiceField(label = "Propietario", choices = [('','Seleccione un Propietario')]+[(x.pk, x.id_propieta+' '+x.name) for x in Propieta.objects.all().exclude(pk__in = propieta)], widget = forms.Select(attrs = {'class': 'form-control', 'required': True}))

	def save(self):
		predio = Predio.objects.get(c_catastral = self.cleaned_data.get('predio'))
		propieta = Propieta.objects.get(pk = self.cleaned_data.get('propieta'))
		predio.propieta_predio.add(propieta)
		return predio

class UploadForm(forms.Form):
	file_input = forms.FileField()

	def upload(self):
		val = 0
		text = self.cleaned_data.get('file_input')
		for txt in text.readlines():
			predio_array = []
			val = txt.replace('\n', '').replace(',', '')
			for v in val.split(" "):
				predio_array.append(v)
			predio = Predio(c_catastral = predio_array[0], t_ord = predio_array[1], t_tot = predio_array[2], propieta = predio_array[3].replace('-', ' '), e = predio_array[4], d = predio_array[5], id_propietario = predio_array[6], dir_predio = predio_array[7].replace('-', ' '), hectarea = int(predio_array[8]), met2 = int(predio_array[9]), area_con = int(predio_array[10]), avaluo_catastral = int(predio_array[11]))
			predio.save()
		return "Importación Exitoso"

class PropietaForm(forms.ModelForm):
	class Meta:
		model = Propieta
		fields = '__all__'
		widgets = {
			'id_propieta': TextInput(attrs = {'class': 'form-control', 'maxlength': '15', 'required': True}),
			'name': TextInput(attrs = {'class': 'form-control', 'maxlength': '80', 'required': True}),
			'direction': TextInput(attrs = {'class': 'form-control', 'maxlength': '100'}),
			'tel': TextInput(attrs = {'class': 'form-control', 'maxlength': '10'}),
			'email': TextInput(attrs = {'type': 'email', 'class': 'form-control', 'maxlength': '50'}),
		}
		labels = {
			'id_propieta': 'Identificación del propietario',
			'name': 'Nombre Completo del propietario',
			'direction': 'Dirección del propietario',
			'tel': 'Número telefónico del propietario',
			'email': 'Correo Electrónico del propietario',
		}

class PagoForm(forms.ModelForm):
	class Meta:
		model = Pago
		fields = '__all__'
		widgets = {
			'c_recaja': TextInput(attrs = {'class': 'form-control number-val', 'required': True}),
			'f_recaja': TextInput(attrs = {'class': 'form-control datepicker', 'required': True}),
			'v_recaja': TextInput(attrs = {'class': 'form-control number-val', 'required': True}),
		}
		labels = {
			'c_recaja': 'Código recibo de caja',
			'f_recaja': 'Fecha',
			'v_recaja': 'Valor',
		}
	def __init__(self, *args, **kwargs):
		super(PagoForm, self).__init__(*args, **kwargs)
		self.fields['predio'] = forms.ModelChoiceField(widget = forms.Select(attrs = {'class': 'form-control'}), queryset = Predio.objects.all())

class UserForm(ModelForm):
	class Meta:
		model = User
		fields = '__all__'
		widgets = {
			'password': TextInput(attrs = {'class': 'form-control', 'type': 'password', 'required': True}),
			'username': TextInput(attrs = {'class': 'form-control', 'required': True}),
			'first_name': TextInput(attrs = {'class': 'form-control', 'required': True}),
		}
		labels = {
			'password': 'Contraseña',
			'username': 'Username',
			'first_name': 'Nombre del Usuario',
		}
		exclude = ('last_login', 'groups', 'user_permissions', 'last_name', 'email', 'date_joined', 'is_staff', 'is_active', 'is_superuser')