from django.shortcuts import render
from redis import StrictRedis
from django import forms
from redis import Redis

# Create your views here.

def get_redis():
    return Redis()

class SetCounterForm(forms.Form):
    counter = forms.IntegerField(label="Counter")
    
    def set(self):
        counter = self.cleaned_data['counter']
        redis = get_redis()
        redis.publish('counter', counter)

def index(request):
    return render(request, 'index.html')

def counter(requust):
    form = SetCounterForm(data=requust.POST or None)
    if form.is_valid():
        form.set()
    return render(requust, 'counter.html', context={"form": form})

