from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Evenement, Cart, Billet
from .forms import EvenementForm
from django.urls import reverse
from django.template import loader
import datetime
from django.utils import timezone
from django.db.models import Sum
from django.contrib import messages
# Create your views here.


def home(request):
    upcoming_evenements = Evenement.objects.filter(date__gte=timezone.now())
    return render(request, "application/home.html", {'evenements': upcoming_evenements})

def evenement_detail(request, id):
    evenement = get_object_or_404(Evenement, id=id)
    return render(request, 'application/evenement_detail.html', {'evenement': evenement})


@login_required
def add_to_cart(request,id):
    user =request.user
    evenement=get_object_or_404(Evenement, id=id)
    cart, _ = Cart.objects.get_or_create(user=user)

    billet, created = Billet.objects.get_or_create(user=user,
                                                    ordered=False,
                                                     evenement=evenement)

    if created:
        cart.billets.add(billet)
        cart.save()
    else:
        billet.quantite += 1
        billet.save()
    
    return redirect(reverse("cart"))



@login_required
def remove_from_cart(request, id):
    user =request.user
    evenement=get_object_or_404(Evenement, id=id)
    cart, _ = Cart.objects.get_or_create(user=user)

    billet, created = Billet.objects.get_or_create(user=user,
                                                    ordered=False,
                                                     evenement=evenement)
    if billet.quantite > 1:
        billet.quantite -= 1
        billet.save()
    else:
        billet.delete()
    return redirect(reverse('cart'))



@login_required
def cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    return render (request, 'application/cart.html', context={"billets":cart.billets.all()})



@login_required
def delete_cart(request):

    if cart := request.user.cart:
        cart.delete()

    return redirect ('home')





@login_required
def ajouter_evenement(request):
    vendeur = Vendeur.objects.get(user=request.user) 
    if request.method == 'POST':
        form = EvenementForm(request.POST, request.FILES)
        if form.is_valid():
            evenement = form.save(commit=False)
            evenement.vendeurs.add(vendeur)
            evenement.save()
            messages.success(request, "Événement ajouté avec succès!")
            return redirect('list_evenement') 
    else:
        form = EvenementForm()  
    return render(request, 'application/ajouter_evenement.html', {'form': form})






@login_required
def list_evenement(request):
    evenements = Evenement.objects.filter(user=request.user) 
    return render(request, "application/list_evenement.html", {'evenements': evenements})


@login_required
def modifier_evenement(request, id):
    evenement = get_object_or_404(Evenement, id=id)
    vendeur = Vendeur.objects.get(user=request.user)
    if vendeur not in evenement.vendeurs.all():

        messages.error(request,"Vous navez pas le droit de modifier")
        return redirect('list_evenement')
        if request.method == 'POST':
            form = EvenementForm(request.POST, request.FILES, instance=evenement)
            if form.is_valid():
                form.save()

                return redirect('list_evenement')
        else:
            form = EvenementForm(instance=evenement)
    return render(request, 'application/modifier_evenement.html', {'form': form})

@login_required
def supprimer_evenement(request, id):
    evenement = get_object_or_404(Evenement, id=id)
    if request.method == 'POST':
        evenement.delete()
        return redirect('list_evenement')
    return render(request, 'application/supprimer_evenement.html', {'evenement': evenement})


















@login_required
def cart_total(request):

    cart = get_object_or_404(Cart, user=request.user)
    total = sum(Billet.evenement.prix_ticket * Billet.quantite for billet in cart.billets.all())
    return render(request, 'application/cart.html', {'total': total, 'billets': cart.billets.all()})
