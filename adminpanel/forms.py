from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


from adminpanel.models import  post, profile
class contactform(forms.Form):
    name=forms.CharField(label='name',max_length=100,required=True)
    email=forms.EmailField(label='email',required=True)
    message=forms.CharField(label='message',required=True)


class registerform(forms.ModelForm):
    username=forms.CharField(label='username',max_length=100,required=True)
    email=forms.CharField(label='email',max_length=100,required=True)
    password=forms.CharField(label='password',max_length=100,required=True)
    password_confirm=forms.CharField(label='password_confirm',max_length=100,required=True)

    class Meta:
        model=User
        fields=['username','email','password']
    def clean(self):
        cleaneddata=super().clean()  
        password=cleaneddata.get('password')
        password_confirm=cleaneddata.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('password do not match')
class loginform(forms.Form):
    username=forms.CharField(label="username",max_length=100,required=True)
    password=forms.CharField(label="password",max_length=100,required=True)
    def clean(self):
        cleaneddata=super().clean()
        username=cleaneddata.get("username")
        password=cleaneddata.get("password")
        if username and password:
            user=authenticate(username=username,password=password)
            if user is None:
                raise forms.ValidationError("invalid username and password") 
class forgotpasswordform(forms.Form):
    email=forms.EmailField(label='email',max_length=50, required=True,)
    def clean(self):
        cleaneddata=super().clean()
        email=cleaneddata.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("no user found with this email ") 
class resetpasswordform(forms.Form):
      newpassword=forms.CharField(label='newpassowrd',min_length=3)
      confirmpassword=forms.CharField(label='confirmpassowrd',min_length=3)
      def clean(self):
        cleaneddata=super().clean()  
        newpassword=cleaneddata.get('newpassword')
        confirmpassword=cleaneddata.get('confirmpassword')
        if newpassword and confirmpassword and newpassword != confirmpassword:
            raise forms.ValidationError('passoword do not match')                          
class profileform(forms.ModelForm):
    Name = forms.CharField(label='name', max_length=200, required=True)
    age= forms.CharField(label='aboutme')
    content= forms.CharField(label='location', required=True)
    address=forms.CharField(label='address', required=True)
    image = forms.ImageField(label='image', required=False)
    email=forms.EmailField(label='email',required=True)
  

    class Meta:
        model = profile
        fields = ['Name', 'age', 'content', 'image','address']

    # Field-level validation (cleaning each field)
    def clean_title(self):
        name = self.cleaned_data.get('Name')
        if name and len(name) < 5:
            raise forms.ValidationError('title must be at least 5 characters long.')
        return name

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if content and len(content) < 10:
            raise forms.ValidationError('content must be at least 10 characters long.')
        return content

    def save(self, commit=True):
        # Save the post object, but don't commit to the database yet
        post_instance = super().save(commit=False)

        # Get the image from the cleaned data
        image = self.cleaned_data.get('image')
        
        # If no image is provided, set a default image
        if not image:
            post_instance.image = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/450px-No_image_available.svg.png"
        else:
            post_instance.image = image  # Use the uploaded image if present

        if commit:
            post_instance.save()  # Save the post to the database

        return post_instance
from django import forms
from .models import quiz

class quizform(forms.ModelForm):
    name = forms.CharField(max_length=100, required=False)
    title = forms.CharField(max_length=100, required=False)
    content = forms.CharField(max_length=100, required=False)
    image = forms.ImageField(required=False)
   
    week = forms.CharField(required=False, max_length=100)
    
    # These fields will represent the word-image pairs.
    # They will be added dynamically in the template.
    word_0 = forms.CharField(max_length=100, required=True, label="Word 1")
    image_0 = forms.ImageField(required=True, label="Image 1")
    word_1 = forms.CharField(max_length=100, required=False, label="Word 2")
    image_1 = forms.ImageField(required=False, label="Image 2")
    
    
    class Meta:
        model = quiz
        fields = ['name', 'title', 'content', 'image', 'week', 'word_0', 'image_0', 'word_1', 'image_1']


        