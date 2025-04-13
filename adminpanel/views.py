
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse
from django.urls import  reverse
from django.contrib import messages
from .forms import ImageUploadForm, contactform, quizform2, registerform,resetpasswordform,loginform,forgotpasswordform,profileform
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
from .models import StudentPerformance, UploadedImage, badges, courses, gameresult, quiz,leaderboard, speechquiz2
import json
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.db.models import Count,Avg


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
   
      
   
    
    



       
  
@login_required
def index1(request):
    blogtitle="bjarath"
    posts=quiz.objects.all()
    return render(request,"index1.html",{ 'blogtitle':blogtitle,'posts':posts})
from django.shortcuts import render

from django.shortcuts import render
from .models import quiz
import json
@login_required
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
@login_required
def attempt2(request,postid):
    quiz_instance = quiz2.objects.get(id=postid)
    gameresult2.objects.all().delete() 

 
    data = quiz_instance.data
    print("Data:", data)

    # Convert the dictionary into a list of words and images
    list_data = [{"word": key, "image": value} for key, value in data.items()]

    print("Serialized list_data:", list_data)  # Check the structure here

    # Pass the serialized data as JSON to the template
    serialized_data = json.dumps(list_data)

    return render(request, "attempt2.html", {"list_data": serialized_data})



    

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
@login_required
def about(request):
    print('abougannnnnnn')
    gameresult2.objects.all().delete() 
    return render(request,'about.html')

def dyslexia(request):
     return render (request,"dyslexia.html")
@login_required
def texttospeech(request):
    return render(request,'texttospeech.html')
@login_required
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
@login_required
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


@login_required
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
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
 # Make sure you're importing your form correctly

@login_required
def addprofiles(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if the user is not logged in
    
    print('manishkumar')  # Just for debugging, you can remove it later

    # Initialize the form, this can be either a blank form or a form with existing data
    form = profileform()

    # Handling POST request
    if request.method == "POST":
        print("Form submitted")

        # Ensure you are passing both POST data and FILES (for file uploads)
        form = profileform(request.POST, request.FILES)

        if form.is_valid():
            # Create a profile instance but don't commit to the DB yet
            post = form.save(commit=False)
            post.user = request.user  # Associate the form with the logged-in user

            try:
                post.save()  # Save the profile to the database
                print("Profile saved successfully.")
                return redirect('profiles')  # Redirect to the profile list or profile page
            except Exception as e:
                print(f"Error saving profile: {e}")
                form.add_error(None, "There was an issue saving your profile.")  # Show a generic error message

        else:
            print("Form is invalid!")
            print(form.errors)  # Print the form errors to help debug

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
@login_required
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








@login_required
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

            
            return redirect("index1")

    else:
        form = quizform()


    return render(request, 'addquiz.html', {'form': form})
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from .forms import quizform2
from .models import quiz2

@permission_required('adminpanel.add_quiz2', raise_exception=True)
def addquiz2(request):
    print("User groups: ", request.user.groups.all())
    print(request.user.get_all_permissions())

    if not request.user.groups.filter(name='lowgroupwithoutaddquiz').exists():
        return redirect('index1')  # Redirect somewhere appropriate

    if request.method == 'POST':
        form = quizform2(request.POST, request.FILES)
        if form.is_valid():
            quiz_data = {}
            word_keys = [key for key in request.POST if key.startswith('word_')]

            for word_key in word_keys:
                index = word_key.split('_')[1]
                word = request.POST.get(f'word_{index}')
                image = request.FILES.get(f'image_{index}')
                if word and image:
                    temp = quiz2(image=image)
                    temp.save()
                    quiz_data[word] = temp.image.url
                    temp.delete()

            quiz_obj = form.save(commit=False)
            quiz_obj.data = quiz_data
            quiz_obj.save()
            return redirect("")
    else:
        form = quizform2()

    return render(request, 'addquiz2.html', {'form': form})

def deletequiz(request):
    quiz2.objects.all().delete() 

    return redirect("studentprogress")





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
@login_required
def home(request):
    
    return render(request, 'chatbot.html')
@login_required
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
@login_required
def speechquizes(request):
    posts=speechquiz2.objects.all()
    gameresult2.objects.all().delete()
    return render(request,'speechquizcard.html',{"posts":posts})
from django.shortcuts import render
import json
@login_required
def avinash(request, postid):
    oii = speechquiz2.objects.get(id=postid)  # Fetch the object using the post ID
    soii = oii.data  # Get the 'data' field (presumably a list of words)
    
    list_data = [i for i in soii]  # Convert data into a list (if needed)
    serialized_data = json.dumps(list_data)  # Serialize the list into JSON format
    print(serialized_data)  # For debugging
    
    return render(request, "avinash.html", {"serialized_data": serialized_data})

    






@login_required  
def coursesda(request):
    posts=courses.objects.all()
    return render(request,"coursesda.html",{"posts":posts})
import json

import json
from django.shortcuts import render
from .models import courses
@login_required
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
@login_required
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
@login_required
def mynotes(request, postid):
    # Retrieve the Notes object for the user with the given postid
    posts = notes.objects.filter(user_id=postid)
    l = []
    
    # Iterate over the posts to extract the data (wrong words)
    for post in posts:
        l.extend(post.data)  # Assuming 'data' is a list of words (wrong words)

    # Render the 'mymistakes.html' template, passing 'l' to display the words
    return render(request, 'mymistakes.html', {'l': l})
@login_required
def dyslexiatools(request):
    return render(request,'dyslexiafinal.html')
@login_required
def wordexplorer(request):
    return render(request,'wordexplorer.html')
@login_required
def teacher(request):
    return render(request,'teacher.html')
from django.shortcuts import render, redirect
from .forms import courseform


from django.shortcuts import render, redirect
from .models import courses
import json
@login_required
def addcourse(request):
    if request.method == 'POST':
        # Extract basic course data from the form
        name = request.POST.get('name')
        title = request.POST.get('title')
        image = request.FILES.get('image')  # For the course image

        # Create the Course object with basic details
        course = courses.objects.create(
            name=name,
            title=title,
            image=image
        )

        # Extract word-image pairs (dynamic fields)
        word_image_pairs = []
        word_image_count = len(request.POST) // 2  # Every word/image pair has two inputs

        for i in range(word_image_count):
            word = request.POST.get(f'word_{i}')
            uploaded_image = request.FILES.get(f'image_{i}')
            if word and uploaded_image:  # Ensure both word and image are provided
                # Check if the image has been uploaded and access its URL safely
                image_url = uploaded_image.url if hasattr(uploaded_image, 'url') else None

                word_image_pairs.append({
                    'word': word,
                    'image': image_url  # Store the image URL, not the file object
                })

        # If there are word-image pairs, store them as JSON in the `data` field
        if word_image_pairs:
            course.data = json.dumps(word_image_pairs)  # Store the pairs as JSON
        course.save()

        # Redirect to the course list or another page after saving
        return redirect('courses')  # Modify the redirect destination as needed

    return render(request, 'addcourses.html') 
 # Render the course addition form page
@login_required
def dineshstorys(request):
    return render(request,'dineshstory.html')
from django.shortcuts import render
from .simplifier import simplify_text  # Import text simplification function

from django.shortcuts import render
from .simplifier import simplify_text  
@login_required
def simplify_view(request):
    simplified_text = None

    if request.method == "POST":
        text = request.POST.get("text", "")
        if text:
            simplified_text = simplify_text(text)
            print("Original:", text)  # Debugging
            print("Simplified:", simplified_text)  # Debugging

    return render(request, "textsimplifier.html", {"simplified_text": simplified_text})
@login_required
def images(request):
   return render(request,'image.html')
from django.shortcuts import render, redirect
from .forms import courseform  # Assuming you have a CourseForm for the 'courses' model
from .models import courses
from django.contrib.auth.decorators import permission_required

@login_required
def addcourse(request):
    print("User groups: ", request.user.groups.all())
    print(request.user.get_all_permissions())

    # Check if user is in the 'lowgroupwithoutaddquiz' group (if needed)
    if not request.user.groups.filter(name='lowgroupwithoutaddquiz').exists():
        return redirect('')  # Redirect if not authorized

    # Form handling
    if request.method == 'POST':
        form = courseform(request.POST, request.FILES)
        if form.is_valid():
            # Process word-image pairs (if applicable)
            course_data = {}
            word_image_pairs = [key for key in request.POST if key.startswith('word_')]

            for word_key in word_image_pairs:
                word_index = word_key.split('_')[1]
                word = request.POST.get(f'word_{word_index}')
                image = request.FILES.get(f'image_{word_index}')
                
                if word and image:
                    # Save the image temporarily to generate a URL
                    temp_course = courses(image=image)
                    temp_course.save()  # Save the image to the database to generate a URL
                    
                    # Now get the image URL after saving the image
                    course_data[word] = temp_course.image.url  # Save the image URL associated with the word
                    
                    # Delete the temporary course object after saving its image URL
                    temp_course.delete()

            # Save the other fields and the word-image pairs as JSON
            course_object = form.save(commit=False)
            course_object.data = course_data  # Save the word-image pairs as JSON
            course_object.save()  # This will auto-fill the 'createdate' field

            # Redirect after saving
            return redirect('courses')  # Replace with your course listing URL

    else:
        form = courseform()

    return render(request, 'addcourses.html', {'form': form})
from django.db.models import Count, Avg, Q, F


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Q, F
from .models import StudentPerformance

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from .models import User, profile, leaderboard  # adapt this if model names differ
import operator

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import User, profile, leaderboard

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group

@login_required
def student_progress(request):
    # Check if the user is in the allowed group
    if not request.user.groups.filter(name='lowgroupwithoutaddquiz').exists():
        return redirect('')  # Replace 'home' with your home URL name

    users = User.objects.all()
    profiles = profile.objects.all()
    leaderboard_entries = leaderboard.objects.all()

    leaderboard_data = []

    for user in users:
        user_profile = profiles.filter(user=user).first()
        user_name = user_profile.Name if user_profile else user.username
        user_image = user_profile.image.url if user_profile and user_profile.image else None

        entry = leaderboard_entries.filter(user=user).first()
        if not entry:
            continue  # Skip users with no attempts

        attempted_data = [result for result in entry.data if result.get('is_attempted', True)]
        total_correct = sum(result['is_correct'] for result in attempted_data)
        total_attempted = len(attempted_data)
        total_incorrect = total_attempted - total_correct

        efficiency = (total_correct / total_attempted * 100) if total_attempted > 0 else 0

        if efficiency >= 90:
            label = "Excellent"
        elif efficiency >= 75:
            label = "Very Good"
        elif efficiency >= 50:
            label = "Average"
        else:
            label = "Needs Improvement"

        leaderboard_data.append({
            'user': user_name,
            'image': user_image,
            'correct': total_correct,
            'incorrect': total_incorrect,
            'efficiency': round(efficiency, 2),
            'label': label
        })

    leaderboard_data.sort(key=lambda x: x['correct'], reverse=True)

    current_user_name = profile.objects.get(user=request.user).Name
    current_user_data = next((d for d in leaderboard_data if d['user'] == current_user_name), None)
    current_user_rank = leaderboard_data.index(current_user_data) + 1 if current_user_data else None

    chart_labels = [d['user'] for d in leaderboard_data]
    correct_data = [d['correct'] for d in leaderboard_data]
    incorrect_data = [d['incorrect'] for d in leaderboard_data]

    return render(request, 'studentprogress.html', {
        'leaderboard_data': leaderboard_data,
        'current_user_data': current_user_data,
        'current_user_rank': current_user_rank,
        'chart_labels': chart_labels,
        'correct_data': correct_data,
        'incorrect_data': incorrect_data,
    })


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import profile, leaderboard

@login_required
def user_progress(request):
    user = request.user
    user_profile = profile.objects.filter(user=user).first()
    leaderboard_entry = leaderboard.objects.filter(user=user).first()

    if leaderboard_entry:
        attempted_data = [res for res in leaderboard_entry.data if res.get('is_attempted', True)]
        correct = sum(res['is_correct'] for res in attempted_data)
        attempted = len(attempted_data)
        incorrect = attempted - correct
        efficiency = (correct / attempted * 100) if attempted > 0 else 0
    else:
        correct = attempted = incorrect = efficiency = 0

    return render(request, 'userprogress.html', {
        'user_name': user_profile.Name if user_profile else user.username,
        'user_image': user_profile.image.url if user_profile and user_profile.image else None,
        'correct': correct,
        'incorrect': incorrect,
        'efficiency': round(efficiency, 2),
    })
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import leaderboard, quiz

from django.shortcuts import render
from .models import leaderboard, quiz2

def index2(request):
    user = request.user
    blogtitle = "Welcome to the Quiz App"
  
    try:
        lb = leaderboard.objects.filter(user=user).latest('id')
    except leaderboard.DoesNotExist:
        lb = None

    efficiency = 0
    if lb and lb.data:
        total_attempts = len(lb.data)
        correct = sum(1 for item in lb.data if item.get("is_correct") == 1)

        if total_attempts > 0:
            efficiency = int((correct / total_attempts) * 100)

   
    if efficiency < 50:
        quizzes = quiz2.objects.filter(name="easy")
    else:
        quizzes = quiz2.objects.filter(name="hard")

    return render(request, "markquiz.html", {
        'blogtitle': blogtitle,


        'posts': quizzes,
        'efficiency': efficiency
    })
from django.utils.timezone import now, timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import UserActivity, Notification

@csrf_exempt
def notify_inactive_users(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message', '📢 You have a new notification!')

        inactive_time = now() - timedelta(seconds=10)
        inactive_users = UserActivity.objects.filter(last_active__lt=inactive_time)

        notifications = []
        for activity in inactive_users:
            notifications.append(Notification(user=activity.user, message=message))

        Notification.objects.bulk_create(notifications)

        return JsonResponse({'status': 'ok', 'notified_users': len(notifications)})

    return JsonResponse({'error': 'Invalid request'}, status=400)

