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
