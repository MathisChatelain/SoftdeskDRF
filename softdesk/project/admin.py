from django.contrib import admin
from .models import CustomUser, Project, Contributor, Issue, Comment

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Project)
admin.site.register(Contributor)
admin.site.register(Issue)
admin.site.register(Comment)
