from django.db import models

class View_lp(models.Model):
     id_int= models.IntegerField(null = True)
     id_lampe = models.CharField(max_length=30)
     status = models.BooleanField(null=False, blank= False)
     date_alum = models.CharField(max_length=30)
     date_ext = models.CharField(max_length=30)
     nom_humain = models.CharField(max_length=20)
     consomation = models.FloatField(null =True)
     consomation_f = models.FloatField(null =True)
     def __str__(self):
          return self.id_lampe 
              
class autorisation(models.Model):
     nom = models.CharField(max_length=20)
     categorie = models.CharField(max_length=20)
     numtel = models.IntegerField()
     status_lampe = models.BooleanField(null=False, blank= False)
     status_alarme = models.BooleanField(null=False, blank= False)
     psswd = models.CharField(null= True, max_length=20)
     alarme_on = models.BooleanField(null=True, blank= False)
     def __str__(self):
          return self.nom 
     
# Create your models here.
