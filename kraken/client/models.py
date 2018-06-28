from django.db import models

class Param(models.Model):
    param_temp = models.DecimalField(max_digits=10,decimal_places=10,default=0)

class Problem(models.Model):
    problem_name = models.CharField(max_length=200)
    problem_algo_used = models.CharField(max_length=200)
    problem_date_essai = models.DateTimeField('date published')
    problem_param_used = models.ForeignKey(Param,on_delete=models.CASCADE)
    # en km, deux chiffres après la virgule, 999 999km max
    problem_length_cycle = models.DecimalField(max_digits=10,decimal_places=2)
    # en seconde
    problem_time_to_resolve = models.DecimalField(max_digits=5,decimal_places=2)
    problem_author = models.CharField(max_length=200)

class City(models.Model):
    city_name = models.CharField(max_length=200)
    city_lat = models.DecimalField(max_digits=10,decimal_places=3)
    city_lg = models.DecimalField(max_digits=10,decimal_places=3)

    def __str__(self):
        return self.city_name

class Problem_City_Association(models.Model):
    city = models.ForeignKey(City,on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem,on_delete=models.CASCADE)
