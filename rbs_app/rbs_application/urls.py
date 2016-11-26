from django.conf.urls import url

from rbs_application import views

urlpatterns = [
    url(r'^money/', views.add_withdraw, name='add_withdraw'),
    url(r'^cart/', views.cart, name='cart'),
    url(r'^checkout/', views.confirm_checkout, name='checkout'),
    url(r'^complaint/', views.file_complaint, name='complaint'),
    url(r'^login/', views.user_login, name='login'),
    url(r'^orders/', views.view_previous_orders, name='previous_orders'),
    url(r'^register/', views.register, name='register'),
    url(r'^$', views.visitors_main, name='index'),
]
