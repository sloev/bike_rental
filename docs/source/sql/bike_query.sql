SELECT 
bike.serial_number,
type.description,
type.color

FROM bikes.bike bike

LEFT JOIN
bikes.type type
ON 
type.type_id = bike.type_id

ORDER BY bike.serial_number;