CREATE TABLE capteurs (
id INTEGER PRIMARY KEY AUTOINCREMENT,
nom VARCHAR(100),
mac VARCHAR(100) NOT NULL,
type_capteur VARCHAR(100),
modele VARCHAR(100),
etat INTEGER NOT NULL
);

CREATE TABLE positions (
id INTEGER PRIMARY KEY AUTOINCREMENT,
salle VARCHAR(100) NOT NULL,
bus INTEGER NOT NULL,
index_position INTEGER NOT NULL
);

CREATE TABLE affectations (
id INTEGER PRIMARY KEY AUTOINCREMENT,
id_position INTEGER UNIQUE NOT NULL,
id_capteur INTEGER UNIQUE NOT NULL,
FOREIGN KEY (id_position) REFERENCES positions(id) ON
DELETE CASCADE,
FOREIGN KEY (id_capteur) REFERENCES capteurs(id) ON DELETE
CASCADE
);

CREATE TABLE historique (
id INTEGER PRIMARY KEY AUTOINCREMENT,
id_position INTEGER NOT NULL,
id_capteur INTEGER NOT NULL,
mise_en_service TIMESTAMP NOT NULL,
fin_de_service TIMESTAMP,
FOREIGN KEY (id_position) REFERENCES positions(id) ON DELETE SET NULL,
FOREIGN KEY (id_capteur) REFERENCES capteurs(id) ON DELETE SET NULL
);

CREATE TABLE event (
id INTEGER PRIMARY KEY AUTOINCREMENT,
titre VARCHAR(100) NOT NULL,
gravite INTEGER NOT NULL,
debut TIMESTAMP NOT NULL
fin TIMESTAMP NOT NULL
sensor INTEGER NOT NULL
);

INSERT INTO capteurs (nom, mac, type_capteur, modele, etat) VALUES ("Test1", "00:00:00:00:01", "thermometre", "modele qui fonctionne bien avec un seche cheveux", 2);
INSERT INTO capteurs (nom, mac, type_capteur, modele, etat) VALUES ("Test2", "00:00:00:00:02", "thermometre", "modele qui fonctionne juste bien", 1);
INSERT INTO capteurs (nom, mac, type_capteur, etat) VALUES ("Test3", "00:00:00:00:03", "thermometre", 3);
INSERT INTO capteurs (nom, mac, type_capteur, modele, etat) VALUES ("Test4", "00:00:00:00:04", "voltmetre", "modele qui mesure le courant je suppose", 1);
INSERT INTO capteurs (mac, type_capteur, etat) VALUES ("00:00:00:00:05", "voltmetre", 2);

INSERT INTO positions (salle, bus, index_position) VALUES ("B135", 2, 0);
INSERT INTO positions (salle, bus, index_position) VALUES ("B135", 2, 1);
INSERT INTO positions (salle, bus, index_position) VALUES ("B135", 2, 2);
INSERT INTO positions (salle, bus, index_position) VALUES ("B135", 2, 6);

INSERT INTO affectations (id_position, id_capteur) VALUES (3, 2);
INSERT INTO affectations (id_position, id_capteur) VALUES (1, 4);

INSERT INTO historique (id_position, id_capteur, mise_en_service) VALUES (1, 4, "2017-11-01T12:00:22");
INSERT INTO historique (id_position, id_capteur, mise_en_service, fin_de_service) VALUES (2, 2, "2017-11-01T12:00:22", "2017-11-13T16:43:54");
INSERT INTO historique (id_position, id_capteur, mise_en_service) VALUES (3, 2, "2017-11-13T16:43:54");
