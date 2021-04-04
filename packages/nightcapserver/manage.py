#!/usr/bin/env python
#region Imports
import os
import sys
#endregion

def main():
    """
        
        This class is used to interact with the Django Docker container

    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nightcapsite.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
