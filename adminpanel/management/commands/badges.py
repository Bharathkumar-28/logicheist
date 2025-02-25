from typing import Any

from django.core.management.base import BaseCommand
from django.utils.text import slugify
import random



class Command(BaseCommand):
    
    help="THis commands insets post data" 
    def handle(self, *args: Any, **options: Any):
        from  adminpanel.models import badges
        #deleting existing data
        badges.objects.all().delete()

        
        
        

        names=[

"Legend League ",
"Titan League",
"Champion League",
"Master League",
"Crystal League",
"Gold League",  
"Silver League",
"Bronze League "

   






]
        scores=[
  
70,60,50,40,30,20,10,1


]
        images=[
            "https://tse1.mm.bing.net/th?id=OIP.hci-If8wGw5BLfychV7EwAAAAA&pid=Api&P=0&h=180",
            "https://tse4.mm.bing.net/th?id=OIP.SwFV15LmUahtcr9DfHJnQgAAAA&pid=Api&P=0&h=180",
            "https://tse4.mm.bing.net/th?id=OIP.lWPLrkot7cgFIILUrJFMjQAAAA&pid=Api&P=0&h=180",
            "https://tse3.mm.bing.net/th?id=OIP.D7OqWEE-E99YdRuSgc0eswAAAA&pid=Api&P=0&h=180",
           " https://tse2.mm.bing.net/th?id=OIP._ZJk1GFXqVtn3vtyLr_IwgAAAA&pid=Api&P=0&h=180",
            "https://tse4.mm.bing.net/th?id=OIP.pf8UrxF6ktEMOwctAUnvOwHaHa&pid=Api&P=0&h=180",
            "https://tse1.mm.bing.net/th?id=OIP.uIrc7PzvUeRM0MMBz0vtxwHaHa&pid=Api&P=0&h=180",
  "https://tse3.mm.bing.net/th?id=OIP.3op0UjjIp-woaHF-G2-_7gAAAA&pid=Api&P=0&h=180"
   
    
]
      
        for title,content,imgurl in zip(names,scores,images,):
       
            badges.objects.create(name=title,score=content,image=imgurl)
       
        self.stdout.write(self.style.SUCCESS("completed inserting data"))
