from django.db import models

class Interest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    unit = models.ForeignKey(ApartmentUnit, on_delete=models.CASCADE)
    roommate_count = models.PositiveSmallIntegerField()
    move_in_date = models.DateField()
