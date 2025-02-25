import os
import sys
import pytest_asyncio
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, project_root)

from backend import db_helper  
@pytest_asyncio.fixture(scope='function')
async def db():
  
    db_instance = db_helper.Database()
    await db_instance.init_pool() 
    yield db_instance 
    await db_instance.pool.clear()  