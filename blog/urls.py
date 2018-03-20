from blog import views
from django.urls import path

urlpatterns = [
    path('edit/<slug:blog>', views.edit),
    path('edit', views.edit),
    path('view/<slug:blog>', views.read),
    path('view', views.read),
    path('markdown/<slug:blog>', views.get),
    path('markdown', views.get),
    path('add', views.add),
    path('put', views.put),
    path('', views.index)
]
