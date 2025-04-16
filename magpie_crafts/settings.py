from pathlib import Path
import os
from dotenv import load_dotenv
from django.urls import reverse_lazy

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-key-for-development')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Create static directory if it doesn't exist
os.makedirs(STATIC_ROOT, exist_ok=True)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-key-for-development')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    
    # Add these django-allauth apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    
    # Django Oscar apps
    'oscar',
    'oscar.apps.address',
    'oscar.apps.analytics',
    'oscar.apps.catalogue',
    'oscar.apps.catalogue.reviews',
    'oscar.apps.basket',
    'oscar.apps.checkout',
    'oscar.apps.shipping',
    'oscar.apps.payment',
    'oscar.apps.offer',
    'oscar.apps.order',
    'oscar.apps.customer',
    'oscar.apps.search',
    'oscar.apps.voucher',
    'oscar.apps.wishlists',
    'oscar.apps.dashboard',
    'oscar.apps.dashboard.reports',
    'oscar.apps.dashboard.users',
    'oscar.apps.dashboard.orders',
    'oscar.apps.dashboard.catalogue',
    'oscar.apps.dashboard.offers',
    'oscar.apps.dashboard.partners',
    'oscar.apps.dashboard.pages',
    'oscar.apps.dashboard.ranges',
    'oscar.apps.dashboard.reviews',
    'oscar.apps.dashboard.vouchers',
    'oscar.apps.dashboard.communications',
    'oscar.apps.dashboard.shipping',
    'oscar.apps.partner',  # Required for product availability
    'oscar.apps.communication',  # Added missing communication app
    
    # Third-party apps required by Oscar
    'widget_tweaks',
    'haystack',
    'treebeard',
    'sorl.thumbnail',
    'django_tables2',
    
    # Other third-party apps
    'tailwind',
    'django_browser_reload',
    'storages',
    
    # Project apps
    'products',
    'blog',
    'cart',
    'orders',
    'social',
    'videos',
    'ai_content',
]

# Required by Django Oscar
SITE_ID = 1

# Haystack settings (required by Oscar) - Added this missing configuration
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',
    'oscar.apps.basket.middleware.BasketMiddleware',  # Oscar basket middleware
]

ROOT_URLCONF = 'magpie_crafts.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Oscar context processors
                'oscar.apps.search.context_processors.search_form',
                'oscar.apps.checkout.context_processors.checkout',
                'oscar.apps.customer.notifications.context_processors.notifications',
                'oscar.apps.promotions.context_processors.promotions',
            ],
        },
    },
]

WSGI_APPLICATION = 'magpie_crafts.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if os.environ.get('DATABASE_URL'):
    # Production database (PostgreSQL)
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600)
    }
else:
    # Development database (SQLite)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Edmonton'  # Edmonton, Alberta timezone
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# AWS S3 configuration for production
if os.environ.get('USE_S3', 'False') == 'True':
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_LOCATION = 'static'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    DEFAULT_FILE_STORAGE = 'magpie_crafts.storage_backends.MediaStorage'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
else:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Tailwind CSS configuration
TAILWIND_APP_NAME = 'theme'

# Email settings
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.environ.get('EMAIL_HOST')
    EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
    EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
    DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

# Stripe settings
STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY', 'pk_test_51REBhaICm0BfGMhchpHaqPkclDgVfqdIQcVYhheJr1Nv6Yp63Y7i29hfug6URPGsYnLfWXWC9i97O54pFqGhW3hC00pWUJVPL3')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', 'sk_test_51REBhaICm0BfGMhc9sr7BQnZOHNKtDmWkCwNWyyP96CZ8UAiuwdri6yM5RxXELEX6eWy25xaZfnTeuMkyCW9F3Jq00SYqzdq5T')
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET', '')

# OpenAI API settings
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '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')

# Canadian GST rate (5%)
GST_RATE = 0.05

# Currency settings
DEFAULT_CURRENCY = 'CAD'

# Django Allauth settings
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Allauth settings
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True

# Oscar settings - must come after MEDIA_URL is defined
OSCAR_SHOP_NAME = 'Magpie Felt'
OSCAR_SHOP_TAGLINE = 'Handmade Wool Felting Kits and Art'
OSCAR_DEFAULT_CURRENCY = 'CAD'
OSCAR_FROM_EMAIL = 'noreply@magpiefelt.ca'

# URLs and slugs
OSCAR_HOMEPAGE = '/'
OSCAR_ACCOUNTS_REDIRECT_URL = 'customer:profile-view'
OSCAR_BASKET_COOKIE_OPEN = 'oscar_open_basket'
OSCAR_BASKET_COOKIE_SECURE = False
OSCAR_BASKET_COOKIE_LIFETIME = 7 * 24 * 60 * 60
OSCAR_LOGIN_REDIRECT_URL = '/'
OSCAR_SLUG_ALLOW_UNICODE = False
OSCAR_SLUG_MAP = None
OSCAR_SLUG_FUNCTION = 'oscar.core.utils.default_slugifier'

# Recently viewed products
OSCAR_RECENTLY_VIEWED_PRODUCTS = 20
OSCAR_RECENTLY_VIEWED_COOKIE_NAME = 'oscar_history'
OSCAR_RECENTLY_VIEWED_COOKIE_LIFETIME = 7 * 24 * 60 * 60
OSCAR_RECENTLY_VIEWED_COOKIE_SECURE = False
OSCAR_RECENTLY_VIEWED_COOKIE_HTTPONLY = True

# Partner settings
OSCAR_PARTNER_WRAPPERS = {}

# Promotions settings
OSCAR_PROMOTIONS_ENABLED = True

# Communication settings
OSCAR_SAVE_SENT_EMAILS_TO_DB = True

# Rating settings
OSCAR_RATINGS_RANGE = range(1, 6)

# Date/time format settings
OSCAR_DATE_FORMAT = 'j F Y'
OSCAR_DATETIME_FORMAT = 'j F Y, H:i'

# Checkout settings
OSCAR_CHECKOUT_STEPS = [
    'checkout.steps.shipping_address',
    'checkout.steps.shipping_method',
    'checkout.steps.payment_method',
    'checkout.steps.preview',
]
# Pagination settings
OSCAR_PRODUCTS_PER_PAGE = 20
OSCAR_OFFERS_PER_PAGE = 20
OSCAR_REVIEWS_PER_PAGE = 20
OSCAR_NOTIFICATIONS_PER_PAGE = 20
OSCAR_EMAILS_PER_PAGE = 20
OSCAR_ORDERS_PER_PAGE = 20
OSCAR_ADDRESSES_PER_PAGE = 20
OSCAR_STOCK_ALERTS_PER_PAGE = 20
OSCAR_DASHBOARD_ITEMS_PER_PAGE = 20

# Product settings
OSCAR_MISSING_IMAGE_URL = MEDIA_URL + 'image_not_found.jpg'
OSCAR_UPLOAD_ROOT = os.path.join(MEDIA_ROOT, 'uploads/')
OSCAR_DELETE_IMAGE_FILES = True

# Search settings
OSCAR_SEARCH_FACETS = {
    'fields': {
        'product_class': {'name': 'Type', 'field': 'product_class'},
        'rating': {'name': 'Rating', 'field': 'rating'},
    },
    'queries': {
        'price_range': {
            'name': 'Price range',
            'field': 'price',
            'queries': [
                # Price ranges
                ('0_15', 'Under $15'),
                ('15_50', '$15 to $50'),
                ('50_100', '$50 to $100'),
                ('100_', 'Over $100'),
            ]
        }
    }
}

# Order settings
OSCAR_INITIAL_ORDER_STATUS = 'Pending'
OSCAR_INITIAL_LINE_STATUS = 'Pending'
OSCAR_ORDER_STATUS_PIPELINE = {
    'Pending': ('Being processed', 'Cancelled',),
    'Being processed': ('Processed', 'Cancelled',),
    'Processed': ('Shipped', 'Cancelled',),
    'Shipped': ('Delivered', 'Cancelled',),
    'Delivered': (),
    'Cancelled': (),
}
OSCAR_LINE_STATUS_PIPELINE = {
    'Pending': ('Being processed', 'Cancelled',),
    'Being processed': ('Processed', 'Cancelled',),
    'Processed': ('Shipped', 'Cancelled',),
    'Shipped': ('Delivered', 'Cancelled',),
    'Delivered': (),
    'Cancelled': (),
}

# Customer settings
OSCAR_ALLOW_ANON_CHECKOUT = True
OSCAR_ALLOW_ANON_REVIEWS = True
OSCAR_MODERATE_REVIEWS = False
OSCAR_REQUIRED_ADDRESS_FIELDS = ('first_name', 'last_name', 'line1', 'city', 'country', 'postcode')
OSCAR_SEND_REGISTRATION_EMAIL = True
OSCAR_DEFAULT_WISHLIST_NAME = 'Default wishlist'

# Communication settings
OSCAR_EAGER_ALERTS = False
OSCAR_SEND_REGISTRATION_EMAIL = True

# Dashboard settings
OSCAR_DASHBOARD_DEFAULT_ACCESS_FUNCTION = 'oscar.apps.dashboard.nav.default_access_fn'

# Misc settings
OSCAR_COOKIES_SECURE = False
OSCAR_COOKIES_HTTPONLY = True
OSCAR_USE_LESS = False
OSCAR_USE_DATADOG = False
OSCAR_HIDDEN_FEATURES = []
OSCAR_DYNAMIC_CLASS_LOADER = 'oscar.core.loading.default_class_loader'

# Promotions settings
OSCAR_PROMOTION_POSITIONS = (('page', 'Page'),
                            ('right', 'Right-hand sidebar'),
                            ('left', 'Left-hand sidebar'))

# Reviews settings
OSCAR_ALLOW_ANON_REVIEWS = True
OSCAR_MODERATE_REVIEWS = False

# Checkout settings
OSCAR_ALLOW_ANON_CHECKOUT = True
OSCAR_SEARCH_FACETS = {
    'fields': {
        'product_class': {'name': 'Type', 'field': 'product_class'},
        'rating': {'name': 'Rating', 'field': 'rating'},
    },
    'queries': {
        'price_range': {
            'name': 'Price range',
            'field': 'price',
            'queries': [
                # Price ranges
                ('0_15', 'Under $15'),
                ('15_50', '$15 to $50'),
                ('50_100', '$50 to $100'),
                ('100_', 'Over $100'),
            ]
        }
    }
}
# Oscar Dashboard Navigation
OSCAR_DASHBOARD_NAVIGATION = [
    {
        'label': 'Dashboard',
        'icon': 'fas fa-tachometer-alt',
        'url_name': 'dashboard:index',
    },
    {
        'label': 'Catalogue',
        'icon': 'fas fa-sitemap',
        'children': [
            {
                'label': 'Products',
                'url_name': 'dashboard:catalogue-product-list',
            },
            {
                'label': 'Categories',
                'url_name': 'dashboard:catalogue-category-list',
            },
            {
                'label': 'Product Types',
                'url_name': 'dashboard:catalogue-class-list',
            },
        ]
    },
    {
        'label': 'Customers',
        'icon': 'fas fa-users',
        'children': [
            {
                'label': 'Customers',
                'url_name': 'dashboard:users-index',
            },
        ]
    },
    {
        'label': 'Orders',
        'icon': 'fas fa-shopping-cart',
        'children': [
            {
                'label': 'Orders',
                'url_name': 'dashboard:order-list',
            },
        ]
    },
]
    AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    ]

# Allauth settings
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
LOGIN_REDIRECT_URL = '/'

