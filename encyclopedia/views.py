import random
import re
from cmath import log
from distutils.log import Log
from django.shortcuts import redirect, render
from django import forms

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request,name):
    article = util.get_entry(name)
    if article == None:
        return render(request, "encyclopedia/error.html",{
            "error":"Article with this name was not found"
        })
    articles_list = util.list_entries()
    number_of_article = [x.upper() for x in articles_list].index(name.upper())
    return render(request, "encyclopedia/wiki.html", {
        "name": articles_list[number_of_article],
        "article": util.get_entry(name)
    })

def search(request):
    query = request.GET["q"]
    if query.upper() in [x.upper() for x in util.list_entries()]:
       return redirect(f"wiki/{query}")
    filtered_values = list(filter(lambda v: re.match(f'.*{query}.*', v , re.IGNORECASE), util.list_entries()))
    return render(request, "encyclopedia/search.html", {
        "entries": filtered_values,
        "q":query
    })

class NewArticleForm(forms.Form):
    name = forms.CharField(label="Name")
    article = forms.CharField(widget=forms.Textarea({'rows':2, 'cols':2}),label="Article")

def create(request):
    if request.method == "POST":
        form = NewArticleForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            if name.upper() in [x.upper() for x in util.list_entries()]:
                return render(request, "encyclopedia/error.html",{
                    "error":"Article already exisist"
                })
            article = form.cleaned_data['article']
            util.save_entry(name,article)
            return redirect("index")
    return render(request, "encyclopedia/create.html",{
        "form":NewArticleForm()
    })


class EditArticleForm(forms.Form):
    article = forms.CharField(widget=forms.Textarea({'rows':2, 'cols':2}),label="Article")

def edit(request,name):
    if request.method == "POST":
        form = EditArticleForm(request.POST)
        if form.is_valid():
            article = form.cleaned_data['article']
            util.save_entry(name,article)
            return redirect(f"/wiki/{name}")
    article = util.get_entry(name)
    if article == None:
        return render(request, "encyclopedia/error.html",{
            "error":"Article with this name was not found"
        })
    articles_list = util.list_entries()
    number_of_article = [x.upper() for x in articles_list].index(name.upper())
    return render(request, "encyclopedia/edit.html", {
        "name": articles_list[number_of_article],
        "form": EditArticleForm({"article": util.get_entry(name)})
    })


def random_choice(request):
    return redirect(f"/wiki/{random.choice(util.list_entries())}")