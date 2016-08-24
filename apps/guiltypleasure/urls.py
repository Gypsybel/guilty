from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^log_reg$', views.log_reg),
    url(r'^customer_login$', views.customer_login),
    url(r'^register$', views.register),
    url(r'^customer_logout$', views.customer_logout),
    url(r'^category/(?P<id>\d+)$', views.category),
    url(r'^show_product/(?P<id>\d+)$', views.show_product),
    url(r'^review/(?P<id>\d+)$', views.review),
    url(r'^comment/(?P<id>\d+)$', views.comment),
    url(r'^buy/(?P<id>\d+)$', views.buy),
    url(r'^cart$', views.cart),
    url(r'^update$', views.update),
    url(r'^pay$', views.pay),
    url(r'^admin_index$', views.admin_index),
    url(r'^admin_log$', views.admin_log),
    url(r'^orders$', views.orders),
    url(r'^products$', views.products),
    url(r'^addnew$', views.addnew),
    url(r'^show_order/(?P<id>\d+)$', views.show_order),
    url(r'^edit/(?P<id>\d+)$', views.edit),
]
