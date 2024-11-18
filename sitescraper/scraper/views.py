from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
import requests
from bs4 import BeautifulSoup
from .models import Link

# Create your views here.
def scrape(request):
    if request.method == "POST":
        site = request.POST.get("site", "")
    
        page = requests.get(site)
        soup = BeautifulSoup(page.text, 'html.parser')

        for link in soup.find_all('a'):
            link_addresses = link.get('href')
            link_text = link.string
            Link.objects.create(address=link_addresses, name=link_text)
            
        return HttpResponseRedirect("/")
    else:
        data = Link.objects.all()
        
    return render(request, 'scraper/results.html', {'data':data})

def clear(request):
    Link.objects.all().delete()
    data = Link.objects.all()    

    return redirect(scrape)