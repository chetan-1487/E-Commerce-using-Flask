import pytest
from app.main import createApp
from app.extension import db

@pytest.fixture
def client():
  app = createApp({
    "Testing":True,
    "SQLALCHEMY_DATABASE_URI":"",
    "WTF_CSRF_ENABLED" : False
  })
  return app.test_client()
