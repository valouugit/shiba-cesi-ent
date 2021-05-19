BEGIN TRANSACTION;
DROP TABLE IF EXISTS "user";
CREATE TABLE IF NOT EXISTS "user" (
	"id_user"	INTEGER NOT NULL,
	"id_discord"	TEXT NOT NULL,
	"cesi_email"	TEXT NOT NULL,
	"cesi_password"	TEXT NOT NULL,
	PRIMARY KEY("id_user" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "bloc";
CREATE TABLE IF NOT EXISTS "bloc" (
	"id_bloc"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"semestre"	INTEGER NOT NULL,
	PRIMARY KEY("id_bloc" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "competence";
CREATE TABLE IF NOT EXISTS "competence" (
	"id_competence"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	PRIMARY KEY("id_competence" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "note_competence";
CREATE TABLE IF NOT EXISTS "note_competence" (
	"id_note_competence"	INTEGER NOT NULL,
	"note"	TEXT NOT NULL,
	"id_competence"	INTEGER NOT NULL,
	"id_bloc"	INTEGER NOT NULL,
	"id_user"	INTEGER NOT NULL,
	CONSTRAINT "note_competence_bloc0_FK" FOREIGN KEY("id_bloc") REFERENCES "bloc"("id_bloc"),
	CONSTRAINT "note_competence_competence_FK" FOREIGN KEY("id_competence") REFERENCES "competence"("id_competence"),
	CONSTRAINT "note_competence_user1_FK" FOREIGN KEY("id_user") REFERENCES "user"("id_user"),
	PRIMARY KEY("id_note_competence" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "note_bloc";
CREATE TABLE IF NOT EXISTS "note_bloc" (
	"id_note_bloc"	INTEGER NOT NULL,
	"note"	TEXT NOT NULL,
	"id_user"	INTEGER NOT NULL,
	"id_bloc"	INTEGER NOT NULL,
	CONSTRAINT "note_bloc_user_FK" FOREIGN KEY("id_user") REFERENCES "user"("id_user"),
	CONSTRAINT "note_bloc_bloc0_FK" FOREIGN KEY("id_bloc") REFERENCES "bloc"("id_bloc"),
	PRIMARY KEY("id_note_bloc" AUTOINCREMENT)
);
COMMIT;
