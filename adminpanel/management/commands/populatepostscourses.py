from typing import Any

from django.core.management.base import BaseCommand





class Command(BaseCommand):
    
    help="THis commands inserts categorydata  data" 
    def handle(self, *args: Any, **options: Any):
        from  adminpanel.models import courses
        #deleting existing data
        courses.objects.all().delete()


        
        names=[
"animal","Bird"
]
        content=[
  
         "power OF animals ",
           "power OF bird "
]
   
        img=[
    "https://picsum.photos/id/1/200/300",
     "https://picsum.photos/id/1/200/300",
]
       
  
        for named,title,image in zip(names,content,img):
            courses.objects.create(
             # Example name for the category
            data={"robot":"https://c.tenor.com/CigpzapemsoAAAAC/hi-robot.gif",'frog':"https://tse4.mm.bing.net/th?id=OIP.Bq6pyy9PsKGHa48VFeUtoQHaFj&pid=Api&P=0&h=180","zebra":"https://tse1.mm.bing.net/th?id=OIP.FT8561H6YloSaR0NUZdtJgHaGX&pid=Api&P=0&h=180",
              "lion":"https://tse2.mm.bing.net/th?id=OIP.OrKSoSSkk_RpMT7w7siQOAHaEK&pid=Api&P=0&h=180","tiger":"https://tse3.mm.bing.net/th?id=OIP.WUwR6MAA7sm-mGUr4_gILwHaEo&pid=Api&P=0&h=180"
              },  # Store the dictionary in the 'data' field,
            name=named,
            title=title,
            image=image
           
        ) 
        self.stdout.write(self.style.SUCCESS("completed inserting data"))             

        
       
    
    


        
        
        

       
   
       
       
       