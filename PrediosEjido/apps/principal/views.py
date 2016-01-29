from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from easy_pdf.views import PDFTemplateView
from django.contrib.auth import logout
from django.shortcuts import render
from django.db.models import Sum
from .models import Predio
from .forms import *
import json

@login_required
def home(request):
	return render(request, 'home.html', {'title': 'Bienvenido'})

@login_required
def list_predio(request):
	predios = Predio.objects.all()
	return render(request, 'list-predio.html', {'title': 'Listado de Predios', 'predios': predios})

def view_predio(request, predio_pk):
	predio = Predio.objects.get(pk = predio_pk)
	return render(request, 'show-predio.html', {'title': 'Detalle del Predio', 'predio': predio})

def predio(request, predio_pk = 0):
	try:
		predio = Predio.objects.get(pk = predio_pk)
	except Predio.DoesNotExist:
		predio = predio_pk
	if request.method == 'POST':
		response = {}
		form = PredioForm(request.POST, instance = predio)
		if form.is_valid():
			if predio != 0:
				response['sold'] = True
			else:
				response['sold'] = False
			predio_data = form.save()
			response['pk'] = predio_data.pk
			response['c_catastral'] = predio_data.c_catastral
			response['dir_predio'] = predio_data.dir_predio
			response['hectarea'] = predio_data.hectarea
			response['met2'] = predio_data.met2
			response['avaluo_catastral'] = str(predio_data.avaluo_catastral)
		else:
			response['response'] = "Ha ocurrido un error"
		return HttpResponse(json.dumps(response), content_type = 'application/json')
	else:
		form = PredioForm(instance = predio)
	return render(request, 'form-predio.html', {'title': 'Nuevo Predio', 'predio_val': predio, 'forms': form})

def add_propieta(request, predio, propieta):
	predio = Predio.objects.get(c_catastral = predio)
	try:
		propieta = Propieta.objects.get(pk = propieta)
	except Propieta.DoesNotExist:
		propieta = propieta
	propieta_exclude = []
	for pre in predio.propieta_predio.all():
		propieta_exclude.append(pre.pk)
	if request.method == 'POST':
		form = PropietarioVentaForm(request.POST, propieta_exclude = propieta_exclude)
		response = {}
		if form.is_valid():
			form.save()
			propieta = Propieta.objects.get(pk = request.POST['propieta'])
			response['pk'] = propieta.pk
			response['predio'] = predio.c_catastral
			response['id_propieta'] = propieta.id_propieta
			response['name'] = propieta.name
			response['direction'] = propieta.direction
			response['tel'] = propieta.tel
			response['email'] = propieta.email
		return HttpResponse(json.dumps(response), content_type = 'application/json')
	else:
		form = PropietarioVentaForm(initial = {'predio': predio}, propieta_exclude = propieta_exclude)
	return render(request, 'add-propieta.html', {'forms': form, 'title': 'Propietarios de '+predio.c_catastral, 'propieta': propieta, 'predio': predio.c_catastral})

def delete_propieta_relation(request, predio, propieta):
	response = {}
	predio = Predio.objects.get(c_catastral = predio)
	propieta = Propieta.objects.get(pk = propieta)
	predio.propieta_predio.remove(propieta)
	response['response'] = propieta.pk
	response['type'] = "pro-"
	return HttpResponse(json.dumps(response), content_type = 'application/json')

def add_pago(request, predio, pago):
	predio = Predio.objects.get(c_catastral = predio)
	try:
		pago = Pago.objects.get(pk = pago)
	except Pago.DoesNotExist:
		pago = pago
	if request.method == 'POST':
		form = PagoForm(request.POST, instance = pago)
		response = {}
		if form.is_valid():
			pagos = form.save()
			response['pk'] = pagos.pk
			response['c_recaja'] = pagos.c_recaja
			response['f_recaja'] = str(pagos.f_recaja.strftime("%d de %B de %Y"))
			response['v_recaja'] = str(int(pagos.v_recaja))
		return HttpResponse(json.dumps(response), content_type = 'application/json')
	else:
		form = PagoForm(initial = {'predio': predio}, instance = pago)
	return render(request, 'add-pago.html', {'forms': form, 'title': 'Pagos para '+predio.c_catastral, 'pago': pago, 'predio': predio.c_catastral})

def delete_pago(request, pago):
	response = {}
	pago = Pago.objects.get(pk = pago)
	response['response'] = pago.pk
	response['type'] = ''
	pago.delete()
	return HttpResponse(json.dumps(response), content_type = 'application/json')

def sold_predio(request, predio):
	predio = Predio.objects.get(c_catastral = predio)
	pago = Pago.objects.filter(predio = predio)
	return render(request, 'sold-predio.html', {'title': 'Venta del predio '+predio.c_catastral, 'pago': pago, 'predio': predio})

def delete_predio(request, predio_pk):
	response = {}
	predio = Predio.objects.get(pk = predio_pk)
	response['response'] = predio.pk
	predio.delete()
	return HttpResponse(json.dumps(response), content_type = 'application/json')

class PredioGeneralPDFView(PDFTemplateView):
	template_name = "pdf_all_predio.html"

	def get_context_data(self, **kwargs):
		context = super(PredioGeneralPDFView, self).get_context_data(**kwargs)
		predios = Predio.objects.all()
		predios_val_sum = predios.aggregate(val_sum = Sum('avaluo_catastral'))
		context['predios_val_sum'] = predios_val_sum
		context['predios'] = predios
		context['title'] = 'LISTADO GENERAL DE PREDIOS Y PROPIERARIOS'
		return context

class PredioPropietaPDFView(PDFTemplateView):
	template_name = "pdf_propieta_predio.html"

	def get_context_data(self, **kwargs):
		context = super(PredioPropietaPDFView, self).get_context_data(**kwargs)
		predios = Predio.objects.filter(propieta_predio__isnull = False).distinct()
		context['predios'] = predios
		context['title'] = 'LISTADO DE PREDIOS POR PROPIERARIOS'
		return context

class PredioVentaPDFView(PDFTemplateView):
	template_name = "pdf_venta_predio.html"

	def get_context_data(self, **kwargs):
		context = super(PredioVentaPDFView, self).get_context_data(**kwargs)
		predios = Predio.objects.all()
		context['predios'] = predios
		context['title'] = 'LISTADO DE VENTAS POR PREDIOS'
		return context

def upload_data_predio(request):
	message = ""
	type_m = ""
	if request.method == 'POST':
		form = UploadForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			if form.upload():
				message = "Importacion Exitosa"
				type_m = "success"
			else:
				message = "Ha Ocurrido un Error"
				type_m = "danger"
	else:
		form = UploadForm()
	return render(request, 'importer.html', {'title': 'Importar', 'form': form, 'message': message, 'type_m': type_m})

def propietario(request, propieta_pk):
	predio =  request.GET.get('predio')
	try:
		propieta = Propieta.objects.get(pk = propieta_pk)
		propieta_val = propieta.pk
	except Propieta.DoesNotExist:
		propieta = propieta_pk
		propieta_val = propieta
	if request.method == 'POST':
		response = {}
		form = PropietaForm(request.POST, instance = propieta)
		if form.is_valid():
			if propieta != 0:
				response['sold'] = True
			else:
				response['sold'] = False
			propieta_data = form.save()
			response['pk'] = propieta_data.pk
			response['id_propieta'] = propieta_data.id_propieta
			response['name'] = propieta_data.name
			response['direction'] = propieta_data.direction
			response['tel'] = propieta_data.tel
			response['email'] = propieta_data.email
			response['type'] = ""
			if predio != None:
				propieta = Propieta.objects.get(pk = propieta_data.pk)
				try:
					predio = Predio.objects.get(c_catastral = predio)
					predio.propieta_predio.add(propieta)
					response['predio'] = predio.c_catastral
					response['type'] = "sold"
				except Predio.DoesNotExist:
					predio = None
		else:
			response['response'] = "Ha ocurrido un error"
		return HttpResponse(json.dumps(response), content_type = 'application/json')
	else:
		form = PropietaForm(instance = propieta)
	return render(request, 'form-propieta.html', {'title': 'Nuevo Propietario', 'predio': predio, 'propieta_val': propieta_val, 'forms': form})

def delete_propieta(request, propieta_pk):
	response = {}
	propieta = Propieta.objects.get(pk = propieta_pk)
	response['response'] = propieta.pk
	propieta.delete()
	return HttpResponse(json.dumps(response), content_type = 'application/json')

@login_required
def list_propieta(request):
	propietas = Propieta.objects.all()
	return render(request, 'list-propieta.html', {'title': 'Listado de Propietarios', 'propietas': propietas})

def logout_user(request):
	logout(request)
	return HttpResponseRedirect('/')

@user_passes_test(lambda u: u.is_superuser)
def list_user(request):
	users = User.objects.all()
	return render(request, 'list-user.html', {'title': 'Listado de Usuarios', 'users': users})

def user(request):
	if request.method == 'POST':
		response = {}
		form = UserForm(request.POST)
		if form.is_valid():
			user_data = User.objects.create_user(**form.cleaned_data)
			response['pk'] = user_data.pk
			response['username'] = user_data.username
			response['first_name'] = user_data.first_name
		else:
			response['response'] = "Ha ocurrido un error"
		return HttpResponse(json.dumps(response), content_type = 'application/json')
	else:
		form = UserForm()
	return render(request, 'form-user.html', {'title': 'Nuevo Propietario', 'forms': form})
