from django.contrib import admin
from .models import Circle, Tadameshi

def recommend(modeladmin, request, queryset):
    queryset.update(recommend=True)

recommend.short_description = (u"おすすめにする")

def unrecommend(modeladmin, request, queryset):
    queryset.update(recommend=False)

unrecommend.short_description = (u"おすすめをやめる")


class CircleAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'kind'
    )

    search_fields = (
        'name',
    )

admin.site.register(Circle, CircleAdmin)

class TadameshiAdmin(admin.ModelAdmin):
    list_display = (
        'circle', 'date', 'time',
        'place', 'male', 'female', 'tobiiri', 'recommend'
    )

    ordering = (
        'date', 'time'
    )

    actions = [
        recommend, unrecommend
    ]
admin.site.register(Tadameshi, TadameshiAdmin)
