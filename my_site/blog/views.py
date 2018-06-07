from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .models import Post, Comment
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail


# Create your views here.
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
    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'comment_form': comment_form})


def share_post(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    recipient = None
    form = EmailPostForm()

    if request.method == "POST":
        # Form Submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Clean the data
            cleaned_form_data = form.cleaned_data

            # Prepare the email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you to read "{}"'.format(cleaned_form_data['name'],
                                                                   cleaned_form_data['email'],
                                                                   post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title,
                                                                     post_url,
                                                                     cleaned_form_data['name'],
                                                                     cleaned_form_data['comments'])
            # Send email
            send_mail(subject, message, 'overlord@myblog.com', [cleaned_form_data['to']])
            sent = True
            recipient = cleaned_form_data['to']
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent, 'recipient': recipient})
