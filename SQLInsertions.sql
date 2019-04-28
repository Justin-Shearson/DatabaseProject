
/* Insertions into locations can be done using this SQL*/
INSERT INTO Locations (name, hub)
Values ('Thwing', 'Center'),
('KSL', 'Center'),
('Leutner', 'North'),
('STJ', 'North'),
('Freshman Housing', 'North'),
('Tink', 'Center')

/*Insertions into users use this */
insert into Users (name, password, isOrganizer, locations_id)
Select 'Justin Shearson', 'bbones225', 1, l.id
from Locations l
where l.name = 'Village House 2'

/*Insertions into organizations */
insert into Organizations (name)
values ('La Alianza'),
('AAA'),
('Taiwanese American Student Association'),
('Glee Club'),
('Johnson Fan Club'),
('UDC'),
('USG'),
('Film Society'),
('Juggling Club')

/*Insertions into caterers*/
insert into Caterers(name)
Values ('Chipotle'),
('Bon Apple Tea'),
('Bon Appetit'),
('Chopstick'),
('Barrio'),
('Qdoba'),
('Starbucks'),
('Mitchells'),
('McDonalds'),
('Den')

/*	Insertions into events
	note datetime in SQL is done by YYYY-MM-DD format*/
insert into Events
Set name = 'Night Market',
dates = '2018-11-09',
locations_id = (
Select l.id 
	from Locations l 
	where l.id = 'Thwing'
	)

/* Insertions into Lead_by*/
insert into lead_by (events_id, organization_id)
select e.id, o.id 
from Organizations o, Events e
where e.name = 'Spring Fest' and o.name = 'Taiwanese American Student Association'
