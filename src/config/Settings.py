
# src/config/Settings.py

class Settings:
    """
    مدیریت تنظیمات سراسری فریم‌ورک YesWeb.
    """
    def __init__(self, user_settings=None):
        # تنظیمات پیش‌فرض فریم‌ورک
        self.DEBUG = False
        self.SECRET_KEY = "insecure-default-key" # باید در پروژه واقعی تغییر کند
        self.INSTALLED_APPS = [] # لیست ماژول‌های برنامه
        self.DEFAULT_HOST = '127.0.0.1'
        self.DEFAULT_PORT = 8000
        
        # اگر تنظیماتی از طرف کاربر (پروژه) داده شده باشد، تنظیمات پیش‌فرض را بازنویسی می‌کند.
        if user_settings:
            for key, value in user_settings.items():
                # از setattr استفاده می‌کنیم تا به طور داینامیک صفت (attribute) را اضافه کنیم.
                setattr(self, key, value)
                
    def __getattr__(self, name):
        """
        این متد زمانی فراخوانی می‌شود که صفت مورد نظر پیدا نشود.
        برای جلوگیری از خطا، یک پیام مناسب می‌دهیم.
        """
        raise AttributeError(f"تنظیمات '{name}' در YesWeb تعریف نشده است.")

    def as_dict(self):
        """بازگرداندن تنظیمات به صورت یک دیکشنری ساده."""
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
