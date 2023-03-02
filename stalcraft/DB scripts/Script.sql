-- создаем схему приложения 
create schema auctioneer;


-- создаем таблицу для записи предметов
create table stalcraft.auctioneer.item_list (
item_id varchar(50) primary key,
item_name_ru varchar(300),
item_name_eu varchar(300),
item_class varchar(100),
item_type varchar(100),
db_last_udt timestamp default current_timestamp,
db_last_upd_by varchar(100) default 'python service');


-- создаем таблицу для хранении истории аукциона
create table stalcraft.auctioneer.item_price_hist (
row_id serial primary key, 
item_id varchar(50),
amount integer,
price integer,
sell_time timestamp,
seller varchar(200),
db_last_udt timestamp default current_timestamp,
db_last_upd_by varchar(100) default 'python service');

create index IX_row_id_date on stalcraft.auctioneer.item_price_hist (row_id, sell_time);
create index IX_row_id on stalcraft.auctioneer.item_price_hist (row_id);
create index IX_sell_time on stalcraft.auctioneer.item_price_hist (sell_time);


-- провверка заполнения 
select tt.item_id,tt.price,tt.amount, tt.price/tt.amount real_price,tt.sell_time 
from stalcraft.auctioneer.item_price_hist tt
where tt.item_id  = '26n1' 
	  and tt.sell_time between now() - INTERVAL '7 DAY' and now()
order by tt.price/tt.amount desc;

select now()

select count(*)
from stalcraft.auctioneer.item_price_hist tt
where tt.item_id  = 'VYEA';

SELECT pg_database_size('stalcraft');

SELECT * FROM pg_catalog.pg_tables

select *
from stalcraft.auctioneer.item_list t
where t.item_id  = 'nj29'
where lower(t.item_name_ru) like '%ziv%';

select t.sell_time as time_limit from stalcraft.auctioneer.item_price_hist t where t.item_id = 'nj29';

--truncate table stalcraft.auctioneer.item_list;
truncate table stalcraft.auctioneer.item_price_hist;

select  it.item_id as item_id
		,max(iph.sell_time) as max_sell_time 
from stalcraft.auctioneer.item_list it
	 left join stalcraft.auctioneer.item_price_hist iph on iph.item_id = it.item_id
group by it.item_id;