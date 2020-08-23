from urllib.parse import quote_plus
from django.shortcuts import render, get_object_or_404,redirect
from django.shortcuts import HttpResponse,HttpResponseRedirect,Http404
from django.contrib import messages
from .models import postspage
from.forms import postform
from .filters import order_filter
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.shortcuts import render,redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import NewUserForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from comments.forms import CommentForm

def home_page(request):
    return render(request,'home.html')

def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect("/userpage")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "login.html",
                    context={"form":form})


def register_page(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            username = form.cleaned_data.get('username')
            login(request, user)
            return redirect("/userpage")
        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])

            return render(request = request,
                          template_name = "register.html",
                          context={"form":form})

    form = NewUserForm
    return render(request = request,
                  template_name = "register.html",
                  context={"form":form})


@login_required(login_url='login')
def logout_page(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("/")


@login_required(login_url='login')
def user_page(request):
    user=request.user
    return render(request,'user.html',{'user':user})

@login_required(login_url='login')
def posts_create(request):
    form=postform(request.POST or None,request.FILES or None)
    if(form.is_valid()):
        instance=form.save(commit=False)
        instance.user =request.user
        instance.save()
        messages.success(request,"Successfully Uploaded")
        return HttpResponseRedirect(instance.get_absolute_url())
    context ={
        "form":form,
    }
    return render(request,'create.html',context)

def posts_detail(request,id):
    instance = get_object_or_404(postspage,id=id)
    string = quote_plus(instance.category)

    initial_data = {
			"content_type": instance.get_content_type.model,
			"object_id": instance.id
	}
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get('object_id')
        messages.success(request,"Comment Successfully Uploaded ")
        content_data = form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
							user = request.user,
							content_type= content_type,
							object_id = obj_id,
							content = content_data,
                            parent=parent_obj,
						)
        return HttpResponseRedirect(instance.get_absolute_url())


    comments=instance.comments#Comment.objects.filter_by_instance(instance)

    context ={
        "string": string,
        "instance": instance,
        "comments":comments,
		"comment_form":form,
    }
    return render(request,'detail.html',context)


def posts_list(request):
    queryset_list = postspage.objects.all().order_by("-timestamp")

    # myFilter = order_filter(request.GET,queryset_list)
    # queryset_list = myFilter.qs

    # queryset_list = postspage.objects.all()
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
				Q(user__username__iexact=query)|
				Q(content__icontains=query)|
				Q(category__iexact=query)
				).distinct()

    paginator = Paginator(queryset_list , 10)
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context ={
        "list":queryset,
    }

    return render(request,'list.html',context)

@login_required(login_url='login')
def posts_update(request,id):
    instance=get_object_or_404(postspage,id=id)
    form=postform(request.POST or None,request.FILES or None,instance=instance)
    if(form.is_valid()):
        instance=form.save(commit=False)
        instance.save()
        messages.success(request,"Successfully Edited")
        return HttpResponseRedirect(instance.get_absolute_url())
    
    context ={
        "instance":instance,
        "form":form,
    }
    return render(request,'create.html',context)

@login_required(login_url='login')
def posts_delete(request,id):
    instance=get_object_or_404(postspage,id=id)
    instance.delete()
    messages.success(request,"Successfully deleted")
    return redirect("userlist")

@login_required(login_url='login')
def user_list(request):

    user = request.user
    queryset_list = postspage.objects.filter(user=request.user).order_by('-timestamp')

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
				Q(user__username__iexact=query)|
				Q(content__icontains=query)|
				Q(category__iexact=query)
				).distinct()

    paginator = Paginator(queryset_list , 10)
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context ={
        "list":queryset,
    }
    return render(request,'list.html',context)

def about(request):
    return render(request,'about.html')

@login_required(login_url='login')
def commented_posts(request):

    user = request.user
    queryset_list = Comment.objects.filter(user=request.user).values_list('object_id', flat=True).order_by('-timestamp')
    queryset_list = postspage.objects.filter(pk__in=queryset_list).order_by('-timestamp')


    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
				Q(user__username__iexact=query)|
				Q(content__icontains=query)|
				Q(category__iexact=query)
				).distinct()

    paginator = Paginator(queryset_list , 10)
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context ={
        "list":queryset,
    }
    return render(request,'list.html',context)