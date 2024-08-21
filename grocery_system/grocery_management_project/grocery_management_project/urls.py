"""
URL configuration for grocery_management_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from grocery_app import views
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.LoginPage,name='login'),
    path('signup/',views.SignupPage,name='signup'),
    path('',views.home,name="home"),
    path('addproduct/',views.Add_Product,name="addproduct"),
    path('about/',views.About,name="About"),
    path('logout_view/',views.logout_view,name="logout_view"),
    path('read_cat/<int:id>/', views.read_cat, name="read"),
    path('product_details/<int:id>/', views.product_details, name='product_details'),
    path('card_read/<int:id>/',views.card_read,name="card_read")


]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

