"""homework5 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Eshop import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", views.register_request, name="register"),
    path("index/", views.index, name = "index"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name= "logout"),
    path("products/<str:category>/", views.products_by_category, name = "products_by_category"),
    path("product/<int:id>/", views.product_by_id, name = "product_by_id"),
    path("add/<int:id>/", views.add_to_shoppingcart, name = "add_to_shoppingcart"),
    path("shoppingcart/", views.show_shopping_cart, name="show_shopping_cart"),
    path("remove/<int:id>/", views.remove_from_shoppingcart, name = "remove_from_shoppingcart"),
    path("order/", views.make_order,name = "make_order")
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
