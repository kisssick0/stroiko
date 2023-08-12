select complex_name, apart_rooms, apart_square, apart_floor, apart_price, apart_plan, apart_id from company.apartments
join company.complexes on complexes.complex_id = apartments.complex_id