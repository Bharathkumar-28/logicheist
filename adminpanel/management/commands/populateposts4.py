from typing import Any

from django.core.management.base import BaseCommand





class Command(BaseCommand):
    
    help="THis commands inserts categorydata  data" 
    def handle(self, *args: Any, **options: Any):
        from  adminpanel.models import quiz
        #deleting existing data
        quiz.objects.all().delete()


        
        titles=[
"power OF ME ","powerof you"
]
        content=[
  
         "power OF ME ",
           "power OF ME "
]
        week=["1","2"]
        img=[
    "https://picsum.photos/id/1/200/300",
     "https://picsum.photos/id/1/200/300",
]
       
  
        for title,content,imgurl,week in zip(titles,content,img,week):
            quiz.objects.create(
            name="Reptiles and Amphibians",  # Example name for the category
            data={"snake":"https://tse3.mm.bing.net/th?id=OIP.RL0ZKNoaDbaPGzZkuAdHAwHaHa&pid=Api&P=0&h=180",'frog':"https://tse4.mm.bing.net/th?id=OIP.Bq6pyy9PsKGHa48VFeUtoQHaFj&pid=Api&P=0&h=180","zebra":"https://tse1.mm.bing.net/th?id=OIP.FT8561H6YloSaR0NUZdtJgHaGX&pid=Api&P=0&h=180",
              "lion":"https://tse2.mm.bing.net/th?id=OIP.OrKSoSSkk_RpMT7w7siQOAHaEK&pid=Api&P=0&h=180","tiger":"https://tse3.mm.bing.net/th?id=OIP.WUwR6MAA7sm-mGUr4_gILwHaEo&pid=Api&P=0&h=180"
              },  # Store the dictionary in the 'data' field,
            title=title,
            content=content,
            image=imgurl,
            week=week
        ) 
        self.stdout.write(self.style.SUCCESS("completed inserting data"))             

        
       
    
    


        
        
        

       
   
       
       
       