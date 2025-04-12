from django.contrib import admin
from .models import UserActivity, badges, leaderboard, notes, post,profile, speechquiz2,words,quiz,courses
# Register your models here.
admin.site.register(post)
admin.site.register(profile)
admin.site.register(words)
admin.site.register(quiz)
admin.site.register(courses)
admin.site.register(leaderboard)
admin.site.register(speechquiz2)
admin.site.register(badges)
admin.site.register(UserActivity)
admin.site.register(notes)
from .models import Topic, Question, StudentPerformance

admin.site.register(Topic)
admin.site.register(Question)
admin.site.register(StudentPerformance)
