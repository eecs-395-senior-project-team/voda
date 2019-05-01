from django.contrib import admin
from .models import Sources, States, Counties, Cities, Contaminants, SourceLevels, StateAvgLevels

admin.site.register(Sources)
admin.site.register(States)
admin.site.register(Counties)
admin.site.register(Cities)
admin.site.register(Contaminants)
admin.site.register(SourceLevels)
admin.site.register(StateAvgLevels)
