"""
Script to check if all required files exist in the project structure
"""

import os
from pathlib import Path

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BOLD = '\033[1m'

# Required files structure
REQUIRED_FILES = {
    'Root Files': [
        'manage.py',
        '.env',
        '.env.example',
        '.gitignore',
        'requirements.txt',
        'README.md',
    ],

    'Config Files': [
        'config/__init__.py',
        'config/settings.py',
        'config/urls.py',
        'config/wsgi.py',
        'config/asgi.py',
        'config/settings/__init__.py',
        'config/settings/base.py',
        'config/settings/development.py',
        'config/settings/production.py',
    ],

    'Apps - Chatbot': [
        'apps/__init__.py',
        'apps/chatbot/__init__.py',
        'apps/chatbot/apps.py',
        'apps/chatbot/models.py',
        'apps/chatbot/admin.py',
        'apps/chatbot/views.py',
        'apps/chatbot/urls.py',
        'apps/chatbot/migrations/__init__.py',
        'apps/chatbot/api/__init__.py',
        'apps/chatbot/api/serializers/__init__.py',
        'apps/chatbot/api/views/__init__.py',
        'apps/chatbot/services/__init__.py',
        'apps/chatbot/tests/__init__.py',
    ],

    'Apps - Users': [
        'apps/users/__init__.py',
        'apps/users/apps.py',
        'apps/users/models.py',
        'apps/users/admin.py',
        'apps/users/views.py',
        'apps/users/urls.py',
        'apps/users/migrations/__init__.py',
        'apps/users/tests/__init__.py',
    ],

    'Apps - Analytics': [
        'apps/analytics/__init__.py',
        'apps/analytics/apps.py',
        'apps/analytics/models.py',
        'apps/analytics/admin.py',
        'apps/analytics/views.py',
        'apps/analytics/urls.py',
        'apps/analytics/migrations/__init__.py',
        'apps/analytics/tests/__init__.py',
    ],

    'Core': [
        'core/__init__.py',
        'core/models.py',
        'core/utils/__init__.py',
        'core/middleware/__init__.py',
    ],

    'ML Models': [
        'ml_models/__init__.py',
    ],
}

# Required directories
REQUIRED_DIRS = [
    'apps',
    'config',
    'core',
    'ml_models',
    'ml_models/trained_models',
    'ml_models/training_data',
    'static',
    'static/css',
    'static/js',
    'static/images',
    'media',
    'media/uploads',
    'templates',
    'templates/base',
    'logs',
    'tests',
]


def check_files():
    """Check if all required files exist"""
    missing_files = []
    existing_files = []

    print(f"\n{BOLD}{'=' * 60}{RESET}")
    print(f"{BOLD}Checking Project Structure for ai_chatbot_advanced{RESET}")
    print(f"{BOLD}{'=' * 60}{RESET}\n")

    for category, files in REQUIRED_FILES.items():
        print(f"\n{BOLD}{YELLOW}Checking: {category}{RESET}")
        print("-" * 60)

        for file_path in files:
            if os.path.exists(file_path):
                print(f"  {GREEN}✓{RESET} {file_path}")
                existing_files.append(file_path)
            else:
                print(f"  {RED}✗{RESET} {file_path} {RED}(MISSING){RESET}")
                missing_files.append(file_path)

    return existing_files, missing_files


def check_directories():
    """Check if all required directories exist"""
    missing_dirs = []
    existing_dirs = []

    print(f"\n{BOLD}{YELLOW}Checking: Directories{RESET}")
    print("-" * 60)

    for dir_path in REQUIRED_DIRS:
        if os.path.isdir(dir_path):
            print(f"  {GREEN}✓{RESET} {dir_path}/")
            existing_dirs.append(dir_path)
        else:
            print(f"  {RED}✗{RESET} {dir_path}/ {RED}(MISSING){RESET}")
            missing_dirs.append(dir_path)

    return existing_dirs, missing_dirs


def generate_fix_commands(missing_files, missing_dirs):
    """Generate commands to create missing files and directories"""

    if not missing_files and not missing_dirs:
        return None

    commands = []

    if missing_dirs:
        dir_cmd = "mkdir -p " + " ".join(missing_dirs)
        commands.append(dir_cmd)

    if missing_files:
        file_cmd = "touch " + " ".join(missing_files)
        commands.append(file_cmd)

    return commands


def main():
    """Main function to run all checks"""

    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print(f"\n{RED}ERROR: This script must be run from the project root directory!{RESET}")
        print(f"{YELLOW}Please navigate to ai_chatbot_advanced/ folder and run again.{RESET}\n")
        return

    # Check directories
    existing_dirs, missing_dirs = check_directories()

    # Check files
    existing_files, missing_files = check_files()

    # Summary
    print(f"\n{BOLD}{'=' * 60}{RESET}")
    print(f"{BOLD}SUMMARY{RESET}")
    print(f"{BOLD}{'=' * 60}{RESET}\n")

    total_dirs = len(existing_dirs) + len(missing_dirs)
    total_files = len(existing_files) + len(missing_files)

    print(f"  Directories: {GREEN}{len(existing_dirs)}{RESET}/{total_dirs} exist")
    print(f"  Files:       {GREEN}{len(existing_files)}{RESET}/{total_files} exist")

    if missing_dirs:
        print(f"\n  {RED}Missing Directories: {len(missing_dirs)}{RESET}")
        for d in missing_dirs:
            print(f"    - {d}/")

    if missing_files:
        print(f"\n  {RED}Missing Files: {len(missing_files)}{RESET}")
        for f in missing_files:
            print(f"    - {f}")

    # Generate fix commands
    if missing_files or missing_dirs:
        print(f"\n{BOLD}{'=' * 60}{RESET}")
        print(f"{BOLD}{YELLOW}FIX COMMANDS{RESET}")
        print(f"{BOLD}{'=' * 60}{RESET}\n")
        print(f"Copy and paste these commands to create missing items:\n")

        commands = generate_fix_commands(missing_files, missing_dirs)
        for cmd in commands:
            print(f"{GREEN}{cmd}{RESET}\n")
    else:
        print(f"\n{GREEN}{BOLD}✓ ALL FILES AND DIRECTORIES EXIST!{RESET}")
        print(f"{GREEN}Your project structure is complete!{RESET}\n")

    print(f"{BOLD}{'=' * 60}{RESET}\n")


if __name__ == "__main__":
    main()
