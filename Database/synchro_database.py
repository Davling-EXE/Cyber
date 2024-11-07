import logging
from file_database import FileDatabase
import multiprocessing
import threading

# Configure logging
logging.basicConfig(filename='synchro_database.log', level=logging.DEBUG)


class SynchroDatabase(FileDatabase):
    def __init__(self, name, db_type):
        super().__init__(name)
        self.db_type = db_type

        # Initialize synchronization primitives based on db_type
        if self.db_type == "thread":
            self.read_sem = threading.Semaphore(10)  # Semaphore to limit concurrent readers
            self.write_lock = threading.Semaphore(1)  # Lock to ensure exclusive write access
            self.reader_count = 0  # Track the number of active readers
        elif self.db_type == "process":
            self.read_sem = multiprocessing.Semaphore(10)  # Semaphore for process-based synchronization
            self.write_lock = multiprocessing.Semaphore(1)  # Lock for process-based synchronization
            self.reader_count = 0

        logging.info(f"Initializing {db_type} SynchroDatabase")

    def acquire_write_lock(self):
        logging.debug("Acquiring write lock")
        self.write_lock.acquire()  # Acquire the write lock

        # Block all readers while the write lock is held
        for i in range(10):
            self.read_sem.acquire()

    def release_write_lock(self):
        # Release the read semaphores to allow readers
        for i in range(10):
            self.read_sem.release()

        self.write_lock.release()  # Release the write lock
        logging.debug("Releasing write lock")

    def acquire_read_lock(self):
        logging.debug("Acquiring read lock")
        self.read_sem.acquire()  # Acquire a read semaphore
        self.reader_count += 1  # Increment the reader count

    def release_read_lock(self):
        self.reader_count -= 1  # Decrement the reader count
        self.read_sem.release()  # Release the read semaphore
        logging.debug("Releasing read lock")

    def set_value(self, key: str, val):
        logging.info(f"Setting value: {key} = {val}")
        self.acquire_write_lock()  # Acquire write lock before modification
        state = super().set_value(key, val)
        self.release_write_lock()  # Release write lock after modification
        return state

    def get_value(self, key: str):
        logging.info(f"Getting value: {key}")
        self.acquire_read_lock()  # Acquire read lock before reading
        state = super().get_value(key)
        self.release_read_lock()  # Release read lock after reading
        return state

    def delete_value(self, key: str):
        logging.info(f"Deleting value: {key}")
        self.acquire_write_lock()  # Acquire write lock before deletion
        state = super().delete_value(key)
        self.release_write_lock()  # Release write lock after deletion
        return state


def test_reader_blocked_by_writer(db):
    """
    Tests that a reader cannot acquire the read lock while a writer holds it.
    """
    logging.info("Test: Reader blocked by writer")

    # Writer thread acquires the write lock
    writer_thread = threading.Thread(target=lambda: db.set_value("test_key", "value"))
    writer_thread.start()

    # Reader thread attempts to acquire the read lock (should block)
    reader_thread = threading.Thread(target=lambda: db.get_value("test_key"))
    reader_thread.start()

    reader_thread.join(timeout=1)  # Wait for 1 second for reader to acquire lock

    # Check if reader thread is still waiting (not running)
    assert not reader_thread.is_alive(), "Reader acquired lock while writer holds it"

    writer_thread.join()  # Wait for writer to finish


def test_writer_releases_read_locks(db):
    """
    Tests that a writer releases all acquired read semaphores after acquiring the write lock.
    """
    logging.info("Test: Writer releases read locks")

    num_readers = 5

    # Start multiple reader threads
    reader_threads = []
    for _ in range(num_readers):
        thread = threading.Thread(target=lambda: db.get_value("test_key"))
        reader_threads.append(thread)
        thread.start()

    # Acquire write lock (should block until all readers release)
    writer_thread = threading.Thread(target=lambda: db.set_value("test_key", "value"))
    writer_thread.start()

    # Wait for writer to finish (indicates all readers released locks)
    writer_thread.join()

    # Join reader threads
    for thread in reader_threads:
        thread.join()


def test_concurrent_access(db):
    """
    Tests concurrent read and write operations with reader blocking during write.
    """
    logging.info("Test: Concurrent access (reader blocked by writer)")

    def reader_func():
        for _ in range(10):
            db.get_value("test_key")

    def writer_func():
        for i in range(10):
            db.set_value("test_key", str(i))

    reader_threads = [threading.Thread(target=reader_func) for _ in range(5)]
    writer_threads = [threading.Thread(target=writer_func) for _ in range(5)]

    for thread in reader_threads + writer_threads:
        thread.start()

    for thread in reader_threads + writer_threads:
        thread.join()


def main():
    db = SynchroDatabase("db", "thread")
    db.set_value("john", 26)
    print(db.get_value("john"))
    test_reader_blocked_by_writer(db)
    test_writer_releases_read_locks(db)
    test_concurrent_access(db)


if __name__ == '__main__':
    main()
