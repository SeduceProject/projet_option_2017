from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from models import Sensor, Position, Assignment, History
 
engine = create_engine('sqlite:///database.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()
 
# Insert 5 Sensor in the sensors table
sensor1 = Sensor(name='Test1', mac='00:00:00:00:01', type='thermometre', model='modele qui fonctionne bien avec un seche cheveux', etat=2)
session.add(sensor1)
sensor2 = Sensor(name='Test2', mac='00:00:00:00:02', type='thermometre', model='modele qui fonctionne juste bien', etat=1)
session.add(sensor2)
sensor3 = Sensor(name='Test3', mac='00:00:00:00:03', type='thermometre', etat=3)
session.add(sensor3)
sensor4 = Sensor(name='Test4', mac='00:00:00:00:04', type='voltmetre', model='modele qui mesure le courant je suppose', etat=1)
session.add(sensor4)
sensor5 = Sensor(mac='00:00:00:00:05', type='voltmetre', etat=2)
session.add(sensor4)
session.commit()
 
# Insert 4 Position in the positions table 
pos1 = Position(room='B135', bus=2, index=0)
session.add(pos1)
pos2 = Position(room='B135', bus=2, index=1)
session.add(pos2)
pos3 = Position(room='B135', bus=2, index=2)
session.add(pos3)
pos4 = Position(room='B135', bus=2, index=6)
session.add(pos4)
session.commit()

