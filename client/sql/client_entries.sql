select managers.manager_name, managers.manager_surname, managers.manager_secondname, entries.entry_date, complexes.office_address from entries
join managers on managers.manager_id = entries.manager_id
join apartments on apartments.apart_id = entries.apart_id
join complexes on complexes.complex_id = apartments.complex_id
where client_id = $client_id
order by entry_date desc
