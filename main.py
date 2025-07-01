import tkinter as tk
from tkinter import messagebox, ttk
from veritabani import create_tables, create_connection, add_personnel_to_db, get_all_personnel
from kullanici import Admin, User, Guest

def db_register(username, password, role):
    try:
        conn = create_connection()
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

def db_login(username, password):
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user

class HRMSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("İnsan Kaynakları Yönetim Sistemi")
        self.root.geometry("900x650")
        self.root.resizable(True, True)
        self.root.configure(bg="#e8f0fe")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Helvetica", 12), padding=6)
        self.style.configure("TLabel", font=("Helvetica", 12), background="#e8f0fe")
        self.style.configure("Header.TLabel", font=("Helvetica", 16, "bold"), background="#e8f0fe", foreground="#2b6cb0")
        self.style.configure("TEntry", font=("Helvetica", 12))

        self.current_user = None
        self.frame = ttk.Frame(self.root, padding=20)
        self.frame.pack(fill="both", expand=True)

        self.show_main()

    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def show_main(self):
        self.clear_frame()

        ttk.Label(self.frame, text="İK Yönetim Sistemine Hoş Geldiniz", style="Header.TLabel").pack(pady=20)

        ttk.Button(self.frame, text="Giriş Yap", command=self.show_login).pack(pady=10, fill="x")
        ttk.Button(self.frame, text="Kayıt Ol", command=self.show_register).pack(pady=10, fill="x")
        ttk.Button(self.frame, text="Guest Olarak Devam Et", command=self.show_guest).pack(pady=10, fill="x")
        ttk.Button(self.frame, text="Çıkış", command=self.root.quit).pack(pady=10, fill="x")

    def show_login(self):
        self.clear_frame()

        box = ttk.LabelFrame(self.frame, text="Kullanıcı Girişi", padding=20)
        box.pack(fill="both", expand=True, pady=20)

        ttk.Label(box, text="Kullanıcı Adı:").pack(anchor="w", pady=5)
        self.username_entry = ttk.Entry(box, width=30)
        self.username_entry.pack(pady=5)

        ttk.Label(box, text="Şifre:").pack(anchor="w", pady=5)
        self.password_entry = ttk.Entry(box, show="*", width=30)
        self.password_entry.pack(pady=5)

        ttk.Button(box, text="Giriş Yap", command=self.login).pack(pady=15)
        ttk.Button(box, text="Geri", command=self.show_main).pack()

    def show_register(self):
        self.clear_frame()

        box = ttk.LabelFrame(self.frame, text="Yeni Kullanıcı Kaydı", padding=20)
        box.pack(fill="both", expand=True, pady=20)

        ttk.Label(box, text="Yeni Kullanıcı Adı:").pack(anchor="w", pady=5)
        self.reg_username = ttk.Entry(box, width=30)
        self.reg_username.pack(pady=5)

        ttk.Label(box, text="Yeni Şifre:").pack(anchor="w", pady=5)
        self.reg_password = ttk.Entry(box, show="*", width=30)
        self.reg_password.pack(pady=5)

        ttk.Label(box, text="Rol (admin/user):").pack(anchor="w", pady=5)
        self.reg_role = ttk.Entry(box, width=30)
        self.reg_role.pack(pady=5)

        ttk.Button(box, text="Kayıt Ol", command=self.register).pack(pady=15)
        ttk.Button(box, text="Geri", command=self.show_main).pack()

    def show_guest(self):
        self.clear_frame()

        self.current_user = Guest()

        box = ttk.LabelFrame(self.frame, text="Guest Girişi", padding=20)
        box.pack(fill="both", expand=True, pady=20)

        ttk.Label(box, text="Guest olarak sisteme giriş yaptınız.", style="Header.TLabel").pack(pady=10)
        ttk.Label(box, text="Sisteme sınırlı erişim sağlıyorsunuz.").pack(pady=5)

        ttk.Button(box, text="Geri", command=self.show_main).pack(pady=15)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_data = db_login(username, password)

        if user_data:
            role = user_data[3]
            if role == "admin":
                self.current_user = Admin(user_data[0], user_data[1])
                self.current_user.kaydet_islem("Admin olarak giriş yaptı")
                self.show_admin_menu()
            elif role == "user":
                self.current_user = User(user_data[0], user_data[1])
                self.current_user.kaydet_islem("User olarak giriş yaptı")
                self.show_user_menu()
        else:
            messagebox.showerror("Hata", "Geçersiz kullanıcı adı veya şifre.")

    def register(self):
        username = self.reg_username.get()
        password = self.reg_password.get()
        role = self.reg_role.get().lower()

        if role not in ["admin", "user"]:
            messagebox.showerror("Hata", "Rol admin veya user olmalıdır.")
            return

        if db_register(username, password, role):
            messagebox.showinfo("Başarılı", "Kayıt başarılı!")
            self.show_main()
        else:
            messagebox.showerror("Hata", "Kayıt başarısız!")

    def show_admin_menu(self):
        self.clear_frame()

        ttk.Label(self.frame, text=f"Hoş geldiniz, {self.current_user.username} (Admin)", style="Header.TLabel").pack(pady=20)

        ttk.Button(self.frame, text="İşlem Geçmişini Görüntüle", command=self.show_admin_logs).pack(pady=10, fill="x")
        ttk.Button(self.frame, text="Personel Ekle", command=self.show_add_personnel).pack(pady=10, fill="x")
        ttk.Button(self.frame, text="Personel Listesi", command=self.show_personnel_list).pack(pady=10, fill="x")
        ttk.Button(self.frame, text="Çıkış Yap", command=self.show_main).pack(pady=10, fill="x")

    def show_admin_logs(self):
        self.clear_frame()

        ttk.Label(self.frame, text="İşlem Geçmişi", style="Header.TLabel").pack(pady=15)

        records = self.current_user.tum_islemleri_gor()

        if records:
            self.create_table_view(self.frame, records, columns=("ID", "Kullanıcı", "İşlem", "Zaman"))
        else:
            ttk.Label(self.frame, text="Kayıt bulunamadı.").pack(pady=10)

        ttk.Button(self.frame, text="Geri", command=self.show_admin_menu).pack(pady=10)

    def show_add_personnel(self):
        self.clear_frame()

        box = ttk.LabelFrame(self.frame, text="Yeni Personel Kaydı", padding=20)
        box.pack(fill="both", expand=True, pady=20)

        ttk.Label(box, text="Adı:").pack(anchor="w", pady=5)
        self.pers_name_entry = ttk.Entry(box, width=30)
        self.pers_name_entry.pack(pady=5)

        ttk.Label(box, text="Pozisyon:").pack(anchor="w", pady=5)
        self.pers_position_entry = ttk.Entry(box, width=30)
        self.pers_position_entry.pack(pady=5)

        ttk.Label(box, text="Maaş (₺):").pack(anchor="w", pady=5)
        self.pers_salary_entry = ttk.Entry(box, width=30)
        self.pers_salary_entry.pack(pady=5)

        ttk.Button(box, text="Kaydet", command=self.save_personnel).pack(pady=15)
        ttk.Button(box, text="Geri", command=self.show_admin_menu).pack()

    def save_personnel(self):
        name = self.pers_name_entry.get().strip()
        position = self.pers_position_entry.get().strip()
        salary = self.pers_salary_entry.get().strip()

        if not name or not position or not salary:
            messagebox.showerror("Hata", "Tüm alanlar doldurulmalıdır!")
            return

        try:
            salary = float(salary)
        except ValueError:
            messagebox.showerror("Hata", "Maaş sayısal bir değer olmalıdır!")
            return

        success = add_personnel_to_db(name, position, salary)

        if success:
            messagebox.showinfo("Başarılı", f"Personel eklendi:\n{name} - {position} - ₺{salary:.2f}")
            self.show_admin_menu()
        else:
            messagebox.showerror("Hata", "Personel eklenemedi!")

    def show_personnel_list(self):
        self.clear_frame()

        ttk.Label(self.frame, text="Personel Listesi", style="Header.TLabel").pack(pady=15)

        records = get_all_personnel()
        if records:
            formatted = [(r[0], r[1], r[2], f"₺{r[3]:,.2f}") for r in records]
            self.create_table_view(self.frame, formatted, columns=("ID", "Adı", "Pozisyon", "Maaş"))
        else:
            ttk.Label(self.frame, text="Personel kaydı bulunamadı.").pack(pady=10)

        ttk.Button(self.frame, text="Geri", command=self.show_admin_menu).pack(pady=10)

    def create_table_view(self, parent, data, columns):
        table_frame = ttk.Frame(parent)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", stretch=True)

        for row in data:
            tree.insert("", tk.END, values=row)

        scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        scrollbar_y.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar_y.set)

        tree.pack(side="left", fill="both", expand=True)

    def show_user_menu(self):
        self.clear_frame()

        ttk.Label(self.frame, text=f"Hoş geldiniz, {self.current_user.username} (User)", style="Header.TLabel").pack(pady=20)

        box = ttk.LabelFrame(self.frame, text="İşlem Kaydı", padding=20)
        box.pack(fill="both", expand=True, pady=20)

        ttk.Label(box, text="İşlem Açıklaması:").pack(anchor="w", pady=5)
        self.user_action_entry = ttk.Entry(box, width=30)
        self.user_action_entry.pack(pady=5)

        ttk.Button(box, text="İşlem Kaydet", command=self.save_user_action).pack(pady=15)
        ttk.Button(box, text="Çıkış Yap", command=self.show_main).pack()

    def save_user_action(self):
        action = self.user_action_entry.get()
        if not action:
            messagebox.showerror("Hata", "İşlem açıklaması boş olamaz!")
            return

        success, msg = self.current_user.kaydet_islem(action)
        if success:
            messagebox.showinfo("Başarılı", msg)
            self.show_user_menu()
        else:
            messagebox.showerror("Hata", msg)


if __name__ == "__main__":
    create_tables()
    root = tk.Tk()
    app = HRMSApp(root)
    root.mainloop()


