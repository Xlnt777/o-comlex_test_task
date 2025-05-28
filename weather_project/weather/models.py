from django.db import models
from django.contrib.auth.models import User

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.CharField(max_length=100)
    count = models.PositiveIntegerField(default=1)
    last_searched = models.DateTimeField(auto_now=True)

    def str(self):
        return f"{self.city} ({self.count})"

class CitySearch(models.Model):
    name = models.CharField(max_length=100)
    count = models.PositiveIntegerField(default=1)

    def str(self):
        return f"{self.name} — {self.count}"