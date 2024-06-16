#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LitDeal.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Get the port from the environment variable or default to 8000
    port = os.environ.get('PORT', '8000')

    # Modify the command line arguments to include the port
    # Check if 'runserver' is already in the arguments
    if 'runserver' in sys.argv:
        # Find the index of 'runserver' and insert the address:port argument after it
        runserver_index = sys.argv.index('runserver')
        sys.argv.insert(runserver_index + 1, port)
    else:
        # If 'runserver' is not in the arguments, append it along with the address:port argument
        sys.argv += ['runserver', port]
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
