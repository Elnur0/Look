from django.urls import path

from . import views
app_name = "mainapp"

urlpatterns = [
    path('list/', views.PrductListView.as_view(), name='list'),
    path('detail/<id>/', views.ProductDetailView.as_view(), name='detail'),
    path('wish/<id>/', views.WishView.as_view(), name='wish'),
    path('wish-list/', views.WishlistView.as_view(), name='wish'),
    path('basket/<id>/', views.BasketView.as_view(), name='basket'),
    path("basket-list/", views.BasketListView.as_view(), name="basket-list"),
    path('review/<id>/', views.ReviewView.as_view(), name='review'),
    path('categores/', views.CategoryView.as_view(), name='category'),
    path("categores/detail/<id>/", views.CategoryDetailView.as_view(), name="category-detail"),
    path('sizes/', views.SizeView.as_view(), name='size'),
    path('colors/', views.ColorView.as_view(), name='color'),
    path('brends/', views.BrendView.as_view(), name='brend'),
    # path('search/', views.SearchView.as_view(), name='global_search'),
]
    



