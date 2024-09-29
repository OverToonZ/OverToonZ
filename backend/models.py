from django.db import models
from django.utils import timezone
from datetime import timedelta,datetime
from django.contrib.auth.models import AbstractUser
from django_mysql.models import ListCharField
import pytz

def IST_time():
    ist = pytz.timezone('Asia/Kolkata')
    return timezone.now().astimezone(ist)
    
class User(AbstractUser):
    email = models.EmailField(max_length=100,unique=True)
    favourite_anime = models.CharField(max_length=100,default='NaN')
    login_count = models.IntegerField(default=0)
    last_login = models.DateTimeField(default=IST_time)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=['username']

    def Updated_time(self):
        now = IST_time()
        delta = now - self.last_login
        days = delta.days
        seconds = delta.seconds

        if days == 0:
            if seconds < 60:
                return "Just now"
            elif seconds < 3600:
                minutes = seconds // 60
                return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
            else:
                hours = seconds // 3600
                return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif days == 1:
            return "Yesterday"
        else:
            return f"{days} days ago"

  

class AnimeInfo(models.Model):
    title = models.CharField(max_length=50)
    img_src = models.URLField(max_length=350)
    studio = models.CharField(max_length=50)
    seasons = models.IntegerField(default=1)
    episodes = models.IntegerField(default=0)
    avail_lang = models.CharField(max_length=5)
    rating = models.DecimalField(max_digits=3,decimal_places=1)
    status = models.CharField(max_length=15)
    updated = models.DateTimeField(default=IST_time)
    description = models.CharField(max_length=1000,default="")
    banner = models.URLField(max_length=350,default="")
    genre = ListCharField(
        base_field=models.CharField(max_length=10),
        size=6,
        max_length=(6 * 11),
    )
    def Updated_time(self):
        now = IST_time()
        delta = now - self.updated
        days = delta.days
        seconds = delta.seconds

        if days == 0:
            if seconds < 60:
                return "Just now"
            elif seconds < 3600:
                minutes = seconds // 60
                return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
            else:
                hours = seconds // 3600
                return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif days == 1:
            return "Yesterday"
        else:
            return f"{days} days ago"

    def __str__(self):
        return self.title

class SeasonInfo(models.Model):
    # anime = models.CharField(max_length=100)
    anime = models.ForeignKey(AnimeInfo, on_delete=models.CASCADE, related_name='seasons_model')
    season_count = models.IntegerField(default=1)
    episode_count = models.IntegerField(default=1)
    season_title = models.CharField(max_length=100)
    season_cover = models.URLField(max_length=350)
    season_banner = models.URLField(max_length=350)
    status = models.CharField(max_length = 15)
    updatedon = models.DateTimeField(default=IST_time)
    def Updated_time(self):
        now = IST_time()
        delta = now - self.updatedon
        days = delta.days
        seconds = delta.seconds

        if days == 0:
            if seconds < 60:
                return "Just now"
            elif seconds < 3600:
                minutes = seconds // 60
                return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
            else:
                hours = seconds // 3600
                return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif days == 1:
            return "Yesterday"
        else:
            return f"{days} days ago"

    def __str__(self):
        return (self.anime.title +" S0"+str(self.season_count))
    

class EpisodesInfo(models.Model):
    # anime = models.CharField(max_length=100)
    # season = models.IntegerField(default=1)
    anime = models.ForeignKey(AnimeInfo, on_delete=models.CASCADE, related_name='episodes_model')
    season = models.ForeignKey(SeasonInfo, on_delete=models.CASCADE, related_name='episodes_model', null=True, blank=True)
    episode = models.IntegerField(default=1)
    static_count = models.IntegerField(default=1)
    code = models.CharField(max_length=8,default='S01EP01')
    episode_title = models.CharField(max_length=100)
    episode_cover = models.URLField(max_length=350)
    views =  models.IntegerField(default=0)
    episode_link = models.URLField(max_length=350)

    def __str__(self):
        return f"{self.anime.title}  -  {self.code}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='comments')
    commenttype = models.CharField(max_length=55)
    visibility = models.CharField(max_length=10)
    comment = models.TextField()
    reply = models.JSONField(default=dict,blank=True, null=True)
    created_at = models.DateTimeField(default=IST_time)
    isedited = models.BooleanField(default=False)

    def Updated_time(self):
        now = IST_time()
        delta = now - self.created_at
        days = delta.days
        seconds = delta.seconds

        if days == 0:
            if seconds < 60:
                return "Just now"
            elif seconds < 3600:
                minutes = seconds // 60
                return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
            else:
                hours = seconds // 3600
                return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif days == 1:
            return "Yesterday"
        else:
            return f"{days} days ago"

    def __str__(self):
        return f"{self.user.username} on {self.created_at}"

class Top_picks(models.Model):
     anime = models.ForeignKey(AnimeInfo, on_delete=models.CASCADE, related_name='animepicks')
     place = models.IntegerField(default=0)

     def __str__(self):
         return f"{self.anime.title}  -  {self.place}"
     
class Storages(models.Model):
    username = models.CharField(max_length=25)
    email = models.EmailField(default=None)
    passkey = models.CharField(max_length=20)
    recoverykey = models.CharField(max_length=50)
    storagetype = models.CharField(max_length=10)
    files = models.JSONField(default=dict,blank=True, null=True)
    occupiedsize = models.DecimalField(max_digits=3,decimal_places=1)
    availsize = models.DecimalField(max_digits=3,decimal_places=1)
    totalsize = models.DecimalField(max_digits=3,decimal_places=1)

    def __str__(self):
        return f"{self.username} - {self.email}"


