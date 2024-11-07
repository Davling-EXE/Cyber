from database import Database
import pickle
import os
import logging

logger = logging.getLogger(__name__)  # Get logger for this class


class FileDatabase(Database):
    def __init__(self, name):
        super().__init__(name)
        self.name = name  # Store name for easy access
        if not os.path.isfile(self.name + '.pkl'):
            open(self.name + '.pkl', 'wb').close()  # Create empty file
            logger.info(f"Created new database file: {self.name}.pkl")

    def load_db(self):
        if not os.path.getsize(self.name + '.pkl') == 0:
            if not self.db:
                try:
                    with open(self.name + '.pkl', 'rb') as f:
                        self.db = pickle.load(f)  # deserialize using load()
                        logger.debug(f"Loaded database from: {self.name}.pkl")
                except (EOFError, FileNotFoundError) as e:
                    # Handle potential errors during loading
                    logger.error(f"Error loading database: {e}")
                    self.db = {}  # Initialize empty db if loading fails

    def dump_db(self):
        with open(self.name + '.pkl', 'wb') as f:  # Open in binary write mode
            pickle.dump(self.db, f)  # serialize the list
            logger.debug(f"Dumped database to: {self.name}.pkl")

    def set_value(self, key: str, val: object) -> bool:
        self.load_db()
        res = super().set_value(key, val)
        self.dump_db()
        logger.info(f"Set value: {key} = {val}")
        return res

    def get_value(self, key: str):
        self.load_db()
        res = super().get_value(key)
        logger.info(f"Get value: {key}")
        return res

    def delete_value(self, key: str):
        self.load_db()
        res = super().delete_value(key)
        self.dump_db()
        logger.info(f"Deleted value: {key}")
        return res
