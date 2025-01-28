from typing import Any

from django.core.management.base import BaseCommand





class Command(BaseCommand):
    
    help="THis commands inserts categorydata  data" 
    def handle(self, *args: Any, **options: Any):
        from  adminpanel.models import words
        #deleting existing data
        words.objects.all().delete()

        name=["snake",'frog',"horse","pig","tree"]
        
        image=["https://picsum.photos/id/1/200/300","https://picsum.photos/id/2/200/300",
               "https://picsum.photos/id/3/200/300","https://picsum.photos/id/4/200/300","https://picsum.photos/id/5/200/300"]
        for name,image in zip(name,image):
            words.objects.create(name=name,image=image)
        self.stdout.write(self.style.SUCCESS("completed inserting data"))    


        
        
        

       
   
       
       
       