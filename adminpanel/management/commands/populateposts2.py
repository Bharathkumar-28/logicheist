from typing import Any

from django.core.management.base import BaseCommand





class Command(BaseCommand):
    
    help="THis commands inserts categorydata  data" 
    def handle(self, *args: Any, **options: Any):
        from  adminpanel.models import profile
        #deleting existing data
        profile.objects.all().delete()

        Name=["bharathkumar"]
        age=[20]

        content=["i am web developer"]
             
        
        address=['vellore']
        image=["https://picsum.photos/id/1/200/300"]
        for name,age,content,address,image in zip(Name,age,content,address,image):
            profile.objects.create(Name=Name,age=age,content=content,address=address,image=image)
        self.stdout.write(self.style.SUCCESS("completed inserting data"))    


        
        
        

       
   
       
       
        