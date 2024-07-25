from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone


class Categorie(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

# Create your models here.
class Evenement(models.Model):

    user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='evenements', null=True, blank=True)

    titre = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date = models.DateTimeField()
    location = models.CharField(max_length=100)
    prix_ticket = models.DecimalField(max_digits=10, decimal_places=0)
    stock=models.IntegerField(default=0)
    thumbnail=models.ImageField(upload_to="products",blank=True,null=True) 

    categorie = models.ForeignKey('Categorie', on_delete=models.CASCADE, default=1)
    class Meta:
        verbose_name = "Evenement"
        verbose_name_plural = "Evenements"

    def __str__(self):
        return f"{self.titre} ({self.categorie.nom})"

class Billet(models.Model):

    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="billets")
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE,related_name="billets")
    #quantite = models.PositiveIntegerField(blank=True, null=True)
    quantite = models.PositiveIntegerField(default=1)

    #commande ou non
    ordered=models.BooleanField(default=False)
    ordered_date=models.DateTimeField(blank=True, null=True)


    class Meta:
        verbose_name = "Billet"
        verbose_name_plural="Billets"

    def __str__(self):
        return f"{self.evenement.titre} ({self.quantite})"


#Panier
class Cart(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #articles    
    billets=models.ManyToManyField(Billet, related_name="carts")
    #Commande ou non
   
    class Meta:
        verbose_name = "Cart"
        verbose_name_plural="Carts"

    def __str__(self):
        return  self.user.username


    
    def delete(self, *args,**kwargs):
    
        for billet in self.billets.all():

            billet.ordered=True
            billet.ordered_date=timezone.now()
            billet.save()

        self.billets.clear()
        super().delete(*args,**kwargs)


    

    def cart_total(self):
    
        total = 0
        for billet in self.billets.all():
            total += billet.evenement.prix_ticket * billet_quantite
            total += billet.evenement.prix_ticket * billet
        return total
