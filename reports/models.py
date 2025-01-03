from django.db import models

class Report(models.Model):
  title = models.CharField(max_length=255, verbose_name="العنوان")
  created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
  content = models.TextField(verbose_name="المحتوى")

  def __str__(self):
    return self.title