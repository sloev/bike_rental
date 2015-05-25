create schema functions;

create language plpythonu;

drop type functions.login_type cascade;

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
select 
    u.username, u.user_id, u.first_name, u.last_name, u.password, u.salt,
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
""" % username #stringformatted username

resultset = plpy.execute(query)

#if results have at least one row
if len(resultset) > 0:
    row = resultset[0]
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

resultset = plpy.execute(query)

if resultset.nrows():
    return "OK"
else:
  return "ERROR"

$$ LANGUAGE plpythonu;




from base64 import b64encode
import os
from hashlib import sha256
import logging

def create_password_from_clear( password):
    salt = b64encode(os.urandom(16))
    _password = _encrypt_password(salt, password)
    return salt, _password

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

