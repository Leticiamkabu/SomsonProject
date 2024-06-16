#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LitDeal.settings')

    # try:
    #     from django.core.management import execute_from_command_line
    # except ImportError as exc:
    #     raise ImportError(
    #         "Couldn't import Django. Are you sure it's installed and "
    #         "available on your PYTHONPATH environment variable? Did you "
    #         "forget to activate a virtual environment?"
    #     ) from exc

    # # Get the port from the environment variable or default to 8000
    # port = os.environ.get('PORT', '8000')

    # # Modify the command line arguments to include the address:port
    # # Check if 'runserver' is already in the arguments
    # if 'runserver' in sys.argv:
    #     # Find the index of 'runserver' and remove any existing address:port argument
    #     runserver_index = sys.argv.index('runserver')
    #     sys.argv.pop(runserver_index + 1) if len(sys.argv) > runserver_index + 1 else None
    #     sys.argv[runserver_index] = '0.0.0.0:' + port
    # else:
    #     # If 'runserver' is not in the arguments, append it along with the address:port argument
    #     sys.argv += ['runserver', '0.0.0.0:' + port]

    # execute_from_command_line(sys.argv)

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

    # Adjust the command to run the Django development server
    # Use '0.0.0.0' as the address and port as an integer
    addr = '0.0.0.0'
    execute_from_command_line(['manage.py', 'runserver', f'{addr}:{port}'])

if __name__ == '__main__':
    main()
