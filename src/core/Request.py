# src/core/Request.py

class Request:
    """
    نماینده یک درخواست HTTP دریافتی.
    در آینده، داده‌های سرور WSGI را به این شیء می‌بندیم.
    """
    def __init__(self, environ=None):
        # 'environ' دیکشنری‌ای است که سرور WSGI حاوی تمام اطلاعات درخواست به ما می‌دهد.
        self.environ = environ if environ is not None else {}
        self.method = self.environ.get('REQUEST_METHOD', 'GET')
        self.path = self.environ.get('PATH_INFO', '/')
        self.query_string = self.environ.get('QUERY_STRING', '')
        
        # برای نمایش ساده فعلی
        print(f"Request دریافت شد: {self.method} {self.path}")

    @property
    def url(self):
        """آدرس URL کامل درخواست."""
        if self.query_string:
            return f"{self.path}?{self.query_string}"
        return self.path
