from django.contrib import admin


from .models import br

# Register your models here.
class brAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'published')
    list_display_link = ('title', 'content')
    search_fields = ('title', 'content')


admin.site.register(br, brAdmin)