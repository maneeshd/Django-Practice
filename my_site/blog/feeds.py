from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post


class LatestPostsFeed(Feed):
    title = "My Blog"
    link = "/blog/"
    description = "New posts from My Blog."

    def items(self):
        return Post.published.all()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)
