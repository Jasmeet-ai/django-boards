from re import L
from django.db.models import Count
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models import Board, Topic,Post
from .forms import NewTopicForm, ReplyTopicForm
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, ListView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage
# Create your views here.

''' Function based view
def home(request):
    board = Board.objects.all()
    return render(request, 'boards/home.html',{'board':board})

'''
class BoardListView(ListView):
    model=Board
    template_name = 'boards/home.html'
    context_object_name = 'board'

def board_topics(request,pk):
    board = get_object_or_404(Board, pk=pk)
    queryset = board.topics.order_by('-last_update').annotate(replies=Count('posts')-1)
    paginator = Paginator(queryset, 20)
    page = request.GET.get('page',1) 

    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        # fallback to the first page
        topics = paginator.page(1)
    except EmptyPage:
        # probably the user tried to add a page number
        # in the url, so we fallback to the last page
        topics = paginator.page(paginator.num_pages)
    
    return render(request, 'boards/topics.html',{'board':board, 'topics':topics})

@login_required
def new_topic(request,pk):
    board = get_object_or_404(Board, pk=pk)
    # user = User.objects.first()

    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
           topic = form.save(commit=False)
           topic.board = board
           topic.starter = request.user
           topic = form.save()
           post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user,
            )
           return redirect('board_topics', pk=board.pk, topic_pk=topic.pk)
    else:
        form = NewTopicForm()
    return render(request, 'boards/new_topic.html', {'form': form})

    # if request.method=="POST":
    #     message = request.POST['message']
    #     subject =  request.POST['message']

    #     user = User.objects.first()

    #     topic = Topic.objects.create(subject=subject, board=board,starter=user)

    #     post = Post.objects.create(message=message,topic=topic,created_by=user )

    #     return redirect('board_topics', pk=board.pk)
  
        

    #return render(request, 'boards/new_topic.html',{'board':board})

def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views+=1
    topic.save()
    return render(request, 'boards/topic_posts.html', {'topic': topic})

@login_required
def reply_topic(request,pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk )
    # user = User.objects.first()

    if request.method == 'POST':
        form = ReplyTopicForm(request.POST)
        if form.is_valid():
           post = form.save(commit=False)
           post.topic = topic
           post.created_by = request.user
           post = form.save()

           topic.last_update=timezone.now()
           topic.save()
           return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = ReplyTopicForm()
    return render(request, 'boards/reply_topic.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model=Post
    fields= ('message',)
    template_name = 'boards/edit_post.html' 
    pk_url_kwarg = "post_pk"
    context_object_name = "post"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by = self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect("topic_posts", pk = post.topic.board.pk , topic_pk = post.topic.pk)


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model=User
    fields= ('first_name','last_name','email',)
    template_name = 'boards/my_account.html' 
    success_url = reverse_lazy('my_account')

    def get_object(self):
        return self.request.user
