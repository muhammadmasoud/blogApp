from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# =============================================================================
# USER MODELS
# =============================================================================

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_blocked = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username


# =============================================================================
# CONTENT MODELS
# =============================================================================

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    publish_date = models.DateTimeField(default=timezone.now)
    
    # Relationships
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Auto-delete if dislikes > 10
        if self.dislikes > 10:
            self.delete()
            return
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-publish_date']


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Relationships
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.username}: {self.content[:50]}...'
    
    def save(self, *args, **kwargs):
        # Filter forbidden words
        forbidden_words = ForbiddenWord.objects.values_list('word', flat=True)
        for word in forbidden_words:
            if word.lower() in self.content.lower():
                self.content = self.content.replace(word, '*' * len(word))
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-created_at']


# =============================================================================
# INTERACTION MODELS
# =============================================================================

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.user.username} -> {self.category.name}'
    
    class Meta:
        unique_together = ('user', 'category')


class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    is_like = models.BooleanField()  # True = like, False = dislike
    
    def __str__(self):
        action = "liked" if self.is_like else "disliked"
        return f'{self.user.username} {action} {self.post.title}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update post counters
        self.post.likes = PostLike.objects.filter(post=self.post, is_like=True).count()
        self.post.dislikes = PostLike.objects.filter(post=self.post, is_like=False).count()
        self.post.save()
    
    class Meta:
        unique_together = ('user', 'post')


# =============================================================================
# ADMIN MODELS
# =============================================================================

class ForbiddenWord(models.Model):
    word = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.word
