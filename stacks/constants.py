APP_LABEL = 'stacks'

HOME_SITE_ID = 1
ASTRO_SITE_ID = 2
CLIMBING_SITE_ID = 3

SUPPORTED_TYPES = (
    'image/*',
    'image/jpeg',
    'image/png',
    'image/gif',
    'text/*',
    'text/plain',
    'text/html',
    'text/x-markdown',
    'text/csv',
    'application/json',

    # astro
    'application/x-astro-object-json',

    # climbing
    'application/x-route-topo-json',
)