import threading
import asyncpg

from bot import settings


class Connection():
    def __init__(self):
        self.connection = None
    
    async def __aenter__(self):
        self.connection = await asyncpg.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            database=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD
        )
        return self.connection

    async def __aexit__(self, *_):
        await self.connection.close()

    
class ConnectionCache:
    thread_to_connection = {}

    @classmethod
    def get_connection(cls):
        thread_id = threading.get_ident()
        if thread_id in cls.thread_to_connection:
            return cls.thread_to_connection[thread_id]
        else:
            raise Exception("Trying to obtain connection")
    
    @classmethod
    def set_connection(cls, connection):
        thread_id = threading.get_ident()
        cls.thread_to_connection[thread_id] = connection
    
    @classmethod
    def clear_connection(cls):
        thread_id = threading.get_ident()
        del cls.thread_to_connection[thread_id]
    

def wrap_with_db_connection(func):

    async def inner(*args, **kwargs):
        async with Connection() as connection:
            ConnectionCache.set_connection(connection)

            async with connection.transaction():
                await func(*args, **kwargs)
            
            ConnectionCache.clear_connection()
    
    return inner