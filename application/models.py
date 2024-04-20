from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone



# Create your models here.
class Evenement(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date = models.DateTimeField()
    location = models.CharField(max_length=100)
    prix_ticket = models.DecimalField(max_digits=10, decimal_places=0)
    stock=models.IntegerField(default=0)
    thumbnail=models.ImageField(upload_to="products",blank=True,null=True)
    #user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

#(Order) Article
class Billet(models.Model):

    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE)
    #quantite = models.PositiveIntegerField(blank=True, null=True)
    quantite = models.PositiveIntegerField(default=1)

    #commande ou non
    ordered=models.BooleanField(default=False)
    ordered_date=models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return f"{self.evenement.titre} ({self.quantite})"


#Panier
class Cart(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #articles    
    billets=models.ManyToManyField(Billet)
    #Commande ou non
   
 

    def __str__(self):
        return  self.user.username


    
    def delete(self, *args,**kwargs):
    
        for billet in self.billets.all():

            billet.ordered=True
            billet.ordered_date=timezone.now()
            billet.save()

        self.billets.clear()
        super().delete(*args,**kwargs)


    
    def total(self):

        total = 0
        for billet in self.billets.all():
            total += self.prix_ticket * self.quantite
        return total
