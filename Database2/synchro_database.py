import logging
from file_database import FileDatabase
import win32event

# Configure logging
logging.basicConfig(filename='synchro_database.log', level=logging.DEBUG)

# Constants
MAX_READERS = 10


class SynchroDatabase(FileDatabase):
    def __init__(self, name):
        super().__init__(name)
        self.write_lock = win32event.CreateMutex(None, False, None)
        self.reader_lock = win32event.CreateSemaphore(None, MAX_READERS, MAX_READERS, None)

    def acquire_write_lock(self):
        """Acquires the write lock and blocks all readers."""
        logging.debug("Acquiring write lock")
        # Wait indefinitely for the write lock
        win32event.WaitForSingleObject(self.write_lock, -1)
        # Block all readers while the write lock is held
        for i in range(MAX_READERS):
            win32event.WaitForSingleObject(self.reader_lock, -1)
        logging.debug("Acquired all reader slots, write lock is now held")

    def release_write_lock(self):
        """Releases the write lock and allows readers to acquire their slots."""
        # Release the read semaphores to allow readers
        for i in range(MAX_READERS):
            win32event.ReleaseSemaphore(self.reader_lock, 1)

        win32event.ReleaseMutex(self.write_lock)  # Release the write lock
        logging.debug("Released write lock, readers can now acquire their locks")

    def acquire_read_lock(self):
        """Acquires a read lock."""
        logging.debug("Acquiring read lock")
        # Wait indefinitely for an available reader slot
        win32event.WaitForSingleObject(self.reader_lock, -1)

    def release_read_lock(self):
        """Releases a read lock."""
        win32event.ReleaseSemaphore(self.reader_lock, 1)
        logging.debug("Released read lock")

    def set_value(self, key: str, val):
        """Sets a value in the database, requiring a write lock."""
        logging.info(f"Setting value: {key} = {val}")
        self.acquire_write_lock()  # Acquire write lock before modification
        state = super().set_value(key, val)
        self.release_write_lock()  # Release write lock after modification
        return state

    def get_value(self, key: str):
        """Gets a value from the database, requiring a read lock."""
        logging.info(f"Getting value: {key}")
        self.acquire_read_lock()  # Acquire read lock before reading
        state = super().get_value(key)
        self.release_read_lock()  # Release read lock after reading
        return state

    def delete_value(self, key: str):
        """Deletes a value from the database, requiring a write lock."""
        logging.info(f"Deleting value: {key}")
        self.acquire_write_lock()  # Acquire write lock before deletion
        state = super().delete_value(key)
        self.release_write_lock()  # Release write lock after deletion
        return state


if __name__ == '__main__':
    main()
