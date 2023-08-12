select complex_name, apart_rooms, apart_square, apart_floor, apart_price, apart_view, apart_plan, apart_3d, apart_id, build_tech, apart_balcon, apart_metro_dist from company.apartments
join company.complexes on complexes.complex_id = apartments.complex_id
where apart_id = $id