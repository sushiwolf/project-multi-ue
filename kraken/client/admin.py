from django.contrib import admin

from .models import City,Param,Problem,Problem_City_Association

admin.site.register(City)
admin.site.register(Param)
admin.site.register(Problem)
admin.site.register(Problem_City_Association)
