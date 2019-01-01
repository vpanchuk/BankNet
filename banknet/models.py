from django.db import models

class Rating(models.Model):
    full_name = models.CharField(max_length=255)
    term = models.PositiveSmallIntegerField()
    volume = models.PositiveIntegerField()
    risk_level = models.PositiveSmallIntegerField()
    credit_history = models.BooleanField()
    wages = models.PositiveIntegerField()
    rating = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.full_name