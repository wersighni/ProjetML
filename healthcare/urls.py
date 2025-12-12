from django.contrib import admin
from django.urls import path
from predictor.views import (
    home,
    predict_view,
    choose_count,
    multi_form
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # 🏠 Page d'accueil
    path("", home, name="home"),

    # 🔹 Projet 1
    path("predict/", predict_view, name="predict"),

    # 🔹 Projet 2 (ton travail)
    path("choose/", choose_count, name="choose_count"),
    path("form_multi/<int:n>/", multi_form, name="multi_form"),
]
