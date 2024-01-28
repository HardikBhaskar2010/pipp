import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileChangeHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return  # Ignore directory events
        elif event.event_type == 'created':
            print(f'File {event.src_path} has been created.')
            self.process_file(event.src_path)
        elif event.event_type == 'modified':
            print(f'File {event.src_path} has been modified.')
            self.process_file(event.src_path)

    def process_file(self, file_path):
        # Add your custom logic to process the file
        # For example, check if it's a downloaded file and perform actions accordingly
        if self.is_downloaded(file_path):
            print(f'Downloaded file detected: {file_path}')
            # Add further actions, e.g., move to a specific folder, check for malware, etc.

    def is_downloaded(self, file_path):
        # Add your logic to determine if the file is recently downloaded
        # You can check the file's extension, creation time, etc.
        # For simplicity, let's assume any file created in the last 10 seconds is considered downloaded
        ten_seconds_ago = time.time() - 10
        return os.path.getctime(file_path) > ten_seconds_ago

if __name__ == "__main__":
    from_dir = "path/to/your/download/folder"  # Replace with the actual path
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, from_dir, recursive=True)

    try:
        print("Monitoring for file system events...")
        observer.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
