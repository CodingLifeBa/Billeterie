from django.urls import path
from . import views
from accounts.views import signup, login_user
from accounts.views import logout_user


urlpatterns = [
    
    path('', views.home, name='home'),
    path('application/signup/', signup, name="signup" ),
    path('application/logout/',logout_user, name="logout"),
    path('accounts/login/',login_user, name="login"),
    path('evenement/<int:id>/', views.evenement_detail, name='evenement_detail'),
    path('evenement/<int:id>/add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('evenement/<int:id>/remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart, name='cart'),
    path('cart/delete', views.delete_cart, name='delete_cart'),
    path('cart/total', views.cart_total, name='cart_total'),
    path('ajouter_evenement/', views.ajouter_evenement, name='ajouter_evenement'),
    path('list_evenement/', views.list_evenement, name='list_evenement'),
]
