CREATE TABLE plantes (
nom text unique,
id int primary key);
CREATE TABLE compagnons (
plante1 int,
plante2 int,
primary key (plante1, plante2),
constraint croissant check(plante1<plante2)
);
CREATE TABLE ennemis (
plante1 int,
plante2 int,
primary key (plante1, plante2),
constraint croissant check(plante1<plante2)
);
