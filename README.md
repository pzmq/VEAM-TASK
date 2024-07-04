# Folder Synchronization Script

This Python script (`Task.py`) facilitates one-way synchronization of files from a source folder to a destination folder at regular intervals.

## Overview

The script periodically checks the source folder for changes and updates the destination folder accordingly. It logs all file operations to a specified log file for tracking purposes.

### Features

- **One-Way Synchronization:** Copies new and modified files from the source to the destination folder.
  
- **Logging:** Records file creation, copying, and removal operations in a log file (`logfile.log`).
  
- **SHA-256 Hashing:** Uses SHA-256 to verify file integrity during synchronization.

### Security and Performance Enhancements
For security and performance reasons, the script utilizes SHA-256 hashing instead of MD5 for file integrity checks. SHA-256 provides stronger security and collision resistance, making it suitable for applications where data integrity is critical.

Chunking is employed to efficiently handle large files during synchronization. By processing files in smaller, manageable chunks (e.g., 8192 bytes), the script optimizes memory usage and improves performance, ensuring smooth operation even with large datasets.

## Test Task

![PDF Page 1](Internal_Development_in_QA_(SDET)_Team_tesk_task.jpg)
