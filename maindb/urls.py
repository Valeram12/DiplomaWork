from django.urls import path
from . import views

urlpatterns = [
    path('', views.database, name='database'),
    path('addPresentation', views.addPr, name='addPresenatation'),
    path('<int:pk>', views.PresentationView.as_view(), name='viewPr'),
    path('<int:id>/update', views.editPr, name='updatePr'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('link/<int:id>', views.link, name='link'),
    path('search/', views.search_view, name='search_results'),

]
