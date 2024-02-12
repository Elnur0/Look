from django.urls import path

from . import views
app_name = "settings"

urlpatterns = [
    path('', views.SettingsView.as_view(), name='settings'),
    path('subscribe/', views.NewslettercreateView.as_view(), name='subscribe'),
    path('faq/', views.FAQListView.as_view(), name='faq'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('shipping/', views.ShippingView.as_view(), name='shipping'),
    path('payment/', views.PaymentView.as_view(), name='payment'),
]