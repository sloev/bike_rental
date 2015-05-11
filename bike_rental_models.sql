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
		rent int,
		address_id int references details.address(address_id),
		phone_number int references details.phone(number) 
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
		user_id integer primary key references users.user(user_id),
		salary integer not null,
		shop_id integer references shops.shop(shop_id)
	);

	create table users.mechanic(
		user_id integer primary key references users.user(user_id),
		educated bool not null
	);

	create table users.manager(
		user_id integer primary key references users.user(user_id),
		senior bool not null
	);

	create table users.admin(
		user_id integer primary key references users.user(user_id),
		admin_by_admin integer references users.user(user_id)
	);
	
	create table users.customer(
		user_id integer primary key references users.user(user_id),
		customer_id serial primary key
	);

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
	create table contracts.type(
		type_id serial primary key,
		name text not null
	);
	create table contracts.contract(
		contract_id serial primary key,
		begin_date date not null,
		end_date date not null,
		bike_serial int references bikes.bike(serial_number)
		type_id integer references contracts.type(type_id)
	);
	
	create table contracts.bill(
		bill_id serial primary key,
		paid bool default false,
		amount int not null,
		pay_date date not null
	);
	
	create table contracts.rental(
		contract_id integer primary key references contracts.contract(contract_id)
		bill_id int references contracts.bill(bill_id),
		manager_id int  references users.manager(user_id)
	)
	
	create table contracts.repair(
		contract_id integer primary key references contracts.contract(contract_id)
		mechanic_id int references users.user(user_id),
		report_id int references bikes.report(report_id)
	)
	
insert into users.employee (first_name, last_name, username, password, salt,salary) values ('lol', 'cat','johannesgj', '1234','salt', 123);
	
	insert into shops.shop values(1);
insert into users.user (first_name, last_name, username, password, salt) values ('lol', 'cat','johannesgj', '1234','salt');
	insert into shops.shop values(1);
		insert into users.employee values(1,1,1);
			select p.relname, c.user_id, c.first_name, c.username, c.password, b.salary from users.user c, users.employee b, pg_class p  where c.user_id = b.user_id and p.oid = b.tableoid;
			
select p.relname, c.user_id, c.first_name, c.username, c.password from users.user c, pg_class p  where user_id = 1 and  p.oid = c.tableoid;
select c.user_id, c.salary from users.employee c where  c.user_id = 1;


drop schema users cascade;
drop schema shops cascade;
drop schema details cascade;
drop schema bikes cascade;
drop schema contracts cascade;