# tourism/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Inisialisasi router untuk API
router = DefaultRouter()
router.register('user', views.UserViewSet, basename='user')
router.register('subkategori', views.SubKategoriViewSet, basename='subkategori')
router.register('kategori', views.KategoriViewSet, basename='kategori')
router.register('review', views.ReviewViewSet, basename='review')
router.register('content', views.ContentViewSet, basename='content')
router.register('booking', views.BookingViewSet, basename='booking')
router.register('transaksi', views.TransaksiViewSet, basename='transaksi')
router.register('currency', views.CurrencyViewSet, basename='currency')
router.register('article', views.ArticleViewSet, basename='article')
router.register('promo', views.PromoViewSet, basename='promo')

# Daftar URL untuk aplikasi 'tourism'
urlpatterns = [
    path('', views.index, name='index'),
    path('set_language/', views.set_language, name='set_language'),
    path('admin/', views.super_admin_dashboard, name='super_admin_dashboard'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/', include(router.urls)),  # URL untuk API aplikasi 'tourism'
    path('bookings/', views.user_bookings, name='user_bookings'),
    path('about/', views.about_view, name='about_view'),
    path('promo/', views.promo_view, name='promo_view'),
    path('promo_page/', views.promo_page, name='promo_page'),
    path('promo_detail/<int:id>/', views.promo_detail, name='promo_detail'),
    path('product/', views.product_view, name='product_view'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('point/', views.point_view, name='point_view'),
    path('save-booking/', views.save_booking_ajax, name='save_booking_ajax'),
]