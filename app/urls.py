
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_user, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('search/', views.search_results, name='search'),
    path('set-location/', views.set_location, name='set_location'),
    path('cart/', views.view_cart, name='cart'),

    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    path('alerts/', views.price_alerts, name='price_alerts'),
    path('set-alert/', views.set_price_alert, name='set_price_alert'),
    path('delete-alert/<int:alert_id>/', views.delete_alert, name='delete_alert'),
    
        # Wishlist
    path('wishlist/', views.view_wishlist, name='view_wishlist'),
    path('add-to-wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-wishlist/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
]

