from django.urls import path

from . import views

app_name = "festival"

urlpatterns = [
    path("", views.InicioView.as_view(), name="inicio"),
    path("ediciones/", views.EdicionListView.as_view(), name="ediciones"),
    path("ediciones/<int:pk>/", views.EdicionDetailView.as_view(), name="edicion"),
    path("categorias/<int:pk>/", views.CategoriaDetailView.as_view(), name="categoria"),
    path("votaciones/<int:pk>/", views.VotacionDetailView.as_view(), name="votacion"),
    # Panel y gestión de ediciones (solo personal)
    path("gestion/", views.PanelView.as_view(), name="gestion_panel"),
    path("gestion/ediciones/", views.GestionEdicionListView.as_view(), name="gestion_ediciones"),
    path("gestion/ediciones/nueva/", views.GestionEdicionCreateView.as_view(), name="gestion_edicion_nueva"),
    path("gestion/ediciones/<int:pk>/editar/", views.GestionEdicionUpdateView.as_view(), name="gestion_edicion_editar"),
    path("gestion/ediciones/<int:pk>/alternar/", views.GestionEdicionAlternarView.as_view(), name="gestion_edicion_alternar"),
]
