from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    """
    The list_display attribute allows you to set the fields of your model that
    you want to display in the admin object list page.
    The list page now includes a right sidebar that allows you to filter the
    results by the fields included in the list_filter attribute.
    A search bar has appeared on the page. This is because we have defined a list of
    searchable fields using the search_fields attribute. Just below the search bar, there
    is a bar to navigate quickly through a date hierarchy. This has been defined by the
    date_hierarchy attribute. You can also see that the posts are ordered by Status
    and Publish columns by default. You have specified the default order using the
    ordering attribute.
    """
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)