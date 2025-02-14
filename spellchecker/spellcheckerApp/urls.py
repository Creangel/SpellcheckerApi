from django.urls import path
from . import views


urlpatterns = [

	path('',views.home, name='home'),
	path('active', views.active),
	path('createModel', views.createModel),
	path('loadModels', views.loadModels),
	path('wordSpell', views.wordSpell),
]