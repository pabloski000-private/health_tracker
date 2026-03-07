from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class WeightEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="weights")
    date = models.DateField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ("user", "date")

    def __str__(self):
        return f"{self.user} {self.date}: {self.weight} kg"