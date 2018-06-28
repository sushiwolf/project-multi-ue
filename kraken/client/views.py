from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
import requests

from .forms import ContactForm
from .models import City

from django.http import JsonResponse

def index(request):

    form = ContactForm(request.POST or None)

    new_villes = City.objects.all()
    villes = []
    for v in new_villes:
        villes.append([v.city_name,float(v.city_lat),float(v.city_lg)])
    print (villes)
    if request.POST:
        iter = request.POST['iteration']
        #villes = [['Caen',49.182,-0.371],['Paris',48.857, 2.352],['Avignon',43.949,4.805],['Nanterre',48.892,2.215],['Roubaix',50.692,3.177],['Nancy',48.692,6.184],['Rouen',49.443, 1.099],['Mulhouse',47.750,7.335],['Limoges',45.833,1.261],['Grenoble',45.188, 5.724]]
        liste_ville = str(villes).replace(" ","")
        liste_ville = str(liste_ville).replace("[","")
        liste_ville = str(liste_ville).replace("]","")
        print(liste_ville)
        r = requests.get('http://127.0.0.1:8080/snippets/last/' + liste_ville + '/' + str(iter))
        villes = r.json()
        print(villes)
    # Nous vérifions que les données envoyées sont valides
    # Cette méthode renvoie False s'il n'y a pas de données
    # dans le formulaire ou qu'il contient des erreurs.
    if form.is_valid():
        # Ici nous pouvons traiter les données du formulaire
        iteration = form.cleaned_data['iteration']

    return render(request,"client/index.html",locals())

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    return HttpResponse("login")

def logout(request):
    return HttpResponse("logout")

def pvc(request):
    return HttpResponse("pvc")

def detail(request, problem_id):
    return HttpResponse("pvc %s" %problem_id)

def result(request, problem_id):
    return HttpResponse("pvc %s result" %problem_id)

def django_view(request):
    # get the response from the URL
    response = requests.get('http://127.0.0.1:8080/snippets/1')
    result = response

    return HttpResponse(result)
