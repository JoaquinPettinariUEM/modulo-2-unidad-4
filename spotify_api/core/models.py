from django.db import models

class SearchTypeEnum(models.TextChoices):
    ARTIST = "ARTIST", "Artist"
    TRACK = "TRACK", "Track"
    ALBUM = "ALBUM", "Album"

class ActionEnum(models.TextChoices):
    LIKE = "LIKE", "Like"
    SAVE = "SAVE", "Save"


class User(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    age = models.IntegerField()
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="searches")
    query = models.CharField(max_length=255, db_index=True)
    type = models.CharField(max_length=50, choices=SearchTypeEnum.choices)

    def __str__(self):
        return f"{self.user.name} - {self.query}"


class MusicAction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="music_actions")
    spotify_id = models.CharField(max_length=255, db_index=True)
    type = models.CharField(max_length=50, choices=SearchTypeEnum.choices)
    action = models.CharField(max_length=50, choices=ActionEnum.choices)

    def __str__(self):
        return f"{self.user.name} - {self.action} ({self.spotify_id})"
