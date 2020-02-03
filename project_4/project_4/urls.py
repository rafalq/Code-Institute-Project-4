"""project_4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from users.views import CartListView
# from users.views import ItemBuyAtAuctionView
# from checkout import views as checkout_views
# ItemBuyAtAuctionView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', user_views.login_request, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('', include('auction_store.urls')),
    path('profile/history/', user_views.history, name='history'),
    path('profile/cart/', CartListView.as_view(), name='cart'),
    # path('profile/cart/checkout/',
    #      user_views.checkout, name='checkout'),
    # path('checkout/', include('checkout.urls')),
    # path('profile/cart/item/<int:pk>/checkout/',
    #      checkout_views.checkout, name='checkout'),
    # path('store/item/<int:pk>/checkout/',
    #      ItemBuyAtAuctionView.as_view(), name='checkout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
