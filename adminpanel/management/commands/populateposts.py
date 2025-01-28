from typing import Any

from django.core.management.base import BaseCommand
from django.utils.text import slugify
import random



class Command(BaseCommand):
    
    help="THis commands insets post data" 
    def handle(self, *args: Any, **options: Any):
        from  adminpanel.models import post
        #deleting existing data
        post.objects.all().delete()

        
        
        

        titles=[
"power OF ME ",
"onlineeducation SYSTEM",
"CRICKET IS MY WORLD",   
"globaL WARMING AND ITS IMPACTS",
"thearT OF SOCIAL MEDIA",
"evolution OF HUMANS",
"medical HISTORY",
"cultural PROGRAMS IN COLLEGES",
"sustainable DEVELOPMENT",
"FOOTBALL AND ITS GROWTH"

]
        content=[
  
         "power OF ME ",
"onlineeducation SYSTEM",
"CRICKET IS MY WORLD",   
"globaL WARMING AND ITS IMPACTS",
"thearT OF SOCIAL MEDIA",
"evolution OF HUMANS",
"medical HISTORY",
"cultural PROGRAMS IN COLLEGES",
"sustainable DEVELOPMENT",
"FOOTBALL AND ITS GROWTH"    


]
        img=[
    "https://picsum.photos/id/1/200/300",
     "https://picsum.photos/id/2/200/300",
      "https://picsum.photos/id/3/200/300",
       "https://picsum.photos/id/4/200/300",
        "https://picsum.photos/id/5/200/300",
         "https://picsum.photos/id/6/200/300",
          "https://picsum.photos/id/7/200/300",
           "https://picsum.photos/id/8/200/300",
            "https://picsum.photos/id/9/200/300",
             "https://picsum.photos/id/10/200/300",
   
    
]
      
        for title,content,imgurl in zip(titles,content,img,):
       
            post.objects.create(title=title,content=content,image=imgurl)
       
        self.stdout.write(self.style.SUCCESS("completed inserting data"))
