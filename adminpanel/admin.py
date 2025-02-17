from django.contrib import admin
from .models import leaderboard, post,profile, speechquiz2,words,quiz,courses
# Register your models here.
admin.site.register(post)
admin.site.register(profile)
admin.site.register(words)
admin.site.register(quiz)
admin.site.register(courses)
admin.site.register(leaderboard)
admin.site.register(speechquiz2)
