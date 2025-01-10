from django.urls import path
from . import views

urlpatterns=[
    path('',views.index),
    path('login', views.login),
    path('register', views.register),
    path('cart', views.view_cart),
    path('cartview', views.add_to_cart_view),
    path('cartremove', views.remove_from_cart_view),
    path('cartedit', views.edit_cart_view),
]
