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
where u.username = 'admin'
order by u.user_id asc;