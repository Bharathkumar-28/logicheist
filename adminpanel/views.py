
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, render,redirect
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
from .models import badges, courses, gameresult, quiz,leaderboard, speechquiz2
import json
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
@login_required
def main(request):
    gameresult2.objects.all().delete() 
    logger=logging.getLogger("testing")
    blogtitle="bharath"
    secondposts=badges.objects.all()
    scores=leaderboard.objects.filter(user=request.user)
  
    # Check if the user has a leaderboard entry
    leaderboard_entry = leaderboard.objects.filter(user=request.user).first()

    if leaderboard_entry:
        total_score = sum(result['is_correct'] for result in leaderboard_entry.data)  # Calculate total score
    else:
        total_score = 0  # Default score if no leaderboard entry
    print('totsal', total_score)
    if  total_score == 0:
         return render(request,"main.html",{ 'blogtitle':blogtitle,})
      
    else:
        for soii in secondposts:
            if total_score>=soii.score:
                a=soii.name
                print("a",a)
                b=soii.image
                print("b",b)
                break
        return render(request,"main.html",{ 'blogtitle':blogtitle,'a':a,'b':b,'total_score':total_score})
   
      
   
    
    



       
  

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
    gameresult2.objects.all().delete() 

 
    data = quiz_instance.data
    print("Data:", data)

    # Convert the dictionary into a list of words and images
    list_data = [{"word": key, "image": value} for key, value in data.items()]

    print("Serialized list_data:", list_data)  # Check the structure here

    # Pass the serialized data as JSON to the template
    serialized_data = json.dumps(list_data)

    return render(request, "attempt.html", {"list_data": serialized_data})




    

def register(request):
    if request.user.is_authenticated:
        return redirect('')
    else:
        form=registerform()
        blogtitle="bjarath" 
        if request.method =='POST':
            form=registerform(request.POST)
            if form.is_valid():
                user=form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()
                """  print('registersucess') """
                lowgroupwithoutaddquiz,created=Group.objects.get_or_create(name='lowgroupwithoutaddquiz')
                user.groups.add(lowgroupwithoutaddquiz)
                messages.success(request,"registration succesfull")
                return redirect("login")
         
    
               
    return render (request,"register.html",{'form':form,'blogtitle':blogtitle})

def about(request):
    print('abougannnnnnn')
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
    if request.user.is_authenticated:
        return redirect('')

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
            return redirect('')
            
                
            
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


from spellchecker import SpellChecker
from django.http import JsonResponse

def spell(request):
    if request.method == 'POST':
        word = request.POST.get('word', '').strip()
        
       
        spell = SpellChecker()

        misspelled = spell.unknown([word])
        suggestions = []

        for word in misspelled:
            suggestions = spell.candidates(word)  

  
        return JsonResponse({'suggestions': list(suggestions)})
    return render(request,"spell.html")



def index(request):
    return render(request,"index.html")
@login_required
def profiles(request):
    posts = profile.objects.filter(user=request.user)
    secondposts=badges.objects.all()
    scores=leaderboard.objects.filter(user=request.user)
  
    # Check if the user has a leaderboard entry
    leaderboard_entry = leaderboard.objects.filter(user=request.user).first()

    if leaderboard_entry:
        total_score = sum(result['is_correct'] for result in leaderboard_entry.data)  # Calculate total score
    else:
        total_score = 0  # Default score if no leaderboard entry
    print('totsal', total_score)     
    

    a=0
    b=0
    if posts:
        for soii in secondposts:
            if total_score>=soii.score:
                a=soii.name
                print("a",a)
                b=soii.image
                print("b",b)
                break
    
        # Get the posts related to the authenticated user
        posts = profile.objects.filter(user=request.user)

        # Print each post's information in the QuerySet
        print('oiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
        for post in posts:
            print(f"Post ID: {post.id}, User: {post.user}, Title: {post.Name},id:{post.id}")  # Example: print the id, user, and title of each post
  
        if a!=0 and b!=0:
            return render(request, "profile.html", {'posts': posts,'a':a,'b':b})
        else:
            return render(request, "profile.html",{"posts":posts})

   

    else:
        if not posts:
            return redirect('addprofiles')
       
      
    

    


     
     
from django.shortcuts import render, redirect

from django.contrib.auth.models import User

def addprofiles(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if the user is not logged in

    print('manishkumar')
    form = profileform()

    if request.method == "POST":
        print("Form submitted")
        form = profileform(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # Associate the form with the logged-in user
            post.save()
            return redirect('profiles')  # Redirect to the profile list or profile page

    return render(request, 'addprofile.html', {'form': form})




    
@login_required
def game(request):
 
    posts = words.objects.all().values('name', 'image')  # Get 'name' and 'image' fields
    # Serialize the data to JSON format
    posts_json = json.dumps(list(posts))
    
    # Pass the serialized data to the template
    return render(request, "game.html", {'posts': posts_json, 'blogtitle': 'bjarath'})
@login_required
def createprofile(request,postid):
    profileinstance= get_object_or_404(profile, id=postid)
    form=profileform()
    if request.method=="POST":
        form=profileform(request.POST,request.FILES,instance=profileinstance)
        if form .is_valid():
            post=form.save(commit=False)
            post.user=request.user
            post.save()
            return redirect('profiles')
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



   




@login_required
def speechtotext(request):
        return render(request,'speechtotext.html')
@login_required
def game2(request):
    gameresult2.objects.all().delete() 
    return render(request,'game2.html')
def texttospeechtamil(request):
    return render (request,'texttospeechtamil.html')
from django.shortcuts import render, redirect
from .forms import quizform
from .models import quiz
import json
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from .forms import quizform
from .models import quiz
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from .forms import quizform
from .models import quiz
from django.contrib import messages

# Permission check and group check combined into the view logic
@permission_required('adminpanel.add_quiz', raise_exception=True)
def addquiz(request):
    print("User groups: ", request.user.groups.all())
    print( request.user.get_all_permissions())

    # Check if user is in the 'lowgroupwithoutaddquiz' group
    if not request.user.groups.filter(name='lowgroupwithoutaddquiz').exists():
 
        return redirect('')

    # Form handling
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
            return render(request, "index1.html")  # Redirect to the quiz list page

    else:
        form = quizform()

    return render(request, 'addquiz.html', {'form': form})
from django.shortcuts import render, redirect
from .forms import speechquizform
from .models import speechquiz2
from django.contrib import messages
from django.core.exceptions import PermissionDenied

@permission_required('adminpanel.add_speechquiz', raise_exception=True)

def addspeechquiz(request):
   # Check if user is in the 'lowgroupwithoutaddquiz' group
    if not request.user.groups.filter(name='lowgroupwithoutaddquiz').exists():
 
        return redirect('')
    
    if request.method == 'POST':
        form =speechquizform(request.POST, request.FILES)  # Handle image upload with request.FILES
        if form.is_valid():
            # Save the main quiz object (title, name, image)
            quiz_object = form.save(commit=False)

            # Process the words
            word_list = []
            word_index = 1
            while f'word_{word_index}' in request.POST:
                word = request.POST.get(f'word_{word_index}')
                if word:
                    word_list.append(word)
                word_index += 1

            # Store the words in the model's data field
            quiz_object.data = word_list  # Assuming 'data' is a JSONField to store words as a list
            quiz_object.save()

            messages.success(request, "Quiz added successfully.")
            return redirect('speechquizcard')  # Redirect to a page that shows the list of quizzes
        else:
            messages.error(request, "There was an error with your submission.")
    else:
        form = speechquizform()

    return render(request, 'addspeechquiz.html', {'form': form})




from django.shortcuts import render
from django.http import JsonResponse
import google.generativeai as genai

# Configure Gemini
api_key = "AIzaSyBNBgchXs6MmOx-lBQSnovzCoyOuC18MY0"  # Replace with your actual API key
genai.configure(api_key=api_key)

# Set the generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the Generative Model
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction="Your dyslexia support instructions here...",
)

# Initial chat history
history = [
    {"role": "user", "parts": ["hi"]},
    {"role": "model", "parts": ["Hello! How can I assist you today? today you will some words and spell the words"]},
]

def home(request):
    """Renders the homepage with the chatbot interface."""
    return render(request, 'chatbot.html')

def chat(request):
    """Handles chat messages sent from the frontend."""
    if request.method == 'POST':
        user_message = request.POST.get('message', '').strip()
        
        if not user_message:
            return JsonResponse({"reply": "Please enter a valid message."}, status=400)
        
        # Create a new chat session with the provided message
        chat_session = model.start_chat(history=history)
        response = chat_session.send_message(user_message)
        
        # Capture the response text
        model_response = response.text
        
        # Append the user and model messages to the history
        history.append({"role": "user", "parts": [user_message]})
        history.append({"role": "model", "parts": [model_response]})
        
        # Return the model's response as JSON
        return JsonResponse({"reply": model_response})

    return JsonResponse({"reply": "Invalid request."}, status=400)
def speechquizes(request):
    posts=speechquiz2.objects.all()
    gameresult2.objects.all().delete()
    return render(request,'speechquizcard.html',{"posts":posts})
from django.shortcuts import render
import json

def avinash(request, postid):
    oii = speechquiz2.objects.get(id=postid)  # Fetch the object using the post ID
    soii = oii.data  # Get the 'data' field (presumably a list of words)
    
    list_data = [i for i in soii]  # Convert data into a list (if needed)
    serialized_data = json.dumps(list_data)  # Serialize the list into JSON format
    print(serialized_data)  # For debugging
    
    return render(request, "avinash.html", {"serialized_data": serialized_data})

    






   
def coursesda(request):
    posts=courses.objects.all()
    return render(request,"coursesda.html",{"posts":posts})
def attemptcourses(request,postid):
    quiz_instance = courses.objects.get(id=postid)
   

    # Get the data (assuming it's a dictionary)
    data = quiz_instance.data
    print("Data:", data)

    # Convert the dictionary into a list of words and images
    list_data = [{"word": key, "image": value} for key, value in data.items()]

    print("Serialized list_data:", list_data)  # Check the structure here

    # Pass the serialized data as JSON to the template
    serialized_data = json.dumps(list_data)

    return render(request, "attemptcourses.html", {"list_data": serialized_data})
from django.http import JsonResponse


from django.contrib.auth.models import User


import logging
from django.http import JsonResponse
from .models import leaderboard
from django.contrib.auth.models import User

# Set up logging
logger = logging.getLogger(__name__)

def leaderboarda(request):
    if request.method == "POST":
        word = request.POST.get("word")
        correct_answer = request.POST.get("correct_answer")
        user_answer = request.POST.get("user_answer")
        is_correct = request.POST.get("is_correct") == "true"  # Convert string to boolean

        logger.debug(f"Received word: {word}, correct_answer: {correct_answer}, user_answer: {user_answer}, is_correct: {is_correct}")

        result_dict = {
            'word': word,
            'is_correct': 1 if is_correct else 0
        }

        try:
            # Ensure user is authenticated
            user = request.user
            if not user.is_authenticated:
                logger.error("User is not authenticated")
                return JsonResponse({'status': 'failure', 'message': 'User is not authenticated.'})

            # Check if previous result exists for the user
            game_result = leaderboard.objects.filter(user=user).last()

            if game_result:
                existing_results = game_result.data if game_result.data else []
                existing_results.append(result_dict)
                logger.debug(f"Existing results: {existing_results}")
            else:
                existing_results = [result_dict]
                logger.debug(f"No previous results, creating new one: {existing_results}")

            if game_result:
                game_result.data = existing_results
                game_result.save()
                logger.debug(f"Updated result: {game_result.data}")
            else:
                game_result = leaderboard(user=user, data=existing_results)
                game_result.save()
                logger.debug(f"Created new result: {game_result.data}")

            return JsonResponse({'status': 'success', 'message': 'Game result saved successfully.'})

        except Exception as e:
            logger.error(f"Error saving result: {str(e)}")
            return JsonResponse({'status': 'failure', 'message': f'Error saving result: {str(e)}'})

    return JsonResponse({'status': 'failure', 'message': 'Invalid request method.'})

from django.shortcuts import render


from django.shortcuts import render
from .models import leaderboard  # Adjust the import if needed

from django.shortcuts import render
from .models import leaderboard, profile

from django.shortcuts import render
from .models import leaderboard, profile, badges  # Assuming badges is the model for the badges
from django.contrib.auth.models import User
@login_required
def leaderboardview(request):
    # Retrieve all users and profiles
    users = User.objects.all()
    posts = profile.objects.all()

    leaderboard_data = []

    for user in users:
        # Get the user's profile (if available)
        user_profile = posts.filter(user=user).first()  # Get the profile for the current user
        
        # Ensure user_profile exists and has a Name field
        user_name = user_profile.Name if user_profile else None  # Access the Name from profile
        user_image = user_profile.image.url if user_profile and user_profile.image else None  # Get the image URL

        # Check if the user has a leaderboard entry
        leaderboard_entry = leaderboard.objects.filter(user=user).first()

        if leaderboard_entry:
            total_score = sum(result['is_correct'] for result in leaderboard_entry.data)  # Calculate total score
        else:
            total_score = 0  # Default score if no leaderboard entry

        # Find the badge based on the total score
        user_badge_name = None
        user_badge_image = None
        
        # Loop through all badges and assign the one that matches the score
        for badge in badges.objects.all():
            if total_score >= badge.score:  # Assign the badge if the score is greater than or equal to the badge score
                user_badge_name = badge.name
                user_badge_image = badge.image 
                break
              # No need to continue if a badge doesn't match the score

        # Add the user data to the leaderboard_data list
        leaderboard_data.append({
            'user': user_name,  # Use `user_profile.Name` for the user name
            'score': total_score,
            'image': user_image,  # User's profile image
            'badge_name': user_badge_name,  # Badge name based on score
            'badge_image': user_badge_image,  # Badge image
        })

    # Check current user's profile and leaderboard entry for assigning badge
    posts = profile.objects.filter(user=request.user)
    secondposts = badges.objects.all()
    scores = leaderboard.objects.filter(user=request.user)
  
    leaderboard_entry = leaderboard.objects.filter(user=request.user).first()

    if leaderboard_entry:
        total_score = sum(result['is_correct'] for result in leaderboard_entry.data)  # Calculate total score
    else:
        total_score = 0  # Default score if no leaderboard entry
    print('Total score for current user:', total_score)

    # Assign a badge for the current user
    a = None
    b = None
    for badge in secondposts:
        if total_score >= badge.score:
            a = badge.name
            b = badge.image   # Ensure URL for image
            break  # Assign the first matching badge

    # Sort the leaderboard data by score in descending order
    leaderboard_data.sort(key=lambda x: x['score'], reverse=True)

    # Pass the leaderboard data, badge info for the current user, and render the template
    return render(request, 'leaderboard.html', {
        'leaderboard_data': leaderboard_data,
        'a': a,
        'b': b
    })

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import notes
import json





@login_required
@csrf_exempt
def takenotes(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse the incoming JSON data
            user = request.user  # Directly use the User object
            wrong_word = data.get('wrong_word')  # Get the wrong word from the request data

            # Ensure a word was provided
            if wrong_word:
                # Get or create the user's notes object
                nnotes, created = notes.objects.get_or_create(user=user)

                # If the 'data' field is None (shouldn't happen if using JSONField with a default), initialize it
                if nnotes.data is None:
                    nnotes.data = []

                # Only add the word if it's not already in the list
                if wrong_word not in nnotes.data:
                    nnotes.data.append(wrong_word)
                    nnotes.save()

                return JsonResponse({'status': 'success', 'message': 'Wrong word saved successfully.'})

            else:
                return JsonResponse({'status': 'error', 'message': 'No word provided.'}, status=400)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'}, status=400)
from django.shortcuts import render
from .models import notes

def mynotes(request, postid):
    # Retrieve the Notes object for the user with the given postid
    posts = notes.objects.filter(user_id=postid)
    l = []
    
    # Iterate over the posts to extract the data (wrong words)
    for post in posts:
        l.extend(post.data)  # Assuming 'data' is a list of words (wrong words)

    # Render the 'mymistakes.html' template, passing 'l' to display the words
    return render(request, 'mymistakes.html', {'l': l})

def dyslexiatools(request):
    return render(request,'dyslexiafinal.html')
def wordexplorer(request):
    return render(request,'wordexplorer.html')
def teacher(request):
    return render(request,'teacher.html')

   
