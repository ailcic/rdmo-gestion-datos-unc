# Configuración compartida de la instancia RDMO de la Universidad Nacional de Córdoba.
# Los valores propios de cada máquina (SECRET_KEY, DEBUG, base de datos, ...) van en local.py.

from django.utils.translation import gettext_lazy as _

# El español es el idioma principal: ocupa los campos lang1 del contenido
LANGUAGE_CODE = 'es'

LANGUAGES = (
    ('es', _('Spanish')),
    ('en', _('English')),
)

# Mostrar el texto en otro idioma cuando falta la traducción al español
REPLACE_MISSING_TRANSLATION = True

TIME_ZONE = 'America/Argentina/Cordoba'

# Cuentas locales con registro abierto (django-allauth)
INSTALLED_APPS += [
    'allauth',
    'allauth.account',
]

MIDDLEWARE += [
    'allauth.account.middleware.AccountMiddleware'
]

ACCOUNT = True
ACCOUNT_SIGNUP = True

# En la prueba local los correos se muestran en la consola
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'rdmo@localhost'
