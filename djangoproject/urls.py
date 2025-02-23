"""
URL configuration for djangoproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from adminpanel import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.main),
    path('index1/',views.index1,name='index1'),
           path('register/',views.register,name='register'),
           path('login/',views.login,name='login'),
           path('forgotpassword/',views.forgotpassword,name='forgotpassword'),
           path('dyslexia/',views.dyslexia,name='dyslexia'),
           path('texttospeech',views.texttospeech,name='texttospeech'),
           path('example/',views.example,name='example'),
           path('resetpassword/<uidb64>/<token>',views.resetpassword,name='resetpassword'),
           path('logout/', views.logout, name='logout'),
           path('about/',views.about,name='about'),
           path('game/',views.game,name='game'),
           path('profiles/',views.profiles,name='profiles'),
           path('createprofile/<int:postid>/',views.createprofile,name='createprofile'),
           path('addprofiles/',views.addprofiles,name="addprofiles"),
             

          path('contact/',views.contact,name='contact'),
          path('graph/',views.graph,name='graph'),
          path('result/',views.result,name='result'),
          path('finalresult/',views.finalresult,name='finalresult'),
          path('spell/',views.spell,name='spell'),


           path("speechtotext/",views.speechtotext,name='speechtotext') ,
           path('game2/',views.game2,name='game2'),

           path('texttospeechtamil',views.texttospeechtamil,name='texttospeechtamil'),
           path('attempt/<int:postid>',views.attempt,name='attempt'),
           path('graph2/', views.graph2, name='graph2'),
           path('addquiz/',views.addquiz,name="addquiz"),
           path('home/',views.home,name='home'),
           path('chat/', views.chat, name='chat'),
           path('avinash/<int:postid>',views.avinash,name="avinash"),
           path('speechquizcard/',views.speechquizes,name="speechquizcard"),
           path('courses/',views.coursesda,name="courses"),
           path('attemptcourses/<int:postid>',views.attemptcourses,name="attemptcourses"),
           path('leaderboarda/',views.leaderboarda,name='leaderboard'),
           path('leaderboardview/',views.leaderboardview,name='leaderboardview'),
           















    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
