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

persona_maletas = {
  "id":77777777,
  "nombre":"Enrique",
  "apellidos":"Flores",
  "numero_telefonico":8521279,
  "correo":"enrique.utec"
}

maleta = {
    "peso":25,
    "color":"Rojo",
    "marca":"Nike",
    "id_dueno":"77777777"
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
        res0 = self.client().post('/personas',json=persona)

        res = self.client().get('/personas')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_personas'])
        self.assertTrue(data['personas'])
        self.assertTrue(data['personas_en_pagina'])

        res0 = self.client().delete(f'/personas/{persona["id"]}')

    def test_get_personas_fail_404(self):
        res = self.client().get('/personas?page=0')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['code'],404)
        self.assertEqual(data['message'],'resource not found')

    def test_post_personas_success(self):
        res = self.client().post('/personas',json=persona)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['persona'])
        self.assertTrue(data['total_personas'])

    def test_post_personas_fail(self):
        res = self.client().post('/personas',json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,400)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['code'],400)
        self.assertEqual(data['message'],'Bad Request')

    def test_patch_personas_success(self):
        res0 = self.client().post('/personas',json=persona)

        res = self.client().patch(f'/personas/{persona["id"]}',json={'nombre':'jose','apellidos':'casillas'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['persona'])

        res0 = self.client().delete(f'/personas/{persona["id"]}')

    def test_patch_personas_fail_404(self):
        res = self.client().patch('/personas/-1',json={'nombre':'jose','apellidos':'casillas'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['code'],404)
        self.assertEqual(data['message'],"resource not found")

    def test_delete_personas_success(self):
        res0 = self.client().post('/personas',json=persona)

        res = self.client().delete(f'/personas/{persona["id"]}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data["deleted_id"])

    def test_delete_personas_fail_404(self):
        pass

    def test_get_maletas_success(self):
        res0 = self.client().post('/personas',json=persona_maletas)
        res0 = self.client().post('/maletas',json=maleta)

        res = self.client().get('/maletas?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data["maletas"])
        self.assertTrue(data["total_maletas"])
        self.assertTrue(data["maletas_en_pagina"])

    def test_get_maletas_fail_404(self):
        res = self.client().get('/maletas?page=1000000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['code'],404)
        self.assertEqual(data['message'],"resource not found")

    def test_post_maletas_success(self):
        res = self.client().post('/maletas',json=maleta)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data["dueño"])
        self.assertTrue(data["maleta"])

    def test_post_maletas_fail(self):
        res = self.client().post('/maletas',json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['code'],404)
        self.assertEqual(data['message'],"resource not found")

    def test_patch_maletas_success(self):
        res0 = self.client().post('/maletas',json=maleta)
        id = json.loads(res0.data)["maleta"]["id"]

        res = self.client().patch(f'/maletas/{id}',json={"peso":"30","color":"blanco","marca":"off white"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data["maleta"])

    def test_patch_maletas_fail_404(self):
        res = self.client().patch('/maletas/50000',json={"peso":"30","color":"blanco","marca":"off white"})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['code'],404)
        self.assertEqual(data['message'],"resource not found")

    def test_delete_maletas_success(self):
        res0 = self.client().post('/maletas',json=maleta)
        id = json.loads(res0.data)["maleta"]["id"]

        res = self.client().delete(f'/maletas/{id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data["deleted_maleta_id"])

    def test_delete_maletas_fail_404(self):
        res = self.client().delete('/maletas/-1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['code'],404)
        self.assertEqual(data['message'],"resource not found")

    def tearDown(self):
        pass
