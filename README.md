
# **Todo list app**

---

### **Modul: Inisialisasi Aplikasi Flask**

Modul ini bertanggung jawab untuk mempersiapkan aplikasi Flask, menginisialisasi ekstensi, mengatur konfigurasi aplikasi, dan mendaftarkan blueprint.

---

### **Fungsionalitas**

#### **1\. Inisialisasi Ekstensi**

db \= SQLAlchemy()  
login\_manager \= LoginManager()

* **`SQLAlchemy`**: Digunakan untuk manajemen database dalam aplikasi.  
* **`LoginManager`**: Mengelola autentikasi pengguna, termasuk login dan logout, serta melindungi rute aplikasi.

---

#### **2\. Fungsi `create_app`**

def create\_app(config\_class=Config):  
    app \= Flask(\_\_name\_\_)

* **Deskripsi**: Fungsi factory untuk membuat dan mengembalikan instance aplikasi Flask.  
* **Parameter**:  
  * `config_class`: Kelas konfigurasi yang digunakan untuk mengatur aplikasi.

---

#### **3\. Konfigurasi Aplikasi**

app.config\['SECRET\_KEY'\] \= 'mysecret'  
app.config\['SQLALCHEMY\_DATABASE\_URI'\] \= 'sqlite:///todolist.db'  
app.config\['SQLALCHEMY\_TRACK\_MODIFICATIONS'\] \= False

* **`SECRET_KEY`**: Digunakan untuk menjaga keamanan aplikasi, misalnya untuk mengenkripsi data sesi.  
* **`SQLALCHEMY_DATABASE_URI`**: Menentukan lokasi dan jenis database yang digunakan (`sqlite:///todolist.db` dalam kasus ini).  
* **`SQLALCHEMY_TRACK_MODIFICATIONS`**: Dimatikan untuk meningkatkan performa dan menghindari peringatan deprecation.

---

#### **4\. Inisialisasi Ekstensi**

db.init\_app(app)  
login\_manager.init\_app(app)  
login\_manager.login\_view \= 'auth\_bp.login'

* **`db.init_app(app)`**: Mengaitkan ekstensi SQLAlchemy dengan aplikasi Flask.  
* **`login_manager.init_app(app)`**: Mengaitkan LoginManager dengan aplikasi Flask.  
* **`login_manager.login_view`**: Menentukan rute login yang akan diakses ketika pengguna mencoba mengakses rute yang dilindungi tanpa login.

---

#### **5\. User Loader**

@login\_manager.user\_loader  
def load\_user(user\_id):  
    from app.models import User  
    return User.query.get(int(user\_id))

* **Deskripsi**: Fungsi ini digunakan oleh `LoginManager` untuk memuat pengguna berdasarkan ID.  
* **Parameter**:  
  * `user_id`: ID pengguna yang disimpan dalam sesi login.  
* **Return**: Instance pengguna (`User`) yang cocok dengan ID, atau `None` jika tidak ditemukan.

---

#### **6\. Pendaftaran Blueprint**

from .routes import register\_blueprints  
register\_blueprints(app)

* **`register_blueprints(app)`**: Fungsi yang digunakan untuk mendaftarkan blueprint yang didefinisikan di modul `routes`.  
* **Manfaat**:  
  * Mempermudah modularisasi aplikasi.  
  * Memisahkan logika dan rute aplikasi ke dalam modul terpisah.

---

#### **7\. Pembuatan Context Aplikasi**

with app.app\_context():  
    from app import models

* **Deskripsi**: Membuat konteks aplikasi untuk memastikan bahwa database (`db`) dan model dapat digunakan.  
* **Fungsi**:  
  * Memuat modul `models` agar semua definisi model tersedia sebelum aplikasi berjalan.

---

### **Pengembalian**

return app

* Mengembalikan instance aplikasi Flask yang sudah diinisialisasi dan dikonfigurasi.

---

### **Keamanan**

1. **`SECRET_KEY`**: Harus diganti dengan string yang lebih kuat untuk produksi.  
2. **`SQLALCHEMY_DATABASE_URI`**: URI database sebaiknya disembunyikan menggunakan variabel lingkungan (environment variable).

---

### **Potensi Peningkatan**

1. **Gunakan Variabel Lingkungan**:  
   * Hindari hardcoding `SECRET_KEY` dan `SQLALCHEMY_DATABASE_URI`.  
   * Gunakan `os.environ.get` untuk mengambil nilai dari variabel lingkungan.

app.config\['SECRET\_KEY'\] \= os.environ.get('SECRET\_KEY', 'defaultsecret')  
app.config\['SQLALCHEMY\_DATABASE\_URI'\] \= os.environ.get('DATABASE\_URI', 'sqlite:///todolist.db')

2.   
3. **Error Handling**:  
   * Tambahkan mekanisme penanganan error (misalnya, untuk database yang tidak tersedia).  
4. **Logging**:  
   * Implementasikan logging untuk melacak aktivitas aplikasi.

---

### **Modul: Model Database**

Modul ini mendefinisikan model database untuk aplikasi menggunakan SQLAlchemy sebagai ORM (Object Relational Mapper). Model mencakup entitas `User` dan `Task`.

---

### **Model 1: `User`**

Represents pengguna aplikasi.

#### **Atribut**

1. **`id`**

   * **Tipe**: Integer  
   * **Deskripsi**: Primary key untuk identifikasi unik setiap pengguna.  
2. **`username`**

   * **Tipe**: String (maks. 100 karakter)  
   * **Deskripsi**: Nama pengguna yang harus unik.  
   * **Properti**:  
     * `unique=True`: Setiap pengguna harus memiliki nama unik.  
     * `nullable=False`: Tidak boleh kosong.  
3. **`password`**

   * **Tipe**: String (maks. 256 karakter)  
   * **Deskripsi**: Kata sandi pengguna yang telah di-hash untuk keamanan.  
   * **Properti**:  
     * `nullable=False`: Tidak boleh kosong.

#### **Fungsi Tambahan**

* **`UserMixin`**: Mengintegrasikan model `User` dengan Flask-Login, memberikan fitur seperti autentikasi dan manajemen sesi.

---

### **Model 2: `Task`**

Represents tugas atau pekerjaan yang harus dilakukan pengguna.

#### **Atribut**

1. **`id`**

   * **Tipe**: Integer  
   * **Deskripsi**: Primary key untuk identifikasi unik setiap tugas.  
2. **`name`**

   * **Tipe**: String (maks. 100 karakter)  
   * **Deskripsi**: Nama atau deskripsi singkat dari tugas.  
   * **Properti**:  
     * `nullable=False`: Tidak boleh kosong.  
3. **`priority`**

   * **Tipe**: String (maks. 10 karakter)  
   * **Deskripsi**: Tingkat prioritas tugas (misalnya, *Low*, *Medium*, *High*).  
   * **Properti**:  
     * `nullable=False`: Tidak boleh kosong.  
4. **`date`**

   * **Tipe**: String (maks. 10 karakter)  
   * **Deskripsi**: Tanggal tugas, disimpan dalam format string.  
   * **Properti**:  
     * `nullable=True`: Opsional (tidak wajib diisi).  
5. **`done`**

   * **Tipe**: Boolean  
   * **Deskripsi**: Status tugas apakah sudah selesai atau belum.  
   * **Default**: `False`.  
6. **`user_id`**

   * **Tipe**: Integer  
   * **Deskripsi**: Foreign key yang merujuk pada `id` pengguna di model `User`.  
   * **Properti**:  
     * `nullable=False`: Tidak boleh kosong.  
7. **`user`**

   * **Deskripsi**: Relasi antara `Task` dan `User`.  
   * **Properti**:  
     * **`backref`**: Memberikan akses dari `User` ke semua `Task` miliknya.  
     * **`lazy=True`**: Relasi akan dimuat saat diperlukan.

---

### **Relasi**

* **`Task.user_id`**: Relasi `many-to-one` dengan model `User`.  
  * Setiap tugas (`Task`) terhubung dengan satu pengguna (`User`).  
  * Atribut `user` memberikan akses ke pengguna terkait dari instance `Task`.

---

### **Keamanan**

1. **Kata Sandi**:

   * Kata sandi disimpan dalam bentuk hashed. Pastikan Anda menggunakan hashing yang aman, seperti `werkzeug.security.generate_password_hash`.  
2. **Validasi Input**:

   * Implementasikan validasi pada `username` dan `password` untuk mencegah injeksi SQL atau data tidak valid.

---

### **Potensi Peningkatan**

1. **Penambahan Validasi Model**

   * Gunakan **SQLAlchemy Validators** atau library tambahan untuk memastikan format data, seperti memeriksa panjang string atau format tanggal.  
2. **Audit Trail**

   * Tambahkan kolom seperti `created_at` dan `updated_at` untuk melacak waktu pembuatan dan pembaruan data.  
3. **Tipe Data `date`**

   * Ganti `date` di model `Task` dari `String` ke `Date` agar lebih sesuai dengan data tanggal.  
4. **Soft Delete**

   * Pertimbangkan menambahkan fitur soft delete untuk pengguna atau tugas, sehingga data tidak benar-benar dihapus dari database.

---

### **Modul: Authentication**

Modul ini mengelola proses autentikasi pengguna, termasuk login, pendaftaran (register), dan logout. Semua fitur ini diimplementasikan menggunakan Flask, Flask-Login, dan integrasi database dengan SQLAlchemy.

---

#### **Blueprint Initialization**

auth\_bp \= Blueprint('auth\_bp', \_\_name\_\_)

Blueprint `auth_bp` digunakan untuk mengelompokkan semua rute yang terkait dengan autentikasi pengguna. Ini mempermudah pemisahan logika aplikasi menjadi modul yang lebih terorganisasi.

---

### **Rute dan Fungsionalitas**

#### 1\. **Login \- `login`**

@auth\_bp.route('/login', methods=\['GET', 'POST'\])

def login():

    if request.method \== 'POST':

        username \= request.form.get('username')

        password \= request.form.get('password')

        user \= User.query.filter\_by(username=username).first()

        if user and check\_password\_hash(user.password, password):

            login\_user(user)

            return redirect(url\_for('main\_bp.index'))

        else:

            flash('Login Unsuccessful. Please check username and password', 'danger')

    return render\_template('login.html')

- **Deskripsi**:  
  Memungkinkan pengguna untuk masuk ke aplikasi.  
- **Metode HTTP**: `GET`, `POST`  
- **Proses**:  
  - **GET**: Menampilkan halaman login.  
  - **POST**:  
    1. Mengambil username dan password dari form.  
    2. Memeriksa apakah username ada di database.  
    3. Memverifikasi password menggunakan `check_password_hash`.  
    4. Jika berhasil, pengguna akan login dan diarahkan ke halaman utama.  
    5. Jika gagal, menampilkan pesan kesalahan menggunakan `flash`.  
- **Keamanan**:  
  - Hash password disimpan di database dan diverifikasi menggunakan `check_password_hash`.  
  - Menghindari kebocoran data sensitif melalui pesan kesalahan generik.

---

#### 2\. **Register \- `register`**

@auth\_bp.route('/register', methods=\['GET', 'POST'\])

def register():

    if request.method \== 'POST':

        username \= request.form.get('username')

        password \= request.form.get('password')

        user \= User.query.filter\_by(username=username).first()

        if user:

            flash('Username already exists', 'danger')

            return redirect(url\_for('auth\_bp.register'))

        new\_user \= User(username=username, password=generate\_password\_hash(password, method='pbkdf2:sha256'))

        db.session.add(new\_user)

        db.session.commit()

        login\_user(new\_user)

        return redirect(url\_for('main\_bp.index'))

    return render\_template('register.html')

- **Deskripsi**:  
  Memungkinkan pengguna untuk membuat akun baru.  
- **Metode HTTP**: `GET`, `POST`  
- **Proses**:  
  - **GET**: Menampilkan halaman registrasi.  
  - **POST**:  
    1. Mengambil username dan password dari form.  
    2. Memeriksa apakah username sudah digunakan.  
    3. Jika username tersedia, membuat pengguna baru dengan hash password menggunakan `generate_password_hash`.  
    4. Menyimpan pengguna baru ke database.  
    5. Secara otomatis login pengguna baru dan mengarahkan mereka ke halaman utama.  
    6. Jika username sudah ada, menampilkan pesan kesalahan menggunakan `flash`.  
- **Keamanan**:  
  - Password yang disimpan di database di-hash untuk menghindari penyimpanan data mentah.  
  - Cegah duplikasi username melalui validasi sebelum menyimpan ke database.

---

#### 3\. **Logout \- `logout`**

@auth\_bp.route('/logout')

@login\_required

def logout():

    logout\_user()

    return redirect(url\_for('auth\_bp.login'))

- **Deskripsi**:  
  Memungkinkan pengguna untuk keluar dari aplikasi.  
- **Metode HTTP**: `GET`  
- **Proses**:  
  1. Memanggil fungsi `logout_user` untuk menghapus sesi pengguna.  
  2. Mengarahkan pengguna ke halaman login.  
- **Keamanan**:  
  - Rute ini dilindungi dengan `@login_required` untuk memastikan hanya pengguna yang sudah login dapat logout.

---

### **Keamanan yang Diterapkan**

2. **Hash Password**: Password disimpan dalam format hash menggunakan `pbkdf2:sha256` untuk mengamankan data pengguna.  
3. **Proteksi Sesi**:  
   - Hanya pengguna yang sudah login dapat mengakses rute logout.  
   - Password diverifikasi menggunakan `check_password_hash` untuk menghindari penyimpanan password mentah.  
4. **Pesan Flash**:  
   - Menggunakan `flash` untuk memberikan umpan balik kepada pengguna tanpa membocorkan informasi sensitif.

---

### **Potensi Peningkatan**

1. **Validasi Input**:  
   - Pastikan username dan password memenuhi aturan tertentu, seperti panjang minimum, tidak boleh kosong, dll.  
   - Validasi sisi klien menggunakan JavaScript.  
2. **Rate Limiting**:  
   - Terapkan mekanisme pembatasan jumlah percobaan login untuk mencegah brute force.  
3. **Error Logging**:  
   - Tambahkan logging untuk mencatat kesalahan autentikasi atau upaya login yang mencurigakan.  
4. **HTTPS**:  
   - Gunakan HTTPS untuk melindungi data sensitif yang dikirimkan dalam form.

Berikut adalah dokumentasi untuk kode yang diberikan:

---

### **Modul: Task Management**

Modul ini berisi rute-rute (routes) utama untuk mengelola tugas (tasks) di aplikasi berbasis Flask. Semua rute dilindungi dengan decorator `@login_required`, sehingga hanya pengguna yang sudah login dapat mengakses fitur-fitur ini.

---

#### **Blueprint Initialization**

main\_bp \= Blueprint('main\_bp', \_\_name\_\_)

Blueprint `main_bp` digunakan untuk mengelompokkan rute-rute utama aplikasi, seperti pengelolaan tugas (task management).

---

### **Rute dan Fungsionalitas**

#### 1\. **Homepage \- `index`**

@main\_bp.route("/")

@login\_required

def index():

    tasks \= Task.query.filter\_by(user\_id=current\_user.id).all()  \# Filter tasks by current user

    return render\_template("index.html", tasks=tasks)

- **Deskripsi**:  
  Menampilkan halaman utama dengan daftar tugas yang dimiliki oleh pengguna yang sedang login.  
- **Metode HTTP**: `GET`  
- **Proses**:  
  1. Query tugas dari database berdasarkan `user_id` pengguna saat ini.  
  2. Kirim data tugas ke template `index.html` untuk ditampilkan.  
- **Keamanan**: Menggunakan `current_user.id` untuk memastikan hanya tugas milik pengguna saat ini yang ditampilkan.

---

#### 2\. **Menambahkan Tugas \- `add_task`**

@main\_bp.route("/add", methods=\["POST"\])

@login\_required

def add\_task():

    name \= request.form.get("name")

    priority \= request.form.get("priority")

    date \= request.form.get("date")

    if name:

        new\_task \= Task(name=name, priority=priority, date=date, user\_id=current\_user.id)

        db.session.add(new\_task)

        db.session.commit()

    return redirect(url\_for("main\_bp.index"))

- **Deskripsi**:  
  Menambahkan tugas baru ke dalam database.  
- **Metode HTTP**: `POST`  
- **Proses**:  
  1. Mengambil data tugas dari form (`name`, `priority`, `date`).  
  2. Membuat objek `Task` baru dan menghubungkannya dengan `user_id` pengguna saat ini.  
  3. Menyimpan tugas ke database.  
  4. Redirect ke halaman utama setelah tugas ditambahkan.  
- **Keamanan**: `user_id` secara otomatis dihubungkan dengan pengguna yang sedang login.

---

#### 3\. **Menghapus Tugas \- `delete_task`**

@main\_bp.route("/delete/\<int:task\_id\>")

@login\_required

def delete\_task(task\_id):

    task \= Task.query.get(task\_id)

    if task and task.user\_id \== current\_user.id:  \# Ensure the task belongs to the current user

        db.session.delete(task)

        db.session.commit()

    return redirect(url\_for("main\_bp.index"))

- **Deskripsi**:  
  Menghapus tugas berdasarkan `task_id`.  
- **Metode HTTP**: `GET`  
- **Proses**:  
  1. Mengambil tugas dari database berdasarkan `task_id`.  
  2. Memastikan tugas tersebut dimiliki oleh pengguna yang sedang login.  
  3. Menghapus tugas dari database jika valid.  
- **Keamanan**: Memverifikasi `user_id` untuk memastikan pengguna hanya dapat menghapus tugas miliknya.

---

#### 4\. **Mengedit Tugas \- `edit_task`**

@main\_bp.route("/edit/\<int:task\_id\>", methods=\["GET", "POST"\])

@login\_required

def edit\_task(task\_id):

    task \= Task.query.get(task\_id)

    if task and task.user\_id \== current\_user.id:  \# Ensure the task belongs to the current user

        if request.method \== "POST":

            task.name \= request.form.get("name")

            task.priority \= request.form.get("priority")

            task.date \= request.form.get("date")

            db.session.commit()

            return redirect(url\_for("main\_bp.index"))

        return render\_template("edit\_task.html", task=task)

    return redirect(url\_for("main\_bp.index"))

- **Deskripsi**:  
  Mengedit detail tugas berdasarkan `task_id`.  
- **Metode HTTP**: `GET`, `POST`  
- **Proses**:  
  - **GET**:  
    1. Mengambil tugas dari database berdasarkan `task_id`.  
    2. Memastikan tugas tersebut dimiliki oleh pengguna yang sedang login.  
    3. Menampilkan form untuk mengedit tugas di template `edit_task.html`.  
  - **POST**:  
    1. Mengambil data yang diubah dari form.  
    2. Memperbarui informasi tugas dalam database.  
    3. Redirect ke halaman utama setelah perubahan disimpan.  
- **Keamanan**: Memverifikasi `user_id` untuk memastikan pengguna hanya dapat mengedit tugas miliknya.

---

### **Keamanan yang Diterapkan**

1. **Login Required**: Semua rute hanya dapat diakses oleh pengguna yang sudah login (`@login_required`).  
2. **Validasi Kepemilikan Tugas**: Sebelum mengedit atau menghapus tugas, sistem memverifikasi bahwa tugas tersebut dimiliki oleh pengguna saat ini (`task.user_id == current_user.id`).

---

### **Modul: `register_blueprints`**

Fungsi `register_blueprints` digunakan untuk mendaftarkan **Blueprints** pada objek aplikasi Flask (`app`). Blueprints memungkinkan aplikasi Flask dipecah menjadi modul-modul kecil untuk mempermudah pengelolaan dan pengorganisasian kode.

---

### **Kode**

from flask import Flask  
from .main import main\_bp  
from .auth import auth\_bp

def register\_blueprints(app):  
    app.register\_blueprint(main\_bp)  
    app.register\_blueprint(auth\_bp)

---

### **Penjelasan**

1. **Imports**:

   * `Flask`: Framework untuk membangun aplikasi web.  
   * `main_bp`: Blueprint untuk modul fitur utama, diimpor dari file `main.py`.  
   * `auth_bp`: Blueprint untuk modul autentikasi, diimpor dari file `auth.py`.  
2. **Fungsi `register_blueprints(app)`**:

   * **Parameter**:  
     * `app`: Objek aplikasi Flask yang diinisialisasi di tempat lain dalam proyek.  
   * **Proses**:  
     * Mendaftarkan Blueprint `main_bp` untuk fitur utama aplikasi (misalnya, halaman utama, pengelolaan tugas, dll.).  
     * Mendaftarkan Blueprint `auth_bp` untuk fitur autentikasi (misalnya, login, register, logout).  
3. **`app.register_blueprint()`**:

   * Fungsi bawaan Flask untuk mendaftarkan **Blueprints** ke aplikasi Flask utama.  
   * Blueprint membantu membagi aplikasi menjadi modul-modul logis yang independen, tetapi tetap terintegrasi.

---

### **Blueprints yang Digunakan**

1. **`main_bp`**:

   * Mengelola rute untuk fitur utama aplikasi, seperti halaman tugas atau dashboard.  
   * Dideklarasikan di `main.py`.  
2. **`auth_bp`**:

   * Mengelola rute autentikasi, seperti login, registrasi, dan logout.  
   * Dideklarasikan di `auth.py`.

---

### **Keuntungan Menggunakan Blueprint**

1. **Modularitas**:

   * Membagi aplikasi menjadi bagian-bagian kecil sehingga lebih mudah dikelola.  
   * Memungkinkan pengembangan tim yang lebih terorganisir.  
2. **Reuse**:

   * Blueprint dapat digunakan kembali di aplikasi lain dengan kebutuhan serupa.  
3. **Skalabilitas**:

   * Mempermudah penambahan fitur baru tanpa memengaruhi arsitektur keseluruhan.

---
