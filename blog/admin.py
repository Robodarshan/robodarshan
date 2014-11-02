from django.contrib import admin
from blog.models import story


class storyAdmin(admin.ModelAdmin):
    pass


admin.site.register(story, storyAdmin)
