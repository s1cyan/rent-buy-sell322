from django.conf.urls import url

from rbs_application import views

urlpatterns = [
    url(r'^money/', views.add_withdraw, name='add_withdraw'),
    url(r'^cart/', views.cart, name='cart'),
    url(r'^checkout/', views.confirm_checkout, name='checkout'),
    url(r'^complaint/', views.file_complaint, name='complaint'),
    url(r'^login/', views.user_login, name='login'),
    url(r'^logout/', views.user_logout, name='logout'),
    url(r'^orders/', views.view_previous_orders, name='previous_orders'),
    url(r'^signup/', views.register, name='register'),
    url(r'^$', views.visitors_main, name='visitor'),
    url(r'^edit/', views.edit_listings, name='edit'),
    url(r'^results/', views.show_results, name='results'),
    url(r'^sell/', views.sell_item, name='sell'),
    # url(r'^su', views.superuser, name='superuser'),
    url(r'^update', views.update_account, name='update'),
    # url(r'^details', views.show_item_details, name='item_details'),
    url(r'^main/', views.user_main, name='user_main'),

]
