from django.contrib import admin
from .models import User, SubKategori, Kategori, Review, Content, Booking, Transaksi, Currency, Article, Promo

# Custom UserAdmin untuk model User
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'nama', 'no_hp', 'email', 'status', 'is_active', 'date_joined', 'last_login', 'is_superuser', 'is_staff')
    list_filter = ('status', 'is_active', 'is_superuser', 'is_staff')
    search_fields = ('username', 'email', 'nama')
    ordering = ('id',)
    list_editable = ('is_active', 'is_staff')

# Daftarkan model User
admin.site.register(User, UserAdmin)
    
# Kategori Admin
class KategoriAdmin(admin.ModelAdmin):
    list_display = ('id_kategori', 'nama_kategori', 'deskripsi_kategori', 'icon_class')
    search_fields = ('nama_kategori',)

# Daftarkan model SubKategori
admin.site.register(Kategori, KategoriAdmin)

# Kategori Admin
class SubKategoriAdmin(admin.ModelAdmin):
    list_display = ('id_subkategori', 'nama_subkategori', 'kategori', 'deskripsi_subkategori')
    search_fields = ('nama_subkategori',)
    list_filter = ('kategori',)

# Daftarkan model Kategori
admin.site.register(SubKategori, SubKategoriAdmin)

# Review Admin
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id_review', 'nama', 'rating', 'tanggal_review')
    search_fields = ('nama',)
    list_filter = ('rating',)

# Daftarkan model Review
admin.site.register(Review, ReviewAdmin)

# Content Admin
class ContentAdmin(admin.ModelAdmin):
    list_display = ('id_content', 'subkategori', 'nama_konten', 'review', 'gambar', 'harga')
    search_fields = ('nama_konten', 'deskripsi_konten')
    list_filter = ('subkategori',)

# Daftarkan model Content
admin.site.register(Content, ContentAdmin)

# Booking Admin
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id_booking', 'content', 'user', 'nama_booking', 'waktu_booking', 'harga', 'status')
    search_fields = ('nama_booking', 'user', 'deskripsi')
    list_filter = ('waktu_booking',)

# Daftarkan model Booking
admin.site.register(Booking, BookingAdmin)

# Transaksi Admin
class TransaksiAdmin(admin.ModelAdmin):
    list_display = ('id_transaksi', 'content', 'nama_transaksi', 'status_transaksi', 'created_at', 'updated_at')
    search_fields = ('nama_transaksi',)
    list_filter = ('status_transaksi', 'created_at')

# Daftarkan model Transaksi
admin.site.register(Transaksi, TransaksiAdmin)

# Currency Admin
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('id_currency', 'negara_input', 'negara_tujuan', 'nilai_konversi')
    search_fields = ('negara_input', 'negara_tujuan')
    list_filter = ('negara_input', 'negara_tujuan')

# Daftarkan model Currency
admin.site.register(Currency, CurrencyAdmin)

# Promo Admin
class PromoAdmin(admin.ModelAdmin):
    list_display = ('id_promo', 'nama', 'deskripsi', 'produk', 'gambar', 'expiry_date')
    search_fields = ('nama', 'deskripsi')
    list_filter = ('produk',)

# Daftarkan model Promo
admin.site.register(Promo, PromoAdmin)

# Article Admin
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id_article', 'judul', 'user', 'tanggal_post', 'gambar')
    search_fields = ('judul', 'konten')
    list_filter = ('user', 'tanggal_post')

# Daftarkan model Article
admin.site.register(Article, ArticleAdmin)