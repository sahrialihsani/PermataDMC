from rest_framework import viewsets
from .models import User, SubKategori, Kategori, Review, Content, Booking, Transaksi, Currency, Article, Promo
from .serializers import (
    UserSerializer,
    SubKategoriSerializer,
    KategoriSerializer,
    ReviewSerializer,
    ContentSerializer,
    BookingSerializer,
    TransaksiSerializer,
    CurrencySerializer,
    ArticleSerializer,
    PromoSerializer
)
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from .forms import LoginForm, RegisterForm, BookingForm
from django.contrib.auth.hashers import make_password
from django.db.models import Avg, Count
from django.utils.translation import activate
from django.conf import settings
import logging
from django.core.paginator import Paginator
from django.utils import timezone

logger = logging.getLogger(__name__)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SubKategoriViewSet(viewsets.ModelViewSet):
    queryset = SubKategori.objects.all()
    serializer_class = SubKategoriSerializer

class KategoriViewSet(viewsets.ModelViewSet):
    queryset = Kategori.objects.all()
    serializer_class = KategoriSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class TransaksiViewSet(viewsets.ModelViewSet):
    queryset = Transaksi.objects.all()
    serializer_class = TransaksiSerializer

class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class PromoViewSet(viewsets.ModelViewSet):
    queryset = Promo.objects.all()
    serializer_class = PromoSerializer

def index(request):
    user_points = 0
    promos = Promo.objects.all()
    categories = Kategori.objects.all()
    contents = Content.objects.select_related('subkategori', 'review').annotate(avg_rating=Avg('review__rating'), review_count=Count('review')).all()
    latest_article = Article.objects.order_by('-tanggal_post').first()
    # Ambil 2 atau 3 artikel lainnya (untuk sebelah kiri)
    other_articles = Article.objects.order_by('-tanggal_post')[1:4]

    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        user_points = user.poin  # Asumsikan Anda memiliki kolom `points` di model User
    return render(request, 'pengguna/pengguna_dashboard.html', {'user_points': user_points, 'promos': promos, 'categories': categories, 'contents': contents, 'latest_article': latest_article,
        'other_articles': other_articles})

@login_required
def super_admin_dashboard(request):
    # Cek apakah pengguna yang login adalah admin (status 1)
    if request.user.status != 1:
        # Jika bukan admin, kembalikan forbidden atau arahkan ke halaman lain
        return HttpResponseForbidden("Akses ditolak: Anda tidak memiliki izin untuk mengakses halaman ini.")
    
    return redirect('/admin/')

def login_view(request):
    # Jika pengguna sudah login, arahkan ke halaman yang sesuai dengan statusnya
    if request.user.is_authenticated:
        if request.user.status == 1:  # Superadmin
            return redirect('/admin/')  # Arahkan ke halaman admin
        else:  # Pengguna biasa
            return redirect('dashboard')  # Arahkan ke dashboard pengguna biasa

    # Form login dikirim dengan POST
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Ambil data dari form
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Autentikasi pengguna
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Login pengguna
                login(request, user)
                # Redirect berdasarkan status pengguna
                if user.status == 1:  # Superadmin
                    return redirect('/admin/')  # Arahkan ke halaman admin
                else:  # Pengguna biasa
                    return redirect('dashboard')  # Arahkan ke dashboard pengguna biasa
            else:
                messages.error(request, 'Username atau Password salah')
        else:
            messages.error(request, 'Form tidak valid')

    # Jika request bukan POST, buat form kosong
    else:
        form = LoginForm()

    # Render halaman login dengan form
    response = render(request, 'login.html', {'form': form})

    # Prevent caching of the login page
    response['Cache-Control'] = 'no-store'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'

    return response

# Logout view
def logout_view(request):
    logout(request)
    # Clear session storage and redirect to login page
    request.session.flush()  # Clears the session data, including the session cookie
    return redirect('login')


@login_required
def dashboard(request):
    # Prevent browser cache for this page
    response = None

    # If the user is not authenticated or the session is expired
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.status == 2:
        response = render(request, 'admin/admin_dashboard.html')
    elif request.user.status == 3:
        user = User.objects.get(id=request.user.id)
        user_points = user.poin  # Asumsikan Anda memiliki kolom `points` di model User
        promos = Promo.objects.all()
        categories = Kategori.objects.all()
        contents = Content.objects.select_related('subkategori', 'review').annotate(avg_rating=Avg('review__rating'), review_count=Count('review')).all()
        latest_article = Article.objects.order_by('-tanggal_post').first()
        # Ambil 2 atau 3 artikel lainnya (untuk sebelah kiri)
        other_articles = Article.objects.order_by('-tanggal_post')[1:4]
        response = render(request, 'pengguna/pengguna_dashboard.html', {'user_points': user_points, 'promos': promos, 'categories': categories, 'contents': contents, 'latest_article': latest_article,
        'other_articles': other_articles})
    else:
        return HttpResponseForbidden("Access Denied")

    # Prevent caching for the dashboard page
    response['Cache-Control'] = 'no-store'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'

    return response

def register_view(request):
    if request.method == 'POST':
        # Tambahkan nilai status ke data POST jika tidak ada
        data = request.POST.copy()
        if 'status' not in data:
            data['status'] = 3  # Default ke "user"
        form = RegisterForm(data)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Akun berhasil dibuat! Silakan login.')
            return redirect('login')
        else:
            messages.error(request, 'Ada kesalahan dalam pengisian form.')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

from django.shortcuts import redirect
from django.utils.translation import activate
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)

def set_language(request):
    # Ambil bahasa yang dipilih dari parameter 'lang'
    language = request.GET.get('lang', None)

    # Validasi bahasa yang dipilih
    if language and language in dict(settings.LANGUAGES):
        logger.debug(f"Language set to {language}")
        activate(language)
        request.session[settings.LANGUAGE_COOKIE_NAME] = language
    else:
        logger.debug("Invalid language selected")

    # Ambil URL referer (path yang sebelumnya dikunjungi)
    current_path = request.META.get('HTTP_REFERER', '/')
    print("Current path 1: %s" % current_path)

    # Pastikan URL referer hanya mencakup path, bukan domain
    if current_path.startswith(f'http://{request.get_host()}/'):
        current_path = current_path.replace(f'http://{request.get_host()}/', '/')
        print("Current path 2: %s" % current_path)
    elif current_path.startswith(f'https://{request.get_host()}/'):
        current_path = current_path.replace(f'https://{request.get_host()}/', '/')
        print("Current path 3: %s" % current_path)

    # Pastikan current_path tidak dimulai dengan '/'
    current_path = current_path.lstrip('/')
    print("Current path 4: %s" % current_path)

    # Jika current_path sudah memiliki prefiks bahasa yang baru, tidak perlu menambahkannya lagi
    if not current_path.startswith(f'{language}/'):
        # Sekarang, tambahkan kode bahasa yang baru di depan URL
        current_path = f'{language}/{current_path}'
        print("Current path 6: %s" % current_path)
    
    parts = current_path.strip('/').split('/')

    # Ambil new language (bagian pertama)
    new_language = parts[0] if len(parts) > 0 else None
    print(new_language)
    # Ambil old language (bagian kedua)
    old_language = parts[1] if len(parts) > 1 else None
    print(old_language)
    # Ambil semua bagian setelah old language sebagai remaining URL
    remaining_url = '/'.join(parts[2:]) if len(parts) > 1 else ''
    print(remaining_url)
    print(request.session.get(settings.LANGUAGE_COOKIE_NAME, settings.LANGUAGE_CODE))
    # Logika if-else untuk memproses URL
    if request.session.get(settings.LANGUAGE_COOKIE_NAME, settings.LANGUAGE_CODE)==new_language:
        # Jika bahasa awal adalah current_language, hapus old_language
        current_path = f'/{new_language}/{remaining_url}'
        print("new")
    elif request.session.get(settings.LANGUAGE_COOKIE_NAME, settings.LANGUAGE_CODE)==old_language:
        # Jika bahasa awal adalah current_language, hapus old_language
        current_path = f'/{new_language}/{remaining_url}'
        print("old")
    else:
        # Jika tidak ada old_language, langsung tambahkan new_language
        current_path = f'/{new_language}/{remaining_url}'
        print("else")
    current_path = f'/{new_language}/{remaining_url}'
    print("Current path last: %s" % current_path)

    # Redirect ke URL yang baru dengan bahasa yang dipilih
    return redirect(current_path)

@login_required
def user_bookings(request):
    user = User.objects.get(id=request.user.id)
    user_points = user.poin
    promos = Promo.objects.all()
    categories = Kategori.objects.all()
    contents = Content.objects.select_related('subkategori', 'review').annotate(avg_rating=Avg('review__rating'), review_count=Count('review')).all()
    latest_article = Article.objects.order_by('-tanggal_post').first()
    # Ambil 2 atau 3 artikel lainnya (untuk sebelah kiri)
    other_articles = Article.objects.order_by('-tanggal_post')[1:4]
    bookings_list = Booking.objects.filter(user=request.user)
    paginator = Paginator(bookings_list, 10)  # Show 10 bookings per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'pengguna/user_bookings.html', {'page_obj': page_obj, 'user_points': user_points, 'promos': promos, 'categories': categories, 'contents': contents, 'latest_article': latest_article,
        'other_articles': other_articles})
    
@login_required
def about_view(request):
    user = User.objects.get(id=request.user.id)
    user_points = user.poin
    return render(request, 'pengguna/about.html', {'user_points': user_points})

@login_required
def promo_view(request):
    user = User.objects.get(id=request.user.id)
    user_points = user.poin
    return render(request, 'pengguna/promo.html', {'user_points': user_points})

@login_required
def promo_page(request):
    user = User.objects.get(id=request.user.id)
    user_points = user.poin
    promos = Promo.objects.select_related('produk').all()
    return render(request, 'pengguna/promo_page.html', {'user_points': user_points, 'promos':promos})

def promo_detail(request, id):
    promo = Promo.objects.get(id_promo=id)
    user = User.objects.get(id=request.user.id)
    user_points = user.poin
    context = {
        'promo': promo,
        'user_points': user_points
    }
    return render(request, 'pengguna/promo_detail.html', context)

@login_required
def product_view(request):
    user = User.objects.get(id=request.user.id)
    user_points = user.poin
    products = Content.objects.select_related('subkategori', 'review').all()
    return render(request, 'pengguna/product.html', {'user_points': user_points, 'products': products})

from django.http import Http404
import logging

# Logging untuk debugging
logger = logging.getLogger(__name__)

def product_detail(request, id):
    try:
        # Ambil objek content berdasarkan ID yang diberikan
        content = Content.objects.get(id_content=id)
    except Content.DoesNotExist:
        raise Http404("Product not found")
    
    user = User.objects.get(id=request.user.id)
    user_points = user.poin  # Jika ada poin yang terkait dengan user

    if request.method == 'POST':
        jumlah_produk = request.POST['jumlah_produk']
        metode_pembayaran = request.POST['metode_pembayaran']
        deskripsi = request.POST['deskripsi']
        total_harga = int(jumlah_produk) * content.harga

        # Buat pesan WhatsApp
        pesan = f"""
        Halo, saya ingin memesan:
        Produk: {content.nama_konten}
        Harga satuan: {content.harga}
        Jumlah: {jumlah_produk}
        Total harga: {total_harga}
        Metode pembayaran: {metode_pembayaran}
        Catatan: {deskripsi}
        """
        whatsapp_url = f"https://wa.me/6285700640121?text={pesan}"
        return redirect(whatsapp_url)

    # Render detail produk
    return render(request, 'pengguna/product_detail.html', {
        'content': content, 'user_points': user_points
    })

@login_required
def point_view(request):
    user = User.objects.get(id=request.user.id)
    user_points = user.poin
    return render(request, 'pengguna/point.html', {'user_points': user_points})


from django.http import JsonResponse
from django.utils import timezone

@login_required
def save_booking_ajax(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            user = User.objects.get(id=request.user.id)
            content_id = request.POST.get('content_id')
            deskripsi = request.POST.get('deskripsi')
            jumlah_produk = int(request.POST.get('jumlah_produk'))
            
            # Ambil data content
            content = Content.objects.get(id_content=content_id)
            total_harga = jumlah_produk * content.harga
            booking_name = f'Book_{user.nama}_{content.nama_konten}_Jumlah_{jumlah_produk}'
            # Simpan ke tabel Booking
            Booking.objects.create(
                user=user,
                content=content,
                nama_booking=booking_name,
                deskripsi=deskripsi,
                waktu_booking=timezone.now(),
                harga=total_harga,
                status="pending"
            )

            return JsonResponse({'success': True, 'message': 'Booking saved successfully.'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request.'})