from django.urls import path, include
from .import views
from django.contrib import admin
"""
urlpatterns = [
    path('', views.dashboard_with_pivot, name='dashboard_with_pivot'),
    path('data', views.pivot_data, name='pivot_data'),
]
"""
admin.autodiscover()
app_name = "dashboard"

urlpatterns = [
    path("", views.index, name="dashboard"),
    path("index1/", views.index1, name="index1"),
    path("app_profil/", views.app_profil, name="app_profil"),
    path("search_history/", views.search_history, name="search_history"),
    path("download_history/", views.download_history, name="download_history"),
    path("review_analysis/", views.review_analysis, name="review_analysis"),
    path("form-basic/", views.form_basic, name="form-basic"),
    path("form-wizard/", views.form_wizard, name="form-wizard"),
    path("smilar_app/", views.smilar_app, name="smilar_app"),
    path("icon-material/", views.icon_material, name="icon-material"),
    path("icon-fontawesome/", views.icon_fontawesome, name="icon-fontawesome"),
    path("new_app/", views.new_app, name="new_app"),
    path("gallery/", views.gallery, name="gallery"),
    path("invoice/", views.invoice, name="invoice"),
    path("chat/", views.chat, name="chat"),
    path("search/", views.search, name="search"),
    path("searchreview/", views.searchreview, name="searchreview"),
    path("searchprofil/", views.searchprofil, name="searchprofil"),
    path("download/", views.download, name="download"),
    path("categorie/", views.categorie, name="categorie"),
    path("export_pdf/", views.export_pdf, name="export_pdf"),
]
