from django.core import paginator
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm


def post_share(request, post_id):
    # Получение статьи по идентификатору
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # Форма отправлена на сохранение
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Все формы прошли валидации
            cd = form.cleaned_data
            # Отправка почты
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True

    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})


def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)  # ПО три статьи на каждой странице
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом то возвращаем первую страницу.
        posts = paginator.page(1)
    except EmptyPage:
        # Если номаер страницы юбольше чем общее количесство страниц то вощзвращаем последнюю
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month,
                             publish__day=day)
    # ОБОЖЕ ДА ЭТО АКТИВНЫЕ КОММЕНТАРИИ
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # пользователь отправил комментарий
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post/detail.html',
                  {'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 10
    template_name = 'blog/post/list.html'
# Create your views here.
