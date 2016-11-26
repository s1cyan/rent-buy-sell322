from django.conf.urls import url

from rbs_application import views

urlpatterns = [
    url(r'^money/', views.add_withdraw, name='add_withdraw'),
    url(r'^cart/', views.cart, name='cart'),
    url(r'^checkout/', views.confirm_checkout, name='checkout'),
    url(r'^register/', views.register, name='registration'),
    url(r'^orders/', views.view_previous_orders, name='previous_orders'),
    url(r'^$', views.visitors_main, name='visitors_main'),
]
