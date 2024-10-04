
from django.urls import path
from. import views
# from .views import CartView

app_name = 'cart'

urlpatterns = [
    path('add/<int:prd_id>/',views.add_cart,name='add_cart'),
    path('',views.cart_detail,name='cart_detail'),
    path('remove/<int:prd_id>/',views.cart_remove,name='cart_remove'),
    path('full_remove/<int:prd_id>/', views.full_remove,name='full_remove'),
    path('order/<int:prd_id>/', views.create_order, name='create_order'),
    path('myorder/', views.myorder, name='myorder'),
    path('wishlist/add/<int:prd_id>/', views.add_wish, name='add_wish'),
    path('wishlist/', views.wish_detail, name='wish_detail'),
    path('wishlist/remove/<int:prd_id>/', views.remove_wish_item, name='remove_wish_item'),
    path('wishlist/addcartdelwish/<int:prd_id>/', views.combined_wish_cart, name='combined_wish_cart'),
    path('create-order-all/', views.create_order_for_all, name='create_order_for_all'),
]
