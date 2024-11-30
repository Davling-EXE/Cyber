import logging

logger = logging.getLogger(__name__)  # Get logger for this class


class Database:
    def __init__(self, name):
        self.db = {"initial": 'initial'}
        self.name = name
        logger.info(f"Created new database: {name}")

    def set_value(self, key: str, val):
        if type(key) is not str:
            logger.error(f"Invalid key type for set_value: {key} (expected string)")
            return False
        self.db[key] = val
        logger.info(f"Set value: {key} = {val}")
        return True

    def get_value(self, key: str):
        if type(key) is not str:
            logger.error(f"Invalid key type for get_value: {key} (expected string)")
            return False
        if key in self.db:
            logger.info(f"Get value: {key}")
            return self.db[key]
        logger.debug(f"Key not found: {key}")
        return None

    def delete_value(self, key: str):
        if type(key) is not str:
            logger.error(f"Invalid key type for delete_value: {key} (expected string)")
            return False
        if key in self.db:
            del self.db[key]
            logger.info(f"Deleted value: {key}")
            return True
        logger.debug(f"Key not found for deletion: {key}")
        return False
