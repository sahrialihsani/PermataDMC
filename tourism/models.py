from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
    
class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        """
        Create and return a regular user with a username and password.
        """
        if not username:
            raise ValueError("The Username field must be set")
        extra_fields.setdefault('is_active', True)

        # Create user with the given username and extra fields
        user = self.model(username=username, **extra_fields)
        user.set_password(password)  # Ensure password is hashed
        user.save(using=self._db)  # Save user in the database
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """
        Create and return a superuser with the necessary fields.
        """
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)  # Superusers must have is_staff set to True
        extra_fields.setdefault('is_superuser', True)  # Superusers must have is_superuser set to True

        # Create and return a superuser
        return self.create_user(username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    STATUS_CHOICES = [
        (1, 'superadmin'),
        (2, 'admin'),
        (3, 'user'),
    ]
    
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    nama = models.CharField(max_length=100)
    no_hp = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)
    poin = models.IntegerField(default=0)
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=3
    )
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)  # Default is False
    is_superuser = models.BooleanField(default=False)  # Default is False

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']  # You need to provide email for superuser and user

    def __str__(self):
        return self.username
    
class Kategori(models.Model):
    id_kategori = models.AutoField(primary_key=True)
    nama_kategori = models.CharField(max_length=100)
    deskripsi_kategori = models.TextField()
    icon_class = models.CharField(max_length=50)

    def __str__(self):
        return self.nama_kategori

class SubKategori(models.Model):
    id_subkategori = models.AutoField(primary_key=True)
    nama_subkategori = models.CharField(max_length=100)
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE, related_name="sub_categories")
    deskripsi_subkategori = models.TextField()

    def __str__(self):
        return self.nama_subkategori

class Review(models.Model):
    id_review = models.AutoField(primary_key=True)
    nama = models.CharField(max_length=100)
    rating = models.PositiveIntegerField()
    komentar = models.TextField()
    tanggal_review = models.DateField()

    def clean(self):
        if not (1 <= self.rating <= 5):
            raise ValidationError("Rating must be between 1 and 5")

    def __str__(self):
        return f"{self.nama} - {self.rating}"

class Content(models.Model):
    id_content = models.AutoField(primary_key=True)
    subkategori = models.ForeignKey(SubKategori, on_delete=models.CASCADE, related_name="contents")
    nama_konten = models.CharField(max_length=100)
    deskripsi_konten = models.TextField()
    experience = models.TextField()
    gambar = models.TextField()
    harga = models.IntegerField()
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="contents")

    def __str__(self):
        return self.nama_konten


class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed To Transaction"),
        ("cancelled", "Cancelled"),
    ]
    id_booking = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name="bookings")
    nama_booking = models.CharField(max_length=100)
    deskripsi = models.TextField()
    waktu_booking = models.DateField()
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return self.nama_booking


class Transaksi(models.Model):
    id_transaksi = models.AutoField(primary_key=True)
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name="transactions")
    nama_transaksi = models.CharField(max_length=100)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="transactions")

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]
    status_transaksi = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(default=timezone.now())
    updated_at = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.nama_transaksi


class Currency(models.Model):
    id_currency = models.AutoField(primary_key=True)
    negara_input = models.CharField(max_length=100)
    negara_tujuan = models.CharField(max_length=100)
    nilai_konversi = models.DecimalField(max_digits=12, decimal_places=4)

    def clean(self):
        if self.negara_input == self.negara_tujuan:
            raise ValidationError("Source and destination countries must be different.")

    def __str__(self):
        return f"{self.negara_input} to {self.negara_tujuan}"
    
class Promo(models.Model):
    id_promo = models.AutoField(primary_key=True)
    nama = models.CharField(max_length=100)
    deskripsi = models.TextField()
    gambar = models.TextField()
    expiry_date = models.DateField()
    produk = models.ForeignKey(Content, on_delete=models.CASCADE, related_name="promo")

    def __str__(self):
        return self.nama

class Article(models.Model):
    id_article = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")
    judul = models.CharField(max_length=100)
    gambar = models.TextField()
    konten = models.TextField()
    tanggal_post = models.DateTimeField(default=timezone.now())
    
    def __str__(self):
        return self.judul