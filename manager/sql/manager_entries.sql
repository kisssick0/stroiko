select clients.client_name, clients.client_surname, clients.client_second_name, entries.entry_date, complexes.office_address, entries.apart_id from entries
join clients on clients.client_id = entries.client_id
join apartments on apartments.apart_id = entries.apart_id
join complexes on complexes.complex_id = apartments.complex_id
where manager_id = $manager_id
order by entry_date desc