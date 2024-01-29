from collect_data.lib import arguments, central, logconfig, utilities
from collect_data.lib.logconfig import logger 
try:
    from icecream import ic
    print('icecream imported')
except ImportError:  # Graceful fallback if IceCream isn't installed.
    ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)  # noqa
