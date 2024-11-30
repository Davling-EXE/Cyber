from database import Database
import pickle
import logging
import win32file

# Set up logger for this class with appropriate logging level
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set default logging level to DEBUG


class FileDatabase(Database):
    def __init__(self, name: str):
        """
        Initializes the FileDatabase object. If the database file does not
        exist, it creates a new file with the serialized state of the database.

        Parameters:
            name (str): The name of the database file (without extension).
        """
        super().__init__(name)
        self.name = name  # Store database name for easy reference

        # Check if the file exists
        exists = True
        try:
            file_handle = win32file.CreateFile(
                self.name + '.pkl',
                win32file.GENERIC_READ, 0, None,
                win32file.OPEN_EXISTING, win32file.FILE_ATTRIBUTE_NORMAL, None
            )
            win32file.CloseHandle(file_handle)
        except Exception as e:
            logger.error(f"Error checking file existence: {e}")
            exists = False

        # If the file doesn't exist, create it and initialize with an empty database
        if not exists:
            try:
                file_handle = win32file.CreateFile(
                    self.name + '.pkl',
                    win32file.GENERIC_WRITE, 0, None,
                    win32file.CREATE_ALWAYS, win32file.FILE_ATTRIBUTE_NORMAL, None
                )
                win32file.WriteFile(file_handle, pickle.dumps(self.db))  # Serialize the empty database
                win32file.CloseHandle(file_handle)
                logger.info(f"Created new database file: {self.name}.pkl")
            except Exception as e:
                logger.error(f"Error creating file: {e}")

    def set_value(self, key: str, val: object) -> bool:
        """
        Sets a value in the database, serializes the database, and updates the file.

        Parameters:
            key (str): The key to be set in the database.
            val (object): The value to be stored in the database.

        Returns:
            bool: True if the operation succeeded, False otherwise.
        """
        try:
            # Read the current database from file
            file_handle = win32file.CreateFile(
                self.name + '.pkl',
                win32file.GENERIC_READ, 0, None,
                win32file.OPEN_EXISTING, win32file.FILE_ATTRIBUTE_NORMAL, None
            )
            __, byte_db = win32file.ReadFile(file_handle, win32file.GetFileSize(file_handle))
            self.db = pickle.loads(byte_db)
            win32file.CloseHandle(file_handle)

            # Call parent method to update the in-memory database
            res = super().set_value(key, val)

            # Serialize the updated database and save it back to the file
            file_handle = win32file.CreateFile(
                self.name + '.pkl',
                win32file.GENERIC_WRITE, 0, None,
                win32file.OPEN_EXISTING, win32file.FILE_ATTRIBUTE_NORMAL, None
            )
            win32file.WriteFile(file_handle, pickle.dumps(self.db))
            win32file.CloseHandle(file_handle)

            # Log the successful operation
            logger.info(f"Set value: {key} = {val}")
            return res

        except Exception as e:
            logger.error(f"Error setting value {key}: {e}")
            return False

    def get_value(self, key: str):
        """
        Gets a value from the database by reading the file and returning the value.

        Parameters:
            key (str): The key for which the value is to be retrieved.

        Returns:
            The value associated with the provided key.
        """
        try:
            # Read the current database from file
            file_handle = win32file.CreateFile(
                self.name + '.pkl',
                win32file.GENERIC_READ, 0, None,
                win32file.OPEN_EXISTING, win32file.FILE_ATTRIBUTE_NORMAL, None
            )
            __, byte_db = win32file.ReadFile(file_handle, win32file.GetFileSize(file_handle))
            self.db = pickle.loads(byte_db)
            win32file.CloseHandle(file_handle)

            # Retrieve the value from the in-memory database
            res = super().get_value(key)
            logger.info(f"Retrieved value for key: {key}")
            return res

        except Exception as e:
            logger.error(f"Error getting value for {key}: {e}")
            return None

    def delete_value(self, key: str):
        """
        Deletes a value from the database, serializes the updated database, and writes it to the file.

        Parameters:
            key (str): The key to be deleted from the database.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        try:
            # Read the current database from file
            file_handle = win32file.CreateFile(
                self.name + '.pkl',
                win32file.GENERIC_READ | win32file.GENERIC_WRITE, 0, None,
                win32file.OPEN_EXISTING, win32file.FILE_ATTRIBUTE_NORMAL, None
            )
            __, byte_db = win32file.ReadFile(file_handle, win32file.GetFileSize(file_handle))
            self.db = pickle.loads(byte_db)

            # Call parent method to delete the value from the in-memory database
            res = super().delete_value(key)

            # Serialize the updated database and save it back to the file
            win32file.WriteFile(file_handle, pickle.dumps(self.db))
            win32file.CloseHandle(file_handle)

            # Log the successful operation
            logger.info(f"Deleted value for key: {key}")
            return res

        except Exception as e:
            logger.error(f"Error deleting value for {key}: {e}")
            return False
