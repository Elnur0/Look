from django.urls import path

from . import views
app_name = "blogs"

urlpatterns = [
    path('list/', views.BlogView.as_view(), name='list'),
    path('detail/<id>/', views.BlogDetailView.as_view(), name='detail'),

]