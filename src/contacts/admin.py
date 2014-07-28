from django.contrib import admin

# Register your models here.
from models import MyUser, Like

class UserAdmin(admin.ModelAdmin):
    pass
class LikeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Like, LikeAdmin)
admin.site.register(MyUser, UserAdmin)