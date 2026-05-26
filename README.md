# Starlink DRC Reseller System

A complete Django-based Starlink data package reseller system localized for the Democratic Republic of the Congo (DRC). Users can purchase Starlink data packages using Airtel Money.

## Features

- **Starlink Package Selection**: Choose from various data packages starting from 1,500 CDF.
- **Airtel Money Integration**: Secure payment flow using Airtel Money (dummy verification).
- **Multi-Step Flow**:
  1. Package Selection (Landing Page)
  2. Airtel Number + PIN Entry
  3. OTP Verification (Multiple attempts)
  4. Success Confirmation
- **Network Dashboard**: Real-time network status and diagnostic tools.
- **Records Page**: View all submitted orders with status tracking.
- **Telegram Notifications**: Real-time notifications for new orders and payment attempts.
- **Admin Panel**: Django admin interface for managing packages and orders.

## Project Structure

```
starlink_drc/
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment configuration template
├── README.md                          # This file
├── airtel_project/                    # Django project settings
│   ├── settings.py                    # Project settings
│   ├── urls.py                        # URL routing
│   ├── wsgi.py                        # WSGI configuration
│   └── asgi.py                        # ASGI configuration
├── withdraw/                          # Django app
│   ├── migrations/                    # Database migrations
│   ├── templates/                     # HTML templates
│   │   ├── base.html                  # Base template
│   │   ├── landing.html               # Package selection
│   │   ├── withdraw.html              # Airtel + PIN entry
│   │   ├── otp_verify.html            # OTP verification
│   │   ├── success.html               # Success confirmation
│   │   ├── records.html               # All orders
│   │   └── network_dashboard.html     # Network status
│   ├── models.py                      # Starlink models
│   ├── views.py                       # Application views
│   └── urls.py                        # App URL routing
└── frontend/
    └── static/
        └── images/                    # Static images (Airtel logo, DRC flag, etc.)
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Extract the Project
```bash
cd starlink_drc
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run Database Migrations
```bash
python manage.py migrate
```

### Step 4: Run Development Server
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000/`

## Localization Details (DRC)

- **Currency**: Congolese Franc (CDF)
- **Minimum Price**: 1,500 CDF
- **Phone Prefix**: +243
- **Payment Provider**: Airtel Money DRC

## Support

For issues or questions, contact support@starlinkrdc.reseller

## License

MIT License
