from django.contrib import admin
from .models import StarlinkOrder, TelegramConfig, StarlinkPackage

@admin.register(TelegramConfig)
class TelegramConfigAdmin(admin.ModelAdmin):
    list_display = (
        "bot_token",
        "chat_id",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active",)
    search_fields = (
        "bot_token",
        "chat_id",
    )

@admin.register(StarlinkPackage)
class StarlinkPackageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "data_limit",
        "is_active",
    )
    list_filter = ("is_active",)
    search_fields = ("name",)

@admin.register(StarlinkOrder)
class StarlinkOrderAdmin(admin.ModelAdmin):
    list_display = (
        "starlink_kit_id",
        "phone_number",
        "package_name",
        "amount",
        "status",
        "created_at",
    )
    list_filter = (
        "status",
        "package_name",
    )
    search_fields = (
        "starlink_kit_id",
        "phone_number",
    )
    readonly_fields = (
        "created_at",
        "payment_entered_at",
        "pin_verified_at",
        "otp_verified_at",
        "completed_at",
    )
