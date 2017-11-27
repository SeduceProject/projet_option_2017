from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from models import Base, Sensor, Position, Assignment, History
 
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
sensor1 = Sensor(name='Test1', mac='00:00:00:00:01', type='thermometre', model='modele qui fonctionne bien avec un seche cheveux', state=2)
session.add(sensor1)
sensor2 = Sensor(name='Test2', mac='00:00:00:00:02', type='thermometre', model='modele qui fonctionne juste bien', state=1)
session.add(sensor2)
sensor3 = Sensor(name='Test3', mac='00:00:00:00:03', type='thermometre', model=None, state=3)
session.add(sensor3)
sensor4 = Sensor(name='Test4', mac='00:00:00:00:04', type='voltmetre', model='modele qui mesure le courant je suppose', state=1)
session.add(sensor4)
sensor5 = Sensor(name=None, mac='00:00:00:00:05', type='voltmetre', model=None, state=2)
session.add(sensor5)
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

# Insert 2 Assignment in the assignments table 
assign1 = Assignment(id_position=pos3, id_sensor=sensor2)
session.add(assign1)
assign2 = Assignment(id_position=pos1, id_sensor=sensor4)
session.add(assign2)
session.commit()

# Insert 3 History in the history table 
hist1 = History(id_position=pos1, id_sensor=sensor4, start_of_service='2017-11-01 12:00:22.000000', end_of_service=None)
session.add(hist1)
hist2 = Assignment(id_position=pos2, id_sensor=sensor2, start_of_service='2017-11-01 12:00:22.000000', end_of_service='2017-11-13 16:43:54.000000')
session.add(hist2)
hist3 = History(id_position=pos3, id_sensor=sensor2, start_of_service='2017-11-13 16:43:54.000000', end_of_service=None)
session.add(hist3)
session.commit()
