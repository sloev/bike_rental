create schema details;
	create table details.address(
		address_id serial primary key,
		street_name text not null,
		street_number int not null,
		zip int not null,
		city text not null,
		unique (street_name, street_number, zip, city)
	);
	
	create table details.phone(
		phone_number int unique not null
	);
	
create schema shops;
	create table shops.shop(
		shop_id serial primary key,
		rent int not null,
		address_id int not null references details.address(address_id),
		phone_number int not null references details.phone(phone_number) 
	);

create schema users;
	create table users.types(
		type_id serial primary key,
		type_name text not null unique
	);
	create table users.user(
		user_id serial primary key,
		first_name text not null,
		last_name text not null,
		username text not null unique,
		salt text not null,
		password text not null,
		address_id int not null references details.address(address_id),
		phone_id int references details.phone(phone_number),
		creation_date date not null default CURRENT_DATE,
		type int not null references users.types(type_id)
	);

	create table users.customer(
		erhverv bool default false,
		user_id int primary key references users.user(user_id)
	);
	


	create table users.employee(
		salary integer not null,
		shop_id integer references shops.shop(shop_id),
		user_id int primary key references users.user(user_id)
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

	
create schema contracts;
	create table contracts.contract_types(
		type_id serial primary key,
		type_name text not null
	);

	create table contracts.contract(
		contract_id serial primary key,
		begin_date date not null,
		end_date date not null,
		bike_serial int references bikes.bike(serial_number),
		type_id int references contracts.contract_types(type_id)
	);

	create table contracts.rental_contract(
		contract_id int primary key references contracts.contract(contract_id),
		customer_id int references users.user(user_id)
	);
	create table contracts.report(
		report_id serial primary key,
		serial_number int references bikes.bike(serial_number),
		report_text text not null
	);

	create table contracts.repair_contract(
		contract_id int primary key references contracts.contract(contract_id),
		report_id int references contracts.report(report_id)
	);

	create table contracts.assigned_to(
		contract_id int primary key references contracts.contract(contract_id),
		employee_id int not null references users.user(user_id)
	);
	
	create table contracts.bill(
		contract_id int primary key references contracts.contract(contract_id),
		paid bool default false,
		amount int not null,
		pay_date date not null
	);




create schema functions;

create language plpythonu;

CREATE TYPE functions.login_type AS (
  username text,
  user_id integer,
  first_name text,
  last_name text,
  password text,
  salt text,
  type_name text,
  erhverv boolean,
  salary integer,
  shop_id integer,
  street_name text,
  street_number integer,
  zip integer,
  city text,
  phone_number int
);


CREATE OR REPLACE FUNCTION functions.login (username text, password text)
  RETURNS functions.login_type
AS $$

from base64 import b64encode
from hashlib import sha256

def authenticate(stored_password, stored_salt, new_password):

    _new_password = _encrypt_password(stored_salt, new_password)
    return _new_password == stored_password

def _encrypt_password(salt, password):

    if isinstance(password, str):
        password_bytes = password.encode("UTF-8")
    else:
        password_bytes = password

    hashed_password = sha256()
    hashed_password.update(password_bytes)
    hashed_password.update(salt)
    hashed_password = hashed_password.hexdigest()
    if not isinstance(hashed_password, str):
        hashed_password = hashed_password.decode("UTF-8")
    return hashed_password


query = """
select u.username, u.user_id, u.first_name, u.last_name, u.password, u.salt,
	t.type_name,
	c.erhverv,
	e.salary, e.shop_id,
	a.street_name, a.street_number, a.zip, a.city,
	p.phone_number 
from 
	users.user u
left join 
	users.customer c 
on 
	u.user_id = c.user_id
left join
	users.employee e
on 
	u.user_id = e.user_id
left join 
	details.phone p
on 
	p.phone_number = u.phone_id

left join
	details.address a
on 
	a.address_id = u.address_id
left join
	users.types t
on
	u.type = t.type_id
where u.username = \'%s\'
""" % username

rows = plpy.execute(query)

#if results have at least one row
if len(rows) > 0:
    row = rows[0]
    #if the results salt and input password is equal to results password
    if authenticate(row['password'], row['salt'], password):
    	#then return all fields from query
        return row
#else return null for all fields
return [None] * 15

$$ LANGUAGE plpythonu;

CREATE OR REPLACE FUNCTION functions.update_login (username text, password text)
  RETURNS text
AS $$
from base64 import b64encode
import os
from hashlib import sha256

def create_password_from_clear( password):
    salt = b64encode(os.urandom(16))
    _password = _encrypt_password(salt, password)
    return salt, _password

def _encrypt_password(salt, password):

    if isinstance(password, str):
        password_bytes = password.encode("UTF-8")
    else:
        password_bytes = password

    hashed_password = sha256()
    hashed_password.update(password_bytes)
    hashed_password.update(salt)
    hashed_password = hashed_password.hexdigest()
    if not isinstance(hashed_password, str):
        hashed_password = hashed_password.decode("UTF-8")
    return hashed_password

salt, new_password = create_password_from_clear(password)
query = """
UPDATE users.user SET
salt = \'%s\',  
password = \'%s\' 
WHERE username = \'%s\';
""" % (salt, new_password, username)
records = plpy.execute(query)
if records.nrows():
    return "OK"
return "ERROR"

$$ LANGUAGE plpythonu;