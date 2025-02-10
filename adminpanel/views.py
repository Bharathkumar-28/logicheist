from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import  reverse
from django.contrib import messages
from .forms import contactform, registerform,resetpasswordform,loginform,forgotpasswordform,profileform
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import  send_mail
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from adminpanel.models import post,profile, words
import pdb
import logging
from django.http import JsonResponse
from .models import gameresult, quiz
import json
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
def main(request):
    gameresult2.objects.all().delete() 
    logger=logging.getLogger("testing")
    blogtitle="bharath"
   
    logger.debug("Blog title: %s", blogtitle)
    print(blogtitle)
   
    
    


    
    return render(request,"main.html",{ 'blogtitle':blogtitle})
def index1(request):
    blogtitle="bjarath"
    posts=quiz.objects.all()
    return render(request,"index1.html",{ 'blogtitle':blogtitle,'posts':posts})
from django.shortcuts import render

from django.shortcuts import render
from .models import quiz
import json

def attempt(request,postid):
    quiz_instance = quiz.objects.get(id=postid)

    # Get the data (assuming it's a dictionary)
    data = quiz_instance.data
    print("Data:", data)

    # Convert the dictionary into a list of words and images
    list_data = [{"word": key, "image": value} for key, value in data.items()]

    print("Serialized list_data:", list_data)  # Check the structure here

    # Pass the serialized data as JSON to the template
    serialized_data = json.dumps(list_data)

    return render(request, "attempt.html", {"list_data": serialized_data})




    

# Create your views here.
def register(request):
    form=registerform()
    blogtitle="bjarath" 
    if request.method =='POST':
        form=registerform(request.POST)
        if form.is_valid():

            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            """  print('registersucess') """
            messages.success(request,"registration succesfull")
            return redirect("login")
         
    
               
    return render (request,"register.html",{'form':form,'blogtitle':blogtitle})

def about(request):
    gameresult2.objects.all().delete() 
    return render(request,'about.html')

def dyslexia(request):
     return render (request,"dyslexia.html")
@login_required
def texttospeech(request):
    return render(request,'texttospeech.html')
def example(request):
    return render(request,'example.html')
def login(request):
    form=loginform()
    if request.method =="POST":
        form=loginform(request.POST)
        if form.is_valid():
           
           print("login success")
           username=form.cleaned_data['username']
           password=form.cleaned_data['password']
           user=authenticate(username=username,password=password)
           if user is not None:
            auth_login(request,user)
            messages.success(request,'you are successfully logged in')
            return redirect("index")
            
                
            
    return render (request,"login.html",{'form':form})
def logout(request):
    gameresult2.objects.all().delete() 
    print("Logging out user")
    auth_logout(request)
    return redirect('login')
def forgotpassword(request):
    form=forgotpasswordform()
    if request.method=='POST':
        form=forgotpasswordform(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            user=User.objects.get(email=email)
            #send resnt email
            token=default_token_generator.make_token(user)
            uid=urlsafe_base64_encode(force_bytes(user.pk))
            currentsite=get_current_site(request)
            domain=currentsite.domain
            subject="reset password requsted"
            message=render_to_string('resetpassword.html',{
                'domain':domain,
                'uid':uid,
                'token':token
            })
            send_mail(subject,message,'noreply@hellojiohellojio.com',[email])
            messages.success(request,"your email is sent")





        
    return render(request,'forgotpassword.html',{'form':form})
def resetpassword(request,uidb64,token):
    form=resetpasswordform()
    if request.method=='POST':
        form=resetpasswordform(request.POST)
        if form.is_valid():
            newpassword=form.cleaned_data['newpassword']
            try:
                uid=urlsafe_base64_decode(uidb64)
                user=User.objects.get(pk=uid)
            except(TypeError,ValueError,OverflowError,User.DoesNotExist):
                user=None
            if user  is not None and default_token_generator.check_token(user,token):
                user.set_password(newpassword)  
                user.save()
                messages.success(request,'password changed correctly')    
                return redirect('login') 
            else:
                messages.error(request,'the password link is invalid')




    return render(request,'resetpassword2.html',{'form':form})
@login_required
def game(request):
    return render (request,"game.html")
@login_required
def spell(request):
    return render(request,"spell.html")

def index(request):
    return render(request,"index.html")
@login_required
def profiles(request):
    posts=profile.objects.first()
    return render(request,"profile.html",{'posts':posts})
@login_required
def game(request):
    # Fetch all the word posts
    posts = words.objects.all().values('name', 'image')  # Get 'name' and 'image' fields
    # Serialize the data to JSON format
    posts_json = json.dumps(list(posts))
    
    # Pass the serialized data to the template
    return render(request, "game.html", {'posts': posts_json, 'blogtitle': 'bjarath'})
@login_required
def createprofile(request):
    form=profileform()
    if request.method=="POST":
        form=profileform(request.POST,request.FILES)
        if form .is_valid():
            post=form.save(commit=False)
            post.user=request.user
            post.save()
            return redirect('profile')
    return render(request,"createprofile.html",{'form':form})

""" def newpost(request):
    
    form=profileform()
    if request.method=="POST":
        form=profileform(request.POST,request.FILES)
        if form .is_valid():
            post=form.save(commit=False)
            post.user=request.user
            post.save()
            return redirect('adminpanel:dashboard')
    return render(request,'newpost.html',{'form':form}) """
@login_required
def contact(request):
     gameresult2.objects.all().delete() 
     form=contactform()
     if request.method=='POST':
        form=contactform( request.POST)
        name=request.POST.get('name')
        email=request.POST.get('email')
        message=request.POST.get('message')
        send_mail(name,message,'noreply@hellojiohellojio.com',[email])
        messages.success(request,"your email is sent")
     return render(request,'contact.html',{'form':form})  
@login_required
def result(request):
    # Retrieve all game results
    oii = gameresult.objects.all()
    
    scores = []
    words = []
    
    # Collect words and their corresponding scores (1 for correct, 0 for incorrect)
    for result in oii:
        words.append(result.word)  # Add the word to the words list
        scores.append(1 if result.iscorrect else 0)  # Add 1 for correct answer, 0 for incorrect answer
    
        # Limit to the first 5 results
      
    
    # Prepare for template rendering
    words = words  # List of words
    scores = scores  # List of scores (1 or 0)
    
    return render(request, 'result.html', {'words': words, 'scores': scores})


from django.shortcuts import render
from .models import gameresult2  # Ensure you're importing your model

def finalresult(request):
    # Retrieve all game results, limit to the first 5 results
    oii = gameresult2.objects.all() # Limit to the first 5 results

    words = []
    scores = []
    
    # Collect words and their corresponding scores (1 for correct, 0 for incorrect)
    for result in oii:
        # Assuming result.iscorrect is a JSONField with a list of dictionaries
        for entry in result.iscorrect:
            words.append(entry['word'])  # Add the word to the words list
            scores.append(entry['is_correct'])  # Add 1 or 0 based on correctness
    
    # Prepare for template rendering
    return render(request, 'finalresult.html', {'words': words, 'scores': scores})



  # Ensure this is the correct model

  # Assuming the model is named GameResult





""" def graph(request):
    # Example data: words and corresponding scores (1 for correct, 0 for incorrect)
    words = ['Word1', 'Word2', 'Word3', 'Word4', 'Word5']
    scores = [1, 0, 0, 1, 1]  # 1 = correct, 0 = incorrect
    
    # Pass the data to the template
    return render(request, 'graph.html', {'words': words, 'scores': scores}) """




import logging

logger = logging.getLogger(__name__)
@login_required
def graph(request):
    if request.method == 'POST':
        word = request.POST.get('word')
        correctanswer = request.POST.get('correct_answer')
        useranswer = request.POST.get('user_answer')

        if not useranswer or not correctanswer:
            return JsonResponse({'status': 'error', 'message': 'Missing answer(s).'}, status=400)

        is_correct = useranswer.lower() == correctanswer.lower()

        game_result = gameresult(
            word=word,
            correctanswer=correctanswer,
            useranswer=useranswer,
            iscorrect=is_correct
        )
        
        try:
            game_result.save()
            logger.info(f"Game result saved: {game_result}")
        except Exception as e:
            logger.error(f"Error saving game result: {e}")
            return JsonResponse({'status': 'error', 'message': 'Error saving result.'}, status=500)

       

        return JsonResponse({'status': 'success', 'message': 'Game result saved successfully.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
from django.shortcuts import render
from django.http import JsonResponse
from .models import gameresult2



<<<<<<< HEAD





def graph2(request):
    if request.method == "POST":
        word = request.POST.get("word")
        correct_answer = request.POST.get("correct_answer")
        user_answer = request.POST.get("user_answer")
        is_correct = request.POST.get("is_correct") == "true"  # Convert string to boolean

        # Prepare the result as a dictionary with word and correctness
        result_dict = {
            'word': word,
            'is_correct': 1 if is_correct else 0
        }

        try:
            # Check if any previous game result exists
            game_result = gameresult2.objects.last()

            if game_result:
                # If previous result exists, append to the existing list of dictionaries
                existing_results = game_result.iscorrect
                existing_results.append(result_dict)  # Append the new dictionary to the list
            else:
                # If no previous results exist, create a new list with the current result
                existing_results = [result_dict]

            # Save or update the game result in the database
            # If no previous result was found, we create a new instance; if one exists, we update it
            if game_result:
                game_result.iscorrect = existing_results
                game_result.save()
            else:
                # Create a new game result object and save it
                game_result = gameresult2(iscorrect=existing_results)
                game_result.save()

            # Return success response
            return JsonResponse({'status': 'success', 'message': 'Game result saved successfully.'})

        except Exception as e:
            # Handle any errors while saving
            return JsonResponse({'status': 'failure', 'message': f'Error saving result: {str(e)}'})

    # Return failure response for invalid request method
    return JsonResponse({'status': 'failure', 'message': 'Invalid request method.'})


def backtohome(request):
    # Delete all game result entries
    gameresult2.objects.all().delete()  # Delete all records from gameresult2 table
    
    # Redirect to a URL named 'index1'
    return redirect(reverse('index1'))




@login_required
def speechtotext(request):
        return render(request,'speechtotext.html')
@login_required
def game2(request):
    return render(request,'game2.html')
def texttospeechtamil(request):
    return render (request,'texttospeechtamil.html')
from django.shortcuts import render, redirect
from .forms import quizform
from .models import quiz
import json

from django.shortcuts import render, redirect
from .forms import quizform
from .models import quiz

def addquiz(request):
    if request.method == 'POST':
        form = quizform(request.POST, request.FILES)
        if form.is_valid():
            # Process word-image pairs
            quiz_data = {}
            word_image_pairs = [key for key in request.POST if key.startswith('word_')]
            
            for word_key in word_image_pairs:
                word_index = word_key.split('_')[1]
                word = request.POST.get(f'word_{word_index}')
                image = request.FILES.get(f'image_{word_index}')
                
                if word and image:
                    # Save the image temporarily to generate a URL
                    temp_quiz = quiz(image=image)
                    temp_quiz.save()  # Save the image to the database to generate a URL
                    
                    # Now get the image URL after saving the image
                    quiz_data[word] = temp_quiz.image.url  # Save the image URL associated with the word
                    
                    # Delete the temporary quiz object after saving its image URL
                    temp_quiz.delete()

            # Save the other fields and the word-image pairs as JSON
            quiz_object = form.save(commit=False)
            quiz_object.data = quiz_data  # Save the word-image pairs as JSON
            quiz_object.save()  # This will auto-fill the 'createdate' field

            # Redirect after saving
            return render(request,"index1.html")  # Redirect to the quiz list page

    else:
        form = quizform()

    return render(request, 'addquiz.html', {'form': form})
=======
def logindemo(request):
    # Your view logic here (e.g., handling form submission, authentication, etc.)

    # Ensure that you return an HttpResponse object
    return render(request, 'logindemo.html')
>>>>>>> ab2fe0eaf5b618df6a8e77aa68fff2fb9ac4b417
