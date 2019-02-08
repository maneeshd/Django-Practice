from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


# Create your Model Managers here.
class DraftedManager(models.Manager):
    """
    Get only the drafted posts.
    """
    def get_queryset(self):
        return super(DraftedManager, self).get_queryset().filter(status='draft')


class PublishedManager(models.Manager):
    """
    Get only the published posts.
    """
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


# Create your models here.
class Post(models.Model):
    """
    title :   This is the field for the post title. This field is CharField , which
              translates into a VARCHAR column in the SQL database.

    slug :    This is a field intended to be used in URLs. A slug is a short label
              containing only letters, numbers, underscores, or hyphens. We will use the
              slug field to build beautiful, SEO-friendly URLs for our blog posts. We have
              added the unique_for_date parameter to this field so we can build URLs
              for posts using the date and slug of the post. Django will prevent from
              multiple posts having the same slug for the same date.

    author :  This field is ForeignKey . This field defines a many-to-one
              relationship. We are telling Django that each post is written by a user and
              a user can write several posts. For this field, Django will create a foreign
              key in the database using the primary key of the related model. In this case,
              we are relying on the User model of the Django authentication system. We
              specify the name of the reverse relationship, from User to Post , with the
              related_name attribute. We are going to learn more about this later.

    body :    This is the body of the post. This field is TextField , which translates
              into a TEXT column in the SQL database.
              publish : This datetime indicates when the post was published. We use
              Django's timezone now method as default value. This is just a timezone-aware
              datetime.now .

    created : This datetime indicates when the post was created. Since we
              are using auto_now_add here, the date will be saved automatically when
              creating an object.

    updated : This datetime indicates the last time the post has been updated.
              Since we are using auto_now here, the date will be updated automatically
              when saving an object.

    status :  This is a field to show the status of a post. We use a choices
              parameter, so the value of this field can only be set to one of the given choices.
    """
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    author = models.ForeignKey(User, related_name="blog_posts", on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    tags = TaggableManager()

    class Meta:
        """
        The class Meta inside the model contains metadata. We are telling Django to sort
        results by the publish field in descending order by default when we query the
        database. We specify descending order by using the negative prefix.
        """
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    # Register the model managers
    objects = models.Manager()  # Default Manager
    published = PublishedManager()  # Our custom manager
    drafted = DraftedManager()  # Our custom manager

    # Canonical URLs for models
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.strftime('%m'),
                             self.publish.strftime('%d'),
                             self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        """
        Sort comments in anti-chronological order (latest-first).
        """
        ordering = ('-created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)
