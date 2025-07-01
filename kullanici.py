from veritabani import create_connection
from datetime import datetime

def log(mesaj):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] {mesaj}")

class Kullanici:
    """
    Tüm kullanıcı tiplerinin temel sınıfı.
    Kullanıcı ID, isim ve rol bilgisi içerir.
    """
    def __init__(self, user_id, username, role):
        self.user_id = user_id
        self.username = username
        self.role = role
        log(f"Kullanici nesnesi oluşturuldu: {self}")

    def __str__(self):
        return f"{self.username} ({self.role})"

    def kaydet_islem(self, islem_aciklama):
        """
        Kullanıcının yaptığı işlemi işlem_kaydi tablosuna yazar.
        """
        try:
            conn = create_connection()
            c = conn.cursor()
            c.execute('''
                INSERT INTO işlem_kaydi (user_id, işlem)
                VALUES (?, ?)
            ''', (self.user_id, islem_aciklama))
            conn.commit()
            conn.close()
            log(f"İşlem kaydedildi: {self.username} - {islem_aciklama}")
            return True, "İşlem başarıyla kaydedildi."
        except Exception as e:
            log(f"Hata işlem kaydında: {e}")
            return False, f"Hata: {e}"

class Admin(Kullanici):
    """
    Admin yetkisine sahip kullanıcı sınıfı.
    İşlem geçmişini görebilir.
    """
    def __init__(self, user_id, username):
        super().__init__(user_id, username, 'admin')
        log(f"Admin oturumu açıldı: {self}")

    def tum_islemleri_gor(self):
        """
        Tüm işlem kayıtlarını görüntüler.
        """
        try:
            conn = create_connection()
            c = conn.cursor()
            c.execute('''
                SELECT i.id, u.username, i.işlem, i.timestamp
                FROM işlem_kaydi i
                JOIN users u ON i.user_id = u.id
                ORDER BY i.timestamp DESC
            ''')
            rows = c.fetchall()
            conn.close()
            log(f"Admin işlem geçmişini görüntüledi. Kayıt sayısı: {len(rows)}")
            return rows
        except Exception as e:
            log(f"Hata işlem geçmişinde: {e}")
            return []

class User(Kullanici):
    """
    Standart kullanıcı sınıfı.
    Sadece işlem kaydı ekleyebilir.
    """
    def __init__(self, user_id, username):
        super().__init__(user_id, username, 'user')
        log(f"User oturumu açıldı: {self}")

class Guest(Kullanici):
    """
    Guest (ziyaretçi) sınıfı – sınırlı erişim.
    İşlem kaydı tutulmaz.
    """
    def __init__(self):
        super().__init__(user_id=None, username='Guest', role='guest')
        log("Guest kullanıcı oluşturuldu.")



