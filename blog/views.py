from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from taggit.models import Tag


from .models import Post, Comment
from .forms import CommentForm


def post_list(request, tag_slug=None):
    posts = Post.published.all()

    paginator = Paginator(posts, 10)  # 10 posts in each page
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    return render(
        request, "post_list.html", {"posts": posts, page: "pages", "tag": tag}
    )


def post_detail(request, post):
    post = get_object_or_404(Post, slug=post, status="published")

    # List of active comments for this post
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == "POST":
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
            return redirect(post.get_absolute_url() + "#" + str(new_comment.id))
    else:
        comment_form = CommentForm()

    return render(
        request,
        "post_detail.html",
        {"post": post, "comments": comments, "comment_form": comment_form},
    )


def reply_page(request):
    if request.method == "POST":

        form = CommentForm(request.Post)

        if form.is_valid():
            post_id = request.POST.get("post_id")
            parent_id = request.POST.get("parent")
            post_url = request.POST.get("post_url")

            reply = form.save(commit=False)

            reply.post = Post(id=post_id)
            reply.parent = Comment(id=parent_id)
            reply.save()

            return redirect(post_url + "#" + str(reply.id))

    return redirect("/")
