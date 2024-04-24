from django.db import models
from add_post.models import ApartmentUnit
from login.models import User


class Interest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    unit = models.ForeignKey(ApartmentUnit, on_delete=models.CASCADE)
    roommate_count = models.PositiveSmallIntegerField()
    move_in_date = models.DateField()
    likes = models.ManyToManyField(User, related_name='liked_interests', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_interests', blank=True)

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()