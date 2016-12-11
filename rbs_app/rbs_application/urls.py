from django.conf.urls import url

from rbs_application import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^money/', views.add_withdraw, name='add_withdraw'),
    url(r'^cart/', views.cart, name='cart'),
    url(r'^checkout/', views.checkout, name='checkout'),
    url(r'^complaint/', views.file_complaint, name='complaint'),
    url(r'^submitted-complaint', views.process_complaint, name='complaint-submitted'),
    url(r'^login/', views.user_login, name='login'),
    url(r'^logout/', views.user_logout, name='logout'),
    url(r'^orders/', views.orders, name='orders'),
    url(r'^signup/', views.register, name='register'),
    url(r'^edit/', views.edit_listings, name='edit'),
    url(r'^results/', views.show_results, name='results'),
    url(r'^details/', views.details, name='details'),
    # url(r'^details/', views.comment, name='comment'),
    url(r'^auction-item-details/', views.auction_item_details_users, name='item-auction'),
    url(r'^sell/', views.sell_item, name='sell'),
    url(r'^process-listing', views.process_sell, name='process_sell_item'),
    url(r'^update', views.update_account, name='update'),
    # url(r'^user/', views.user_index, name='user'),
    # url(r'^su', views.superuser, name='superuser'),
    # url(r'^details', views.show_item_details, name='item_details'),
]

