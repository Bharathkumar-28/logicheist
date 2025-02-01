from typing import Any

from django.core.management.base import BaseCommand





class Command(BaseCommand):
    
    help="THis commands inserts categorydata  data" 
    def handle(self, *args: Any, **options: Any):
        from  adminpanel.models import words
        #deleting existing data
        words.objects.all().delete()


        name=["snake",'frog',"horse","pig","tree",'dog',"bird",'eagle',"cricket",'football']
<<<<<<< HEAD
                                           
=======


        
>>>>>>> 2b53b6f05a7b6025940e5b382fcae469052ad911
        image=["https://tse3.mm.bing.net/th?id=OIP.RL0ZKNoaDbaPGzZkuAdHAwHaHa&pid=Api&P=0&h=180","https://tse4.mm.bing.net/th?id=OIP.Bq6pyy9PsKGHa48VFeUtoQHaFj&pid=Api&P=0&h=180",
               "https://tse2.mm.bing.net/th?id=OIP.l5MlccMpovMVFgb3H5dQdgHaGO&pid=Api&P=0&h=180","https://tse3.mm.bing.net/th?id=OIP.EzJrrZwrVWEpOX4P9nI-vgHaIw&pid=Api&P=0&h=180","https://tse3.mm.bing.net/th?id=OIP.GkMD2FBlCrgUQjlEvqLGtwHaH8&pid=Api&P=0&h=180",
               "https://tse2.mm.bing.net/th?id=OIP.ZfuC4RnPRyyKHJ9co6w-PQHaFS&pid=Api&P=0&h=180","https://tse3.mm.bing.net/th?id=OIP.yKJsIdxjAg8xnLaLBIpOYgHaGO&pid=Api&P=0&h=180",
              " https://tse2.mm.bing.net/th?id=OIP.LtcnlLNGtUss3KuEmY0DgwHaKX&pid=Api&P=0&h=180","https://tse4.mm.bing.net/th?id=OIP._ZNJxChTg2V99-H7LSfJEgHaFN&pid=Api&P=0&h=180","https://tse1.mm.bing.net/th?id=OIP.8hnmXmBVq69thugiyPnGBAHaHa&pid=Api&P=0&h=180"]
        for name,image in zip(name,image):
            words.objects.create(name=name,image=image)
        self.stdout.write(self.style.SUCCESS("completed inserting data"))  


        
        
        

       
   
       
       
       