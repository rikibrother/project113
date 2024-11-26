from django.contrib import admin
from .models import student, Extended, Movie
# Register your models here.


class SuperAdmin(admin.ModelAdmin):
    list_display = ("title", "released", "director", "writer")
    list_filter = ("genre", "released", "rated", "writer")
    search_fields = ("title", "plot")
    # exclude= ('title', 'director')
    # fields = (("title", 'released'), 'writer','director' ) #if want to show all then either mention __all__ or no need to mention this as all is auto
    
    
    fieldsets =(
        ('Basic Info', {
            'fields' : (("title", "released"), ("director", "writer"))
        }),
        ('Detailed Info', {
            'classes' :('collapse',),
            'fields' :(("genre", "language"),)
         }),
        
    )

admin.site.register(student)
admin.site.register(Extended)
admin.site.register(Movie, SuperAdmin)
