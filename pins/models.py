from django.db import models
from django.contrib.auth.models import User
from boards.models import Board

class Pin(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='pins/')
    board = models.ForeignKey(Board, on_delete=models.CASCADE,related_name="pins")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pins')  # Only this one!
    saved_by = models.ManyToManyField(
        User,
        related_name='saved_pins',
        blank=True
    )

    def __str__(self):
        return self.title

class Comment(models.Model):
    pin = models.ForeignKey('Pin', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.text[:20]}"


class Like(models.Model):
    pin = models.ForeignKey('Pin', on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_pins')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('pin', 'user')  

    def __str__(self):
        return f"{self.user.username} liked {self.pin.title}"
