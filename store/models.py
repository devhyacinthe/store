from distutils.command.upload import upload
from django.utils import timezone
from django.db import models
from pyparsing import OnlyOnce
from shop.settings import AUTH_USER_MODEL
from django.urls import reverse

# Create your models here.
"""
Ca c'est la planiquation de products
Product
-Nom (String)
-Prix (double)
-La quantite en stock (int)
-Description
-Image

Ensuite on creer notre classe avec la class avec l'ORM de django
"""


class Products(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    price = models.FloatField(default=0.0)
    stock = models.IntegerField(default=0)
    # pour q'on puisse avoir le choix de ne pas mettre une description
    description = models.TextField(blank=True)
    # Ou on veut mettre cette image dans le dossier products et on veut que ca puisse etre nul
    image = models.ImageField(upload_to="products", blank=True, null=True)

    def __str__(self):
        # c'est pour afficher notre classe(c'est la methode toString() en java)
        return f"{self.name}: {self.stock}"

    def get_absolute_url(self):
        return reverse("products", kwargs={"slug": self.slug})


"""
Article(Order)
-Utilisateur
-Produit
-Quantité
-Commandé ou non

"""


class Order(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"


"""
Panier(Cart)
-Utilisateur
-Articles
-Commandé ou non
-Date de la commande
"""


class Cart(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)

    def __str__(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        for order in self.orders.all():
            order.ordered = True
            order.ordered_date = timezone.now()
            order.save()

        self.orders.clear()
        super().delete(*args, **kwargs)
