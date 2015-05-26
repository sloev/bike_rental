SELECT 
contract.contract_id, contract.begin_date, 
contract.end_date, contract.bike_serial, 
type.type_name, 
rental.customer_id,
report.report_text, report.report_id,
assigned.employee_id,
bill.paid, bill.pay_date, bill.amount

FROM contracts.contract contract

LEFT JOIN
contracts.rental_contract rental
ON 
rental.contract_id = contract.contract_id
LEFT JOIN
contracts.repair_contract repair
ON
repair.contract_id = contract.contract_id
LEFT JOIN
contracts.contract_types type
ON
type.type_id = contract.type_id
LEFT JOIN 
contracts.report report 
ON 
report.report_id = repair.report_id
LEFT JOIN
contracts.assigned_to assigned
ON 
assigned.contract_id = contract.contract_id
LEFT JOIN
contracts.bill bill
ON
bill.contract_id = contract.contract_id

ORDER BY contract_id;