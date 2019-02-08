from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.views.generic import ListView
# from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from .models import Post
from .forms import EmailPostForm, CommentForm
from taggit.models import Tag


# Create your views here.
def post_list(request, tag_slug=None):
    """
    List the posts in the home page (3 posts per page)
    """
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)   # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page,
                                                   'posts': posts,
                                                   'tag': tag})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post,
                             slug=slug,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    # List of active comments for this post
    comments = post.comments.filter(active=True)
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
            to_next = request.POST.get('next', '/blog/')
            return HttpResponseRedirect(to_next)
    else:
        comment_form = CommentForm()
    sent = request.session.get("sent", False)
    recipient = request.session.get("recipient", None)
    if sent:
        request.session["sent"] = False
        request.session["sent"] = None

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'comment_form': comment_form,
                                                     'sent': sent,
                                                     'recipient': recipient,
                                                     'similar_posts': similar_posts})


def share_post(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')

    # Create the form object
    form = EmailPostForm()

    if request.method == "POST":
        # Form Submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Clean the data
            cleaned_form_data = form.cleaned_data

            # Prepare the email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} recommends you to read "{}"'.format(cleaned_form_data['name'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title,
                                                                     post_url,
                                                                     cleaned_form_data['name'],
                                                                     cleaned_form_data['comments'])
            # Send email
            # send_mail(subject, message, 'overlord@myblog.com', [cleaned_form_data['to']])
            recipient = cleaned_form_data['to']
            request.session["sent"] = True
            request.session["recipient"] = recipient
            to_next = request.POST.get('next', '/blog/')
            print(to_next)
            return HttpResponseRedirect(to_next)
    return render(request, 'blog/post/share.html', {'post': post, 'form': form})
