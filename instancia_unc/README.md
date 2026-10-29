Instancia RDMO de la UNC
========================

Configuración de una instancia de [RDMO](https://rdmorganiser.github.io) en español para evaluar el acompañamiento de los planes de gestión de datos (PGD) de los proyectos de la Universidad Nacional de Córdoba.

Esta carpeta cumple el papel de `rdmo-app`: contiene `manage.py`, la configuración de Django (`config/`) y, más adelante, los catálogos traducidos (`catalogos/`). RDMO se instala en modo editable desde la raíz de este repositorio.

Configuración
-------------

- `config/settings/base.py`: configuración compartida (versionada). Español como idioma principal (`LANGUAGE_CODE = 'es'`, `es` primero en `LANGUAGES`), zona horaria de Córdoba, cuentas locales con registro abierto y correos por consola.
- `config/settings/local.py`: configuración propia de cada máquina (no versionada). Se crea a partir de `local.py.ejemplo`.

`REPLACE_MISSING_TRANSLATION = True` hace que, cuando una pregunta no tiene texto en español, se muestre el inglés en lugar de un campo vacío.

Instalación local (prueba)
--------------------------

Requisitos: Python ≥ 3.10, Node 22.22.x (o podman/docker) y pandoc. Para exportar a PDF también hace falta LaTeX (`pdflatex`).

Desde la raíz del repositorio:

```bash
python3 -m venv env
source env/bin/activate
pip install -e ".[allauth]"

npm ci
npm run build:prod
# si la versión de Node no es 22.22.x, compilar en un contenedor:
# podman run --rm -v "$PWD":/app:Z -w /app docker.io/library/node:22.22 npm run build:prod
```

Desde `instancia_unc/`:

```bash
cp config/settings/local.py.ejemplo config/settings/local.py   # y cambiar SECRET_KEY
python manage.py migrate
python manage.py setup_groups
python manage.py createsuperuser
python manage.py runserver
```

La instancia queda en <http://localhost:8000>. La gestión de contenido está en `/management/` y el admin de Django en `/admin/`. En el admin conviene cambiar el *Sitio* a nombre "RDMO UNC" y dominio `localhost:8000`.

Importar el contenido oficial
-----------------------------

Clonar [rdmo-catalog](https://github.com/rdmorganiser/rdmo-catalog) fuera de este repositorio e importar **en este orden**:

```bash
C=/ruta/a/rdmo-catalog/rdmorganiser
python manage.py import $C/domain/attributes.xml
python manage.py import $C/conditions/conditions.xml
python manage.py import $C/options/optionsets.xml
python manage.py import $C/conditions/conditions.xml        # sí, otra vez
python manage.py import $C/questions/questions-rdmo.xml
python manage.py import $C/questions/questions-horizon-europe.xml
python manage.py import $C/questions/questions-smp.xml
python manage.py import $C/tasks/tasks.xml
python manage.py import $C/views/view-horizon-europe.xml    # y las demás vistas que se quieran
```

También se puede importar desde la interfaz: Gestión → Importar.

Los textos en inglés se guardan en `lang2` y los textos en español que traiga el XML (`lang="es"`), en `lang1`. El alemán se descarta porque no figura en `LANGUAGES`.

Estado del español en el contenido oficial (rdmo-catalog, octubre de 2026)
-------------------------------------------------------------------------

| Contenido | Preguntas con texto en español |
|---|---|
| Catálogo Horizon Europe | 84 / 84 |
| Catálogo RDMO | 125 / 137 |
| Plan de gestión de software (SMP) | 0 / 61 |
| Opciones | 515 / 517 |

Las **plantillas de las vistas** (los documentos exportados) están solo en inglés. Por ejemplo, los títulos de la vista Horizon Europe son "1. Data Summary", "2. FAIR data", etc. En cambio, la exportación de respuestas (Proyecto → Respuestas → Exportar) sale en español.

Problemas conocidos
-------------------

- La exportación a **PDF de la vista "Horizon Europe"** falla porque su plantilla incluye imágenes SVG remotas que LaTeX no puede procesar. Hay que quitar las etiquetas `<img>` de la plantilla (Gestión → Vistas). Las demás vistas y la exportación de respuestas sí generan PDF.
- Las rutas de documentación de la API (OpenAPI) no están activadas. Para usarlas, instalar `rdmo[openapi]` y agregar `drf_spectacular` como en `testing/config/`.

Próximos pasos
--------------

1. Completar la traducción del catálogo elegido (RDMO o Horizon Europe) y traducir su vista. Para eso, exportar el XML, agregar los textos `lang="es"` que falten, guardarlo en `catalogos/` y reimportarlo.
2. Adaptar los textos de inicio y "acerca de" y la identidad visual de la UNC: `python manage.py make_theme --name tema_unc`.
3. Servidor: PostgreSQL (`pip install -e ".[postgres,gunicorn]"`), `DEBUG = False`, `SECRET_KEY` y `ALLOWED_HOSTS` propios, `python manage.py deploy` (collectstatic), gunicorn + nginx con HTTPS, envío real de correo, copias de respaldo y, si hace falta, autenticación institucional (LDAP, OIDC o Shibboleth).
