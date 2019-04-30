
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
Set name = 'TestEvent',
dates = '2019-11-09',
location_id = (
Select l.id 
	from Locations l 
	where l.id = 'Thwing'
	);

insert into lead_by (event_id, organization_id)
select e.id, o.id 
from Organizations o, Events e
where e.name = 'TestEvent' and o.name = 'Taiwanese American Student Association';

insert into catered_by (event_id, caterer_id)
select e.id, c.id 
from Caterers c, Events e
where e.name = 'TestEvent' and c.name = 'Chipotle'


Delete c from Events e, catered_by c
where e.name = 'TestEvent' and e.id = c.event_id;
Delete l from Events e, lead_by l
where e.name = 'TestEvent' and e.id = l.event_id;
delete e from Events e where e.name = 'TestEvent';


SELECT e.name, e.dates, l2.name, c2.name,o.name,e.price from Events e
JOIN catered_by c on e.id = c.event_id
JOIN lead_by l on e.id = l.event_id
JOIN Locations l2 on l2.id = e.location_id
JOIN Caterers c2 on c2.id = c.caterer_id
JOIN Organizations o on o.id = l.organization_id;