from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('PrediosEjido.apps.principal.views',
	url(r'^$', 'home', name = 'home'),
	url(r'^Importar/$', 'upload_data_predio', name = 'upload_data_predio'),
	url(r'^Predios/$', 'list_predio', name = 'list_predio'),
	url(r'^Predios/Ver/(?P<predio_pk>\d+)/$', 'view_predio', name = 'view_predio'),
	url(r'^Predios/Nuevo/(?:/(?P<predio_pk>\d+))?', 'predio', name = 'predio'),
	url(r'^Predios/Venta/(?P<predio>\d+)/$', 'sold_predio', name = 'sold_predio'),
	url(r'^Predios/Venta/Nuevo-propietario/(?P<predio>\d+)/(?:/(?P<propieta>\d+))?', 'add_propieta', name = 'add_propieta'),
	url(r'^Predios/Venta/Nuevo-pago/(?P<predio>\d+)/(?:/(?P<pago>\d+))?', 'add_pago', name = 'add_pago'),
	url(r'^Predios/Venta/Eliminar-propietario/(?P<predio>\d+)/(?P<propieta>\d+)/$', 'delete_propieta_relation', name = 'delete_propieta_relation'),
	url(r'^Predios/Venta/Eliminar-pago/(?P<pago>\d+)/$', 'delete_pago', name = 'delete_pago'),
	url(r'^Predios/Eliminar/(?P<predio_pk>\d+)/$', 'delete_predio', name = 'delete_predio'),
	url(r'^Predios/Reportes/all-predio/(?:/(?P<option>\d+))?', PredioAllPDFView.as_view(), name = 'pdf_all_predio'),
	url(r'^Propietarios/$', 'list_propieta', name = 'list_propieta'),
	url(r'^Propietarios/Nuevo/(?:/(?P<propieta_pk>\d+))?/', 'propietario', name = 'propietario'),
	url(r'^Propietarios/Eliminar/(?P<propieta_pk>\d+)/$', 'delete_propieta', name = 'delete_propieta'),
	url(r'^Logout/$', 'logout_user', name = 'logout_user'),
	url(r'^Usuarios/$', 'list_user', name = 'list_user'),
	url(r'^Usuarios/Nuevo/$', 'user', name = 'user'),
)
