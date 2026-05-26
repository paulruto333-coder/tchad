import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'airtel_project.settings')
django.setup()

from withdraw.models import StarlinkPackage

# Delete old packages and create fresh Kenya KES packages
StarlinkPackage.objects.all().delete()

packages = [
    {"name": "Starter Package", "description": "Ideal for light usage", "price": 70.00, "data_limit": "5GB"},
    {"name": "Basic Package", "description": "Perfect for browsing & social media", "price": 210.00, "data_limit": "15GB"},
    {"name": "Standard Package", "description": "Great for streaming & remote work", "price": 430.00, "data_limit": "30GB"},
    {"name": "Premium Package", "description": "For the whole family", "price": 900.00, "data_limit": "60GB"},
    {"name": "Business Package", "description": "Professional high-speed use", "price": 1700.00, "data_limit": "100GB"},
    {"name": "Unlimited Package", "description": "Unlimited data for power users", "price": 2500.00, "data_limit": "Unlimited"},
]

for pkg in packages:
    p = StarlinkPackage.objects.create(**pkg, is_active=True)
    print(f"Created {p.name} - KES {p.price}")

print("All Kenya packages created successfully.")
