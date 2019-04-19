
from django.conf.urls import url, include
from django.contrib import admin
from eshop import views
from rest_framework.authtoken import views as rest_framework_views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^login/', views.user_authentication),
    url(r'^logout/', views.user_session_end),
    url(r'^registration/', views.registration),
    url(r'^confirm/(?P<activation_key>\w+)/', views.register_confirm),
    url(r'^Dashboard/', views.dashboard),
    url(r'^CreateProduct/', views.create_product),
    # url(r'^Product/', views.product_list),
    url(r'^admin/', admin.site.urls),

    # User Login and Logout
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Token Generation for login
    url(r'^get_auth_token/$', rest_framework_views.obtain_auth_token, name='get_auth_token'),

    url(r'^customer/$', views.customer.as_view(), name='customer'),
    url(r'^product/$', views.product.as_view(), name='product'),
    url(r'^cart/$', views.cart.as_view(), name='cart'),
]
