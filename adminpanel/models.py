from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
# Create your models here.
 
class post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField( null=True,upload_to='posts/images',blank=True)
    createdate = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, max_length=150,db_index=True)
    
    
  

    
        

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

            # Ensure slug is unique
            original_slug = self.slug
            queryset = post.objects.filter(slug=self.slug)

            # If the slug already exists, modify it by appending a number
            if queryset.exists():
                self.slug = f"{original_slug}-{queryset.count() + 1}"

            super().save(*args, **kwargs)
    @property        
    def formattedimgurl(self):
         url=self.image if self.image.__str__().startswith(('http','https://')) else self.image.url
         return url
    def __str__(self):
            return self.title
class profile(models.Model):
     Name=models.CharField(max_length=100)
     email=models.EmailField()
     image=models.ImageField(max_length=100)  
     age=models.PositiveIntegerField()  
     content=models.CharField(max_length=100) 
     address=models.CharField(max_length=100) 
     user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
     
     @property        
     def formattedimgurl(self):
        url=self.image if self.image.__str__().startswith(('http','https://')) else self.image.url
        return url
    
      
class words(models.Model):
     name=models.CharField(max_length=100) 
     image=models.ImageField(max_length=100)
     @property        
     def formattedimgurl(self):
        url=self.image if self.image.__str__().startswith(('http','https://')) else self.image.url
        return url
# models.py


class gameresult(models.Model):
    word = models.CharField(max_length=100)
    correctanswer = models.CharField(max_length=100)
    useranswer = models.CharField(max_length=100)
    iscorrect = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"Word: {self.word}, Correct: {self.iscorrect}"
class gameresult2(models.Model):
    iscorrect = models.JSONField(default=list)  
    word=models.CharField(max_length=100,null=True)


class quiz(models.Model):
    name=models.CharField(max_length=100,null=True)
    title = models.CharField(max_length=100,null=True)
    content = models.TextField(null=True)
    image = models.ImageField( null=True,upload_to='posts/images',blank=True)
    createdate = models.DateTimeField(auto_now_add=True,null=True)
    week=models.CharField(null=True,max_length=100)
    data = models.JSONField(null=True, blank=True) 
    @property        
    def formattedimgurl(self):
        url=self.image if self.image.__str__().startswith(('http','https://')) else self.image.url
        return url
from django.db import models
import json

class courses(models.Model):
    name = models.CharField(max_length=255,null=True)
    title = models.CharField(max_length=255,null=True)
    image = models.ImageField(upload_to='courses/', null=True, blank=True)
    data = models.JSONField(null=True, blank=True)  # Assuming you're storing word-image pairs in JSON format

    def formattedimgurl(self):
        if self.image and hasattr(self.image, 'url'):
            if self.image.url.startswith(('http', 'https://')):
                return self.image.url
            else:
                return self.image.url
        return None


class  leaderboard(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    data=models.JSONField(null=True,blank=True)
class notes(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    data=models.JSONField(null=True,blank=True)

class speechquiz2(models.Model):
   
   
    title=models.CharField(max_length=100,null=True)
    name=models.CharField(max_length=100,null=True)
    image=models.ImageField(null=True,upload_to='posts/images',blank=True)
    data=models.JSONField(null=True,blank=True)
    @property        
    def formattedimgurl(self):
        url=self.image if self.image.__str__().startswith(('http','https://')) else self.image.url
        return url

from django.contrib.auth.models import User

class UserActivity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    last_active = models.DateTimeField(auto_now=True)  # Automatically updated when user is active

    def __str__(self):
        return self.user.username
class badges(models.Model):
    name=models.CharField(max_length=100,null=True)
    image=models.ImageField(null=True)
    score=models.IntegerField(null=True)        
    @property        
    def formattedimgurl(self):
        url=self.image if self.image.__str__().startswith(('http','https://')) else self.image.url
        return url

from django.db import models

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='images/')  # Store the image file in the 'images' directory
    extracted_text = models.TextField(blank=True, null=True)  # Store the extracted text

    def __str__(self):
        return f"Image {self.id} - Extracted Text"  # For easy identification in the admin interface


        

     
