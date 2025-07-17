from django.db import models

# Create your models here.

#CATEGORIES: referring to different post categories
class Category (models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Post (models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='post', blank=True, null=True)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(
        Category,
        on_delete= models.SET_NULL, #Will set the category of post no null if it is delelted
        related_name='posts', #All posts under that category in reverse relationship
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    #Order descendingly by likes and creation date 
    class Meta:
        ordering = ['-likes', '-created_at']

    def __str__(self):
        return self.title

    
