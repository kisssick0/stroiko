select complex_name, apart_rooms, apart_square, apart_floor, apart_price, apart_plan, apart_id from company.apartments
join company.complexes on complexes.complex_id = apartments.complex_id
where apart_rooms = '$apart_rooms' and apart_price > $price_from and apart_price < $price_to and apart_square  > $squares_from and apart_square  < $squares_to
$order_by