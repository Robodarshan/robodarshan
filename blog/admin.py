from django.contrib import admin
from blog.models import story


def make_published(modeladmin, request, queryset):
    queryset.update(published=True)
make_published.short_description = "Published selected stories"


def unpublish(modeladmin, request, queryset):
    queryset.update(published=False)
unpublish.short_description = "Unpublish selected stories"


class storyAdmin(admin.ModelAdmin):
    list_display = ('story_text', 'author_name', 'timestamp', 'published')
    date_hierarchy = 'timestamp'
    readonly_fields = ('author_name',)
    fieldsets = (
        ('Edit Story', {
            'fields': ('title', 'author_name', 'body')
        }),
        ('Publish Story', {
            'classes': ('extrapretty'),
            'fields': ('published',)
        }),
    )
    list_filter = ['published', 'timestamp']
    search_fields = ['title']
    actions = [make_published, unpublish]

    def story_text(self, obj):
        return obj.__unicode__()
    story_text.short_description = 'Story Title'

    def author_name(self, obj):
        return obj.author.get_full_name()
    author_name.short_description = 'Author'

    class Media:
        js = [
            'https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js',
            'blog/tinymce/jquery.tinymce.min.js',
            'blog/editor.js',
        ]


admin.site.register(story, storyAdmin)
