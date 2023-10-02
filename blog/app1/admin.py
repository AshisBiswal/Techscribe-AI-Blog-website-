from django.contrib import admin

from .models import BlogModel,Bloggers,Profile,Addcomment

admin.site.register(BlogModel)

#class BloggersAdmin(admin.ModelAdmin):
    #list_display = ("name", "blog","category")
admin.site.register(Bloggers)
admin.site.register(Profile)
admin.site.register(Addcomment)

