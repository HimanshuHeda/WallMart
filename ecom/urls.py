
from django.urls import path
from. import views

urlpatterns = [
    path('',views.homenew,name='home'),
    path('topoffers/',views.topoffers,name='topoffers'),
    path('register_cus/',views.register_user ,name='register_cus'),
    path('login_cus/',views.login_user,name='login_cus'),
    path('logout_cus/', views.logout_view, name='logout'),
    path('productpage/<int:pk>',views.productpage,name='productpage'),
    path('categorylist/',views.categorylist,name='Categorylist'),
    path('category/<int:pk>/', views.category_view, name='Category'),
]
