from typing import Any

from django.core.management.base import BaseCommand





class Command(BaseCommand):
    
    help="THis commands inserts categorydata  data" 
    def handle(self, *args: Any, **options: Any):
        from  adminpanel.models import profile
        #deleting existing data
        profile.objects.all().delete()

        names=["bharathkumar"]
        ages=[20]

        contents=["i am web developer"]
             
        emails=["hellojiohellojio@gmail.com"]
        addresss=['vellore']
        images=["https://picsum.photos/id/1/200/300"]
        for name,age,content,address,image,email in zip(names,ages,contents,addresss,images,emails):
            profile.objects.create(Name=name,age=age,content=content,address=address,image=image,email=email)
        self.stdout.write(self.style.SUCCESS("completed inserting data"))    


        
        
        

       
   
       
       
        