#!/usr/bin/env python
"""
Build script for Vercel deployment.
This script runs during the build process to collect static files.
"""
import os
import subprocess
import sys

def main():
    """Main build function."""
    print("Starting Vercel build process...")
    
    # Set Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
    
    try:
        # Import Django and setup
        import django
        django.setup()
        
        # Run collectstatic
        print("Collecting static files...")
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        
        print("Build completed successfully!")
        
    except Exception as e:
        print(f"Build failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
