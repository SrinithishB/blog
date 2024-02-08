from django.shortcuts import render,redirect
from .forms import NewRegisterForm
from .models import Profile
from article.models import Article
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    if request.method=="POST":
        form=NewRegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            return redirect('login')
    else:
        form=NewRegisterForm()
    context={
        'form':form
    }
    return render(request,'users/register.html',context)

def profile(request):
    articles=Article.objects.filter(author=request.user).all().order_by("-date")
    context={
        'articles':articles
    }
    return render(request,'users/profile.html',context)

@login_required
def edit_profile(request):
    try:
        profile =request.user.profile
    except Profile.DoesNotExist:
        profile=None
    if request.method=='POST':
        if profile:
            profile.first_name=request.POST.get('first_name')
            profile.last_name=request.POST.get('last_name')
            profile.contact_number=request.POST.get('contact_number')
            profile.bio=request.POST.get('bio')
            if request.FILES.get('image'):
                profile.image=request.FILES['image']
            profile.save()      
        else:
            user=request.user
            first_name=request.POST.get('first_name')
            last_name=request.POST.get('last_name')
            contact_number=request.POST.get('contact_number')
            image=request.FILES['image']
            bio=request.POST.get('bio')
            profile=Profile(user=user,first_name=first_name,last_name=last_name,contact_number=contact_number,image=image,bio=bio)
            profile.save()
        return redirect('profile')
    context={
        'profile':profile
    }
    return render(request,'users/edit_profile.html',context)

def author_profile(request,pk):
    author=User.objects.get(pk=pk)
    articles=Article.objects.filter(author=author)
    count=len(articles)
    context={
        "author":author,
        "count":count
    }
    return render(request,'users/author_profile.html',context)
    
