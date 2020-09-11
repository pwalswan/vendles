CREATE TABLE event (
id UUID default uuid_generate_v4(),
event_type character varying (50) not null,
customer_id int,
event_version character varying (20),
currency character varying (3) not null,
financial_status character varying (12),
total_discounts int,
total_tax decimal,
discount_codes character varying (20),
buyer_accepts_marketing character varying (5),
event_date DATE,
PRIMARY KEY (id)
);

select * from event;

// drop table event;

CREATE TABLE line_items (
id UUID default uuid_generate_v4(),
event_id UUID,
quantity int,
product_id bigint not null,
PRIMARY KEY (id)
);

select * from line_items;

// drop table line_items;

CREATE TABLE customer (
lovevery_user_id int,
email character varying (100) not null,
first_name character varying (100) not null,
last_name character varying (100) not null,
PRIMARY KEY (lovevery_user_id)
);

select * from customer;

// drop table customer;

CREATE TABLE address (
id UUID default uuid_generate_v4(),
customer_id int,
address1 character varying (100),
address2 character varying (100),
city character varying (100) not null,
province character varying (100),
country character varying (100),
zip character varying (20),
phone character varying (20),
address_type character varying (40),
PRIMARY KEY (id)
);

select * from address;

// drop table address;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";


select sum(total_discounts) discounts, sum(total_tax) tax, sum(quantity) quanity
from event e
join line_items i on i.event_id = e.id
where event_date between '2020-01-01' and '2020-12-31'
;

select event_date, sum(total_discounts) discounts, sum(total_tax) tax, sum(quantity) quanity
from event e
join line_items i on i.event_id = e.id
where event_date between '2020-06-22' and '2020-07-12'
group by event_date
;

select event_date, province, sum(total_discounts) discounts, sum(total_tax) tax, sum(quantity) quanity
from event e
join line_items i on i.event_id = e.id
join address a on a.customer_id = e.customer_id
where event_date between '2020-06-22' and '2020-07-12'
and a.address_type = 'billing_address'
group by event_date, province
order by province, event_date
;

select c.first_name, c.last_name, i.quantity
from event e
join line_items i on i.event_id = e.id
join customer c on c.lovevery_user_id = e.customer_id
where e.buyer_accepts_marketing = 'True'
order by quantity desc;