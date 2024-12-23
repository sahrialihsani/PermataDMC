# forms.py
from django import forms
from tourism.models import User, Booking  # Menggunakan model kustom Anda
from django.core.exceptions import ValidationError

class RegisterForm(forms.ModelForm):
    STATUS_CHOICES = [
        (1, 'superadmin'),
        (2, 'admin'),
        (3, 'user'),
    ]
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    # Menambahkan form fields yang ingin diinput oleh pengguna
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    nama = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Nama Lengkap'}))
    no_hp = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'placeholder': 'Nomor HP'}))
    status = forms.ChoiceField(choices=User.STATUS_CHOICES, initial=3, widget=forms.HiddenInput())
    is_active = forms.BooleanField(initial=True, required=False, widget=forms.HiddenInput())
    is_staff = forms.BooleanField(initial=False, required=False, widget=forms.HiddenInput())
    is_superuser = forms.BooleanField(initial=False, required=False, widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'nama', 'no_hp', 'status', 'is_active', 'is_staff', 'is_superuser']

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        
        if password != password_confirm:
            raise forms.ValidationError("Password dan Konfirmasi Password tidak cocok.")
        return password_confirm

    # Optional: Custom validation untuk memastikan status valid
    def clean_status(self):
        status = self.cleaned_data.get("status")
        if status and int(status) not in [1, 2, 3]:  # Pastikan status valid jika diberikan
            raise forms.ValidationError("Status tidak valid.")
        return status
    
    # Optional: Custom validation untuk is_staff dan is_superuser jika diperlukan
    def clean_is_staff(self):
        if self.cleaned_data.get("is_staff") and not self.cleaned_data.get("is_superuser"):
            raise forms.ValidationError("User harus menjadi superuser jika staff diaktifkan.")
        return self.cleaned_data.get("is_staff")

    def clean_is_superuser(self):
        if self.cleaned_data.get("is_superuser") and not self.cleaned_data.get("is_staff"):
            raise forms.ValidationError("User harus menjadi staff jika superuser diaktifkan.")
        return self.cleaned_data.get("is_superuser")
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))

class BookingForm(forms.ModelForm):
    # Field tambahan untuk jumlah produk
    jumlah_produk = forms.IntegerField(min_value=1, required=True, label="Jumlah Produk", initial=1)
    
    # Pilihan metode pembayaran
    METODE_PEMBAYARAN_CHOICES = [
        ('transfer', 'Transfer Bank'),
        ('cod', 'Cash on Delivery'),
        ('paypal', 'PayPal'),
    ]
    metode_pembayaran = forms.ChoiceField(choices=METODE_PEMBAYARAN_CHOICES, required=True, label="Metode Pembayaran")

    class Meta:
        model = Booking
        fields = ['nama_booking', 'deskripsi', 'waktu_booking', 'harga']
        widgets = {
            'waktu_booking': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_harga(self):
        """
        Menghitung harga berdasarkan jumlah produk yang dipesan.
        """
        harga_per_unit = self.instance.content.harga  # Mengambil harga dari produk terkait
        jumlah_produk = self.cleaned_data['jumlah_produk']
        
        if harga_per_unit is None:
            raise ValidationError("Harga produk tidak tersedia.")
        
        total_harga = harga_per_unit * jumlah_produk
        return total_harga

    def save(self, commit=True):
        # Menghitung harga berdasarkan jumlah produk yang dipilih
        instance = super().save(commit=False)
        
        # Menyimpan harga yang sudah dihitung
        instance.harga = self.cleaned_data['harga']
        
        if commit:
            instance.save()
        return instance