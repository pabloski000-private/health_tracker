from django.db import models

class WeightEntry(models.Model):
    client_id = models.CharField(max_length=64, db_index=True)
    date = models.DateField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ("client_id", "date")

    def __str__(self):
        return f"{self.client_id} {self.date}: {self.weight} kg"