from django.contrib import admin
from django.urls import path
from main import views as main_views
from users import views as users_views
from purchases import views as purchase_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login_page/', main_views.login_page, name='login_page'),
    path('register_page/', main_views.register_page, name='register_page'),
    path('register/', users_views.register, name='register'),
    path('store/', users_views.login_view, name='login_view'),
    path('main/<str:username>/<str:shopping_items>/<str:total_cost>/', users_views.main, name='main'),
    path('store/<str:username>/<str:product_id>/', purchase_views.create_purchase, name='create_purchase'),
    path('remove_product/<str:username>/<int:product_id>/', purchase_views.remove_product, name='remove_product'),
]
