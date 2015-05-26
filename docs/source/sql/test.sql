insert into users.types (type_name) values
	('customer'),
	('mechanic'),
	('manager'),
	('admin')
	returning * ;

insert into details.address (street_name, street_number, zip, city) values
	('slotsgade', 3, 2200, 'copenhagen'),
	('bredgade', 33, 1080,'copenhagen'),
	('omvej', 243, 2100,'copenhagen'),
	('smalgade', 88, 2300,'copenhagen'),
	('langgade', 63, 2870,'copenhagen')
	returning *;

insert into details.phone(phone_number) values
	(88776633),
	(22443355)
	returning *;

insert into shops.shop (rent, address_id, phone_number) values 
	(10000,1, 88776633)
	returning *;

/*
create admin, manager, mechanic, customer
all users have 1234 passwords
*/
insert into users.user 
	(first_name, last_name, username, salt, password, phone_id, address_id, type) values
	('johannes', 'jorgensen','admin','QZq6FcB1pjT4iAIt42VFvg==', 
	'0a1b7bcf28010c62239504354219751aa5655f894a4de8fc2576509f0bfff030', 22443355, 2, 4),
	('kunde', 'kundesen','kunde','L7O+CHb6RML9eMIcbTJpNA==', 
	'9be8e9a15baa8b2f5d5cb233f538cbd0ecb1b17ea74de0a86cb1b41686aafd25',null, 3, 1),
	('mekaniker','mekanikersen','mekaniker','LUk2WbNqKXTgjnJRXTV7Cw==',
	'bda0cc2f97700f650a5cf9451e4d3060f9aef94c56c615d6a6faf783de6817ae', null, 4, 2),
	('manager','managersen','manager','LUk2WbNqKXTgjnJRXTV7Cw==',
	'bda0cc2f97700f650a5cf9451e4d3060f9aef94c56c615d6a6faf783de6817ae', null, 5, 3)
	returning *;

insert into users.employee (salary, shop_id, user_id) values
	(12000, 1, 1),
	(5600, 1, 3),
	(7667, 1, 4)
	returning *;


insert into users.customer (user_id) values
	(2)
	returning * ;

insert into bikes.type (description, color) values
	('tall and fast', '#ff00ee'),
	('long and comfortable', '#ffddaa')
	returning *;

insert into bikes.bike(serial_number, type_id) values
	(12435542, 1),
	(5467332, 1),
	(1122134, 2),
	(987786333, 1),
	(54637281, 2)
	returning *;

insert into contracts.contract_types(type_name)
	values
	('rental'),
	('repair')
	returning * ;


insert into contracts.contract (begin_date, end_date, bike_serial, type_id) 
	values
	('1/5/2014', '1/9/2014', 12435542, 1),
	('2/10/2014', '31/12/2014', 1122134, 2)
	returning *;

insert into contracts.rental_contract(contract_id, customer_id)
	values
	(1, 2)
	returning *;

insert into contracts.report(serial_number, report_text)
	values
	(1122134, 'broken frontwheel')
	returning *;

insert into contracts.repair_contract(contract_id, report_id)
	values
	(2, 1)
	returning *;

insert into contracts.bill(contract_id, amount, pay_date)
	values
	(1, 100, '1/12/2014')
	returning *;

insert into contracts.assigned_to(contract_id, employee_id)
	values
	(1, 4),
	(2,3)
	returning *;
