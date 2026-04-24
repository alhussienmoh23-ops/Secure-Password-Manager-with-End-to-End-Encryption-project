#  Secure Password Manager with End-to-End Encryption
---
##  Problem Statement
Users reuse weak passwords across 100+ sites, making them vulnerable to data breaches.  
This project solves that by providing a **local, encrypted password vault** with zero cloud dependency.

---

## Solution Overview
A desktop password manager that securely stores credentials using **AES-256-GCM encryption**, protected by a master password.  
All data stays local and never syncs to external servers.

---

 ####____Features _____####

#  Security
- AES-256-GCM encryption for all stored passwords
- Master password protected vault
- PBKDF2 key derivation for secure encryption keys
- Zero-knowledge architecture (no server storage)

#  Password Management
- Secure password generation (configurable complexity)
- Password strength analysis
- Weak password alerts

# Breach Protection
- Offline breach detection using HaveIBeenPwned database
- Alerts for compromised passwords

# Organization
- Categorized password storage
- Secure clipboard auto-clear

---

## Tech Stack
- Python
- PyQt5 (GUI)
- PyCryptodome (Encryption)
- PBKDF2 (Key Derivation)
- SQLite (Local Storage)

---

## Project Structure
-backend
-encryption
-database
-ui
-main.py
---

---

## Future Improvements
- Biometric login support
- Browser extension integration
- Cloud optional encrypted backup (user-controlled)
- Multi-device sync (end-to-end encrypted)

---
