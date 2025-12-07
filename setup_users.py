#!/usr/bin/env python3
"""
Simple user management script for livepaste.
Usage: python setup_users.py
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.auth import UserStore

USERS_FILE = os.path.join(os.path.dirname(__file__), "backend", "users.json")


def main():
    user_store = UserStore(USERS_FILE)

    print("=== livepaste User Management ===\n")
    print("Current users:", list(user_store.users.keys()) if user_store.users else "None")
    print()

    while True:
        print("\nOptions:")
        print("1. Add user")
        print("2. List users")
        print("3. Exit")
        choice = input("\nChoose option (1-3): ").strip()

        if choice == "1":
            username = input("Enter username: ").strip()
            if not username:
                print("Username cannot be empty")
                continue
            if user_store.user_exists(username):
                print(f"User '{username}' already exists")
                continue
            password = input("Enter password: ").strip()
            if not password:
                print("Password cannot be empty")
                continue
            if user_store.add_user(username, password):
                print(f"User '{username}' added successfully!")
            else:
                print("Failed to add user")

        elif choice == "2":
            users = list(user_store.users.keys())
            if users:
                print("Registered users:")
                for u in users:
                    print(f"  - {u}")
            else:
                print("No users registered")

        elif choice == "3":
            print("Exiting...")
            break

        else:
            print("Invalid option")


if __name__ == "__main__":
    main()
