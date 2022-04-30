from distutils.command.upload import upload
from django.db import models
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
