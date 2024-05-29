from django.db import models

class Presentation(models.Model):
    title = models.TextField("Назва презентації", max_length=500)
    author = models.TextField("Автор", max_length=250)
    notes = models.TextField("Примітки",max_length=500)
    time = models.DateTimeField("Час отримання")
    link = models.TextField("Посилання на презентацію")
    rating = models.TextField("Оцінка", default="")
    group = models.TextField("Група", max_length=2500)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/database'
