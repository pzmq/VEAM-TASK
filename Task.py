import os
import sys
import hashlib
import shutil
import time
from datetime import datetime

class FolderSync:
    """
    Class for one-way synchronization of content between two folders.

    Attributes:
        source (str): Path to the source folder.
        destination (str): Path to the destination folder.
        interval (int): Interval in seconds between synchronizations.
        log_file (str): Path to the log file.
        running (bool): Flag to control the execution of the synchronization process.
    """

    def __init__(self, source, destination, interval, log_file):
        """
        Initializes an instance of the FolderSync class.

        Args:
            source (str): Path to the source folder.
            destination (str): Path to the destination folder.
            interval (int): Interval in seconds between synchronizations.
            log_file (str): Path to the log file.
        """
        
        self.source = source
        self.destination = destination
        self.interval = int(interval)
        self.log_file = log_file
        self.running = True  # Flag to control the loop execution

    def file_hash(self, filepath):
        """
        Calculates the SHA-256 hash of a file.

        Args:
            filepath (str): Path to the file.

        Returns:
            str: SHA-256 hash of the file in hexadecimal format.
        
        Notes:
            This computes the SHA-256 hash of a file by reading it in 8 KB chunks (8192 bytes). 
            Each chunk is processed incrementally with hash_func.update(chunk), optimizing memory usage and ensuring accurate hash computation for files of any size.
            (Needed for large files)
        """
        
        hash_func = hashlib.sha256()
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                hash_func.update(chunk)
        return hash_func.hexdigest()

    def generate_hash_list(self, directory):
        """
        Generates a dictionary of file hashes in a directory.

        Args:
            directory (str): Path to the directory.

        Returns:
            dict: Dictionary with relative file path as key and SHA-256 hash as value.
        """
        
        hash_list = {}
        for root, _, files in os.walk(directory):
            for file in files:
                filepath = os.path.join(root, file)
                relative_path = os.path.relpath(filepath, directory)
                hash_list[relative_path] = self.file_hash(filepath)
        return hash_list

    def sync_folders(self):
        """
        Synchronizes the destination folder with the source folder.

        Compares file hashes in the source folder with those in the destination folder
        and copies and/or removes files as necessary.
        """
        
        source_hashes = self.generate_hash_list(self.source)
        destination_hashes = self.generate_hash_list(self.destination)

        # Copy files from source to destination if they don't exist or their hashes differ.
        for relative_path, filehash in source_hashes.items():
            source_item = os.path.join(self.source, relative_path)
            destination_item = os.path.join(self.destination, relative_path)

            if relative_path not in destination_hashes or destination_hashes[relative_path] != filehash:
                os.makedirs(os.path.dirname(destination_item), exist_ok=True)
                shutil.copy2(source_item, destination_item)
                self.log_message(f"Copied {source_item} to {destination_item} - Hash: {filehash}")

        # Remove files from destination if they don't exist in source.
        for relative_path in destination_hashes:
            if relative_path not in source_hashes:
                destination_item = os.path.join(self.destination, relative_path)
                os.remove(destination_item)
                self.log_message(f"Removed {destination_item} - Hash: {destination_hashes[relative_path]}")

    def log_message(self, message):
        """
        Logs a message to the log file and prints it to the console.

        Args:
            message (str): Message to log.
        """
        
        timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        log_entry = f"{timestamp} - SyncTask - {message}"
        print(log_entry)
        with open(self.log_file, 'a') as log_file:
            log_file.write(log_entry + "\n")

    def start_sync(self):
        """
        Starts the synchronization process in a continuous loop.

        The process is stopped when the self.running flag is set to False.
        """
        
        try:
            while self.running:
                self.sync_folders()
                self.log_message(f"Synchronization completed from {self.source} to {self.destination}")
                time.sleep(self.interval)
        except KeyboardInterrupt:
            self.running = False
            self.log_message("Synchronization interrupted by user.")
            print("\nSynchronization interrupted by user. Exiting...")

def validate_arguments(args):
    """
    Validates command-line arguments provided.

    Args:
        args (list): List of command-line arguments.

    Returns:
        bool or str: Path to the log file if arguments are valid, False otherwise.
    """
    
    if len(args) < 3 or len(args) > 4:
        return False
    source = args[0]
    destination = args[1]
    interval = args[2]
    log_file = args[3] if len(args) == 4 else os.path.join(os.getcwd(), "default.log")
    if not os.path.isdir(source):
        print(f"Error: {source} is not a valid directory.")
        return False
    if not os.path.isdir(destination):
        print(f"Error: {destination} is not a valid directory.")
        return False
    try:
        interval = int(interval)
    except ValueError:
        print(f"Error: Interval {interval} is not a valid integer.")
        return False
    return log_file

if __name__ == "__main__":
    if not validate_arguments(sys.argv[1:]):
        print("Usage: ./Task.py /path/to/source /path/to/destination 60 [/path/to/logfile.log]")
        sys.exit(1)
    
    source = sys.argv[1]
    destination = sys.argv[2]
    interval = sys.argv[3]
    log_file = sys.argv[4] if len(sys.argv) == 5 else os.path.join(os.getcwd(), "default.log")

    folder_sync = FolderSync(source, destination, interval, log_file)
    
    try:
        folder_sync.start_sync()
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting...")
        sys.exit(0)
