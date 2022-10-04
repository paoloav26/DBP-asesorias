import unittest
from flask_sqlalchemy import SQLAlchemy

from server import create_app
from models import setup_db
import json

persona = {
  "id":3213213,
  "nombre":"Enrique",
  "apellidos":"Flores",
  "numero_telefonico":8521279,
  "correo":"enrique.utec"
}

class TestCaseTodoApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'maletas_test'
        self.database_path = 'postgresql+psycopg2://{}@{}/{}'.format('postgres:keypaolo', 'localhost:27015', self.database_name)

        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
    
    def test_get_personas_success(self):
        pass

    def test_get_personas_fail_404(self):
        pass

    def tearDown(self):
        pass
