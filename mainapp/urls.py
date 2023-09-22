from django.urls import path

from . import views
app_name = "mainapp"

urlpatterns = [
    path('list/', views.PrductListView.as_view(), name='list'),
    path('detail/<id>/', views.ProductDetailView.as_view(), name='detail'),
    path('wish/<id>/', views.WishlistView.as_view(), name='wish'),
    path('basket/<id>/', views.BasketView.as_view(), name='basket'),
    path('review/<id>/', views.ReviewView.as_view(), name='review'),
]
    



