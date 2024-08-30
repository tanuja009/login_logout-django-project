from django.views import View
from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from .forms import *


class HomePage(View):
    def get(self, request):
        return render(request, 'home.html')

class Category_List(View):   
    def get(self,request):
            categories=Category.objects.all()
            return render(request,'base.html',{'categories':categories})
    
class Tweet_List(View):
    def get(self, request):
        tweets = Tweet.objects.all().order_by('created_at')  # Removed the underscore before 'created_at'
        return render(request, 'tweet_list.html', {'tweets': tweets})
    
class Tweet_create(View):
    def post(self,request):
        form=TweetForm(request.POST,request.FILES)
        if form.is_valid():
            tweet=form.save(commit=False)
            tweet.user=request.user
            tweet.save()
            return redirect('tweet_List')
        return render(request,'tweet_form.html',{'form':form})
    def get(self,request):
        form=TweetForm()
        return render(request,'tweet_form.html',{'form':form})
    
class Tweet_Edit(View):
    def get(self, request, id):
        tweet = get_object_or_404(Tweet, pk=id)
        form = TweetForm(instance=tweet)
        return render(request, 'Edit_Tweet.html', {'form': form, 'tweet': tweet})

    def post(self, request, id):
        tweet = get_object_or_404(Tweet, pk=id, user=request.user)
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            form.save()
            return redirect('tweet_list')  # Redirect to the 'tweet_list' view after saving
        return render(request, 'Edit_Tweet.html', {'form': form, 'tweet': tweet})
        
class Tweet_Delete(View):
    def post(self,request,id):
        tweet=get_object_or_404(Tweet,pk=id,user=request.user)
        tweet.delete()
        return redirect('tweet_list')
    
    

        

        
        
  
    

