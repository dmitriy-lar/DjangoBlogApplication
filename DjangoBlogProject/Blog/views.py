from django.db.models import Q
from django.shortcuts import render, redirect
from .models import PostModel, CategoryModel, Comments, CustomUserModel, PostView
from .forms import NewsLetterForm, CommentsForm, UserChangeForm, PostCreationForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def index(request):
    slider_posts = PostModel.objects.order_by('-date_created')[:4]
    posts = PostModel.objects.order_by('-date_created')[:9]

    first_col = posts[:3]
    second_col = posts[3:6]
    third_col = posts[6:9]

    trending_posts = PostModel.objects.order_by('-view_count')[:5]
    categories = CategoryModel.objects.all()

    if request.method == 'POST':
        form = NewsLetterForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = NewsLetterForm()

    context = {
        'slider_posts': slider_posts,
        'first_col': first_col,
        'second_col': second_col,
        'third_col': third_col,
        'trending_posts': trending_posts,
        'categories': categories,
        'form': form
    }
    return render(request, 'Blog/index.html', context)


def category(request, pk):
    category_obj = CategoryModel.objects.get(pk=pk)
    categories = CategoryModel.objects.all()
    posts = PostModel.objects.filter(category__pk=pk).order_by('-date_created')
    popular_posts = PostModel.objects.order_by('-view_count')[:6]
    latest_posts = PostModel.objects.order_by('-date_created')[:6]

    paginator = Paginator(posts, 5)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'categories': categories,
        'category_obj': category_obj,
        'popular_posts': popular_posts,
        'latest_posts': latest_posts,
        'page_request_var': page_request_var,
        'posts': paginated_queryset

    }

    return render(request, 'Blog/category.html', context)


def search(request):
    categories = CategoryModel.objects.all()
    popular_posts = PostModel.objects.order_by('-view_count')[:6]
    latest_posts = PostModel.objects.order_by('-date_created')[:6]

    queryset = PostModel.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        )

    context = {
        'categories': categories,
        'popular_posts': popular_posts,
        'latest_posts': latest_posts,
        'queryset': queryset,
        'search_name': query,
    }
    return render(request, 'Blog/search-result.html', context)


def post(request, pk):
    categories = CategoryModel.objects.all()
    popular_posts = PostModel.objects.order_by('-view_count')[:6]
    latest_posts = PostModel.objects.order_by('-date_created')[:6]

    post = PostModel.objects.get(pk=pk)
    if request.user.is_authenticated:
        PostView.objects.get_or_create(author=request.user, post=post)
        # temp_post = PostModel.objects.get(pk=pk)
        post.view_count = post.get_view_count
        post.save()

    comments = Comments.objects.filter(post__pk=pk).order_by('-time_created')
    if request.POST:
        form = CommentsForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.instance.post = post
            form.save()
            return redirect('post', pk)
    else:
        form = CommentsForm()

    context = {
        'categories': categories,
        'popular_posts': popular_posts,
        'latest_posts': latest_posts,
        'post': post,
        'comments': comments,
        'form': form,
    }
    return render(request, 'Blog/single-post.html', context)


def profile(request):
    categories = CategoryModel.objects.all()
    author = CustomUserModel.objects.get(pk=request.user.pk)
    comments = Comments.objects.filter(author=request.user)

    posts = PostModel.objects.filter(author=request.user)
    context = {
        'author': author,
        'comments': comments,
        'categories': categories,
        'posts': posts,
    }

    return render(request, 'Blog/profile.html', context)


def update(request):
    categories = CategoryModel.objects.all()

    if request.POST:
        form = UserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserChangeForm(
            initial={
                'username': request.user.username,
                'email': request.user.email,
                'profile_picture': request.user.profile_picture
            }
        )

    context = {
        'form': form,
        'categories': categories,
    }

    return render(request, 'Blog/update.html', context)




def my_posts(request):
    categories = CategoryModel.objects.all()
    popular_posts = PostModel.objects.order_by('-view_count')[:6]
    latest_posts = PostModel.objects.order_by('-date_created')[:6]

    posts = PostModel.objects.filter(author=request.user).order_by('-date_created')

    context = {
        'categories': categories,
        'popular_posts': popular_posts,
        'latest_posts': latest_posts,
        'posts': posts,
    }

    return render(request, 'Blog/my_posts.html', context)


def create_post(request):
    if request.POST:
        form = PostCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = request.user

            form.save()
            return redirect('my_posts')
    else:
        form = PostCreationForm()

    context = {
        'form': form,
    }

    return render(request, 'Blog/create-post.html', context)


def update_post(request, pk):
    post = PostModel.objects.get(pk=pk)

    if request.POST:
        form = PostCreationForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('my_posts')
    else:
        form = PostCreationForm(
            initial={
                'title': post.title,
                'overview': post.overview,
                'content': post.content,
                'category': post.category,
                'thumbnail': post.thumbnail
            }
        )
    context = {
        'form': form
    }

    return render(request, 'Blog/update-post.html', context)


def delete_post(request, pk):
    post = PostModel.objects.get(pk=pk)

    if request.POST:
        post.delete()
        return redirect('my_posts')

    context = {
        'post': post,
    }

    return render(request, 'BLog/delete-post.html', context)
