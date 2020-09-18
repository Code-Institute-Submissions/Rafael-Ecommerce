"""shopping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from shopping_app import views
from shopping import settings
from django.conf.urls.static import static

from allauth.account.views import SignupView, LoginView, PasswordResetView, LogoutView

class MySignupView(SignupView):
    template_name = 'accounts/signup.html'

class MyLoginView(LoginView):
    template_name = 'accounts/login.html'

class MyPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'

class MyLogoutView(LogoutView):
    template_name = 'accounts/logout.html'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('product_details/',views.DetailPageView , name='product_details'),
    path('category_details/',views.CategoryDetailPageView,name='category_details'),
    path('cart/',views.Cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),

    path('', include('core.urls', namespace='core')),
    path('accounts/login/', MyLoginView.as_view(), name='account_login'),
    path('accounts/signup/', MySignupView.as_view(), name='account_signup'),
    path('accounts/password/reset/', MyPasswordResetView.as_view(), name='account_reset_password'),
    path('accounts/logout/', MyLogoutView.as_view(), name='account_logout'),
    path('accounts/', include('allauth.urls')),
    path('', views.homePageView, name='homepage'),



]+ static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)