
-- tabela profesori
CREATE TABLE IF NOT EXISTS profesori (
    id int AUTO_INCREMENT PRIMARY KEY,
    nume VARCHAR(255) NOT NULL,
    prenume VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    grad_didactic ENUM('asist', 'sef lucr', 'conf', 'prof'),
    tip_asociere ENUM('titular', 'asociat', 'extern') NOT NULL,
    afiliere VARCHAR(255)
);

INSERT INTO profesori (nume, prenume, email, grad_didactic, tip_asociere, afiliere) VALUES 
    ('Snape', 'Severus', 'severus.snape@hogwarts.com', 'sef lucr', 'titular', 'Hogwarts University'),
    ('Darth', 'Vader', 'darth.vader@mustafar.com', 'asist', 'asociat', 'Mustafar University'),
    ('Jon', 'Snow', 'jon.snow@winterfell.com', 'prof', 'titular', 'Winterfell University');

-- tabela studenti
CREATE TABLE IF NOT EXISTS studenti (
    id int AUTO_INCREMENT PRIMARY KEY,
    nume VARCHAR(255) NOT NULL,
    prenume VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    ciclu_studii ENUM('licenta', 'master') NOT NULL,
    an_studiu int NOT NULL,
    grupa int NOT NULL
);

INSERT INTO studenti (nume, prenume, email, ciclu_studii, an_studiu, grupa) VALUES
    ('Arya', 'Stark', 'arya.stark@tuiasi.ro', 'licenta', 1, 1109),
    ('Bojack', 'Horseman', 'bojack.horseman@tuiasi.ro', 'licenta', '4', 1409),
    ('Dexter', 'Morgan', 'dexter.morgan@tuiasi.ro', 'licenta', 4, 1409);

-- tabela discipline
CREATE TABLE IF NOT EXISTS discipline (
    cod int PRIMARY KEY,
    id_titular int NOT NULL,
    nume_disciplina VARCHAR(255) NOT NULL,
    an_studiu int NOT NULL,
    tip_disciplina ENUM('impusa', 'optionala', 'liber_aleasa') NOT NULL,
    categorie_disciplina ENUM ('domeniu', 'specialitate', 'adiacenta') NOT NULL,
    tip_examinare ENUM('examen', 'colocviu') NOT NULL,
    FOREIGN KEY (id_titular) REFERENCES profesori(id) ON DELETE CASCADE
);

INSERT INTO discipline (cod, id_titular, nume_disciplina, an_studiu, tip_disciplina, categorie_disciplina, tip_examinare) VALUES 
--    (1, 1, "Advanced Chemistry", 4, 'optionala', 'specialitate', 'examen'),
    (2, 1, "Test disciplina", 4, 'optionala', 'specialitate', 'examen'),
    (3, 1, "Advanced Chemistry", 4, 'optionala', 'specialitate', 'examen');

-- tabela join ds
CREATE TABLE IF NOT EXISTS join_ds (
    disciplinaID int,
    studentID int,
    PRIMARY KEY (disciplinaID, studentID),
    FOREIGN KEY (disciplinaID) REFERENCES discipline(cod) ON DELETE CASCADE,
    FOREIGN KEY (studentID) REFERENCES studenti(id) ON DELETE CASCADE
);

INSERT INTO join_ds (disciplinaID, studentID) VALUES
    (1, 2);