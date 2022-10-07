from flask_sqlalchemy import SQLAlchemy

user = "postgres:keypaolo"
conection = "localhost:27015"
data_base_name = "maletas"
database_path = f"postgresql+psycopg2://{user}@{conection}/{data_base_name}"

db=SQLAlchemy()

def setup_db(app,database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()

# models
class Personas(db.Model):
    __tablename__ = 'personas'
    # attributes
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(),nullable=False)
    apellidos = db.Column(db.String(),nullable=False)
    numero_telefonico = db.Column(db.Integer,nullable = False)
    correo = db.Column(db.String(), nullable= False)

    meletas = db.relationship('Maletas',backref='maletas',lazy=True)


    # methods
    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
            return self.format()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return self.id
        except Exception as e:
            print(e)
            db.session.rollback()
        finally:
            db.session.close()
        

    def format(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellidos,
            'numero_telefonico':self.numero_telefonico,
            'correo': self.correo
        }

    def __repr__(self):
        return f'Persona: id={self.id}'


class Maletas(db.Model):
    __tablename__ = 'maletas'
    # attributes
    id = db.Column(db.Integer, primary_key=True)
    peso = db.Column(db.Integer,nullable=False)
    color = db.Column(db.String(),nullable=False)
    marca = db.Column(db.String(),nullable=False)

    id_dueno = db.Column(db.Integer,db.ForeignKey('personas.id'),nullable=False)

    # methods
    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.format()
        except Exception as e:
            print(e)
            db.session.rollback()
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
            return self.format()
        except Exception as e:
            print(e)
            db.session.rollback()
        finally:
            db.session.close()
        

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return self.id
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def format(self):
        return {
            'id': self.id,
            'peso':self.peso,
            'color':self.color,
            'marca':self.marca
        }

    def __repr__(self):
        return f'Persona: id={self.id}'