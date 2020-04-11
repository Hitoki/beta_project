from django.contrib import admin

from insane_app.models import *
# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Story)
admin.site.register(StoryImage)
admin.site.register(StoryLike)
admin.site.register(Profile)
admin.site.register(Membership)
admin.site.register(SanityRank)
admin.site.register(UserGroup)
admin.site.register(
    ProductImage,
    readonly_fields = ('image_tag',)
)
