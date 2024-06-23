from django.contrib import admin
from .models import User, Manager, Profile


class UserAdmin(admin.ModelAdmin):
    list_display = ["telephone", "full_name", "email"]


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ["full_name", "email", "subject"]


class ProfileManager(admin.ModelAdmin):
    list_display = ["get_full_name", "get_bio", "get_phone"]

    def get_full_name(self, obj):
        return obj.profile.user.full_name

    get_full_name.short_description = "Full Name"

    def get_bio(self, obj):
        return obj.profile.bio

    get_bio.short_description = "Bio"

    def get_phone(self, obj):
        return obj.profile.phone

    get_phone.short_description = "Phone"

    get_full_name.admin_order_field = "profile__full_name"
    get_bio.admin_order_field = "profile__bio"
    get_phone.admin_order_field = "profile__phone"


admin.site.register(User, UserAdmin)
admin.site.register(Manager, ProfileManager)
admin.site.register(Profile)
