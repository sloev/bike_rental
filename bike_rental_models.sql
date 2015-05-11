create schema details;
	create table details.address(
		address_id serial primary key,
		streetname text not null,
		streetnumber int not null,
		zip int not null,
		city text not null
	);
	
	create table details.phone(
		number int unique not null
	);
	
create schema shops;
	create table shops.shop(
		shop_id serial primary key,
		rent int not null,
		address_id int not null references details.address(address_id),
		phone_number int not null references details.phone(number) 
	);

create schema users;
	
	create table users.user(
		user_id serial primary key,
		first_name text not null,
		last_name text not null,
		username text not null,
		salt text not null,
		password text not null,
		phone_id int references details.phone(number),
		address_id int references details.address(address_id)
	);
	
	create table users.employee(
		salary integer not null,
		shop_id integer references shops.shop(shop_id)
	) inherits (users.user);

	create table users.mechanic(
		educated bool not null
	) inherits (users.employee);

	create table users.manager(
		senior bool not null
	) inherits (users.employee);

	create table users.admin(
		admin_by_admin int references users.user(user_id)
	) inherits (users.manager);

create schema bikes;	
	create table bikes.type(
		type_id serial primary key,
		description text not null,
		color text not null
	);
	create table bikes.bike(
		serial_number serial primary key,
		bike_type int references bikes.type(type_id)	
	);

	create table bikes.report(
		report_id serial primary key,
		serial_number int references bikes.bike(serial_number),
		report_text text not null
	);
	
create schema contracts;
	create table contracts.contract(
		contract_id serial primary key,
		begin_date date not null,
		end_date date not null,
		bike_serial int references bikes.bike(serial_number)
	);
	
	create table contracts.bill(
		bill_id serial primary key,
		paid bool default false,
		amount int not null,
		pay_date date not null
	);
	
	create table contracts.rental(
		bill_id int references contracts.bill(bill_id),
		manager_id int  references users.user(user_id)
	)inherits (contracts.contract);
	
	create table contracts.repair(
		mechanic_id int references users.user(user_id),
		report_id int references bikes.report(report_id)
	)inherits (contracts.contract);
	


	
insert into users.employee (first_name, last_name, username, password, salt,salary) values ('lol', 'cat','johannesgj', '1234','salt', 123);

select p.relname, c.user_id, c.first_name, c.username, c.password from users.user c, pg_class p  where user_id = 1 and  p.oid = c.tableoid;
select c.user_id, c.salary from users.employee c where  c.user_id = 1;


drop schema users cascade;
drop schema shops cascade;
drop schema details cascade;
drop schema bikes cascade;
drop schema contracts cascade;