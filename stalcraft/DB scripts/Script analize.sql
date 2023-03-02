-- средняя цена продажи по месяцам
select   il.item_id 
		,il.item_name_ru 
		,TO_DATE(to_char(iph.sell_time,'YYYY/MM'), 'YYYY/MM/DD') as sell_time_dt
		,round(avg(iph.price/iph.amount)) as avg_price
from stalcraft.auctioneer.item_list il 
	join stalcraft.auctioneer.item_price_hist iph on iph.item_id = il.item_id 
where il.item_id = 'Ry9G'
group by il.item_id, il.item_name_ru, TO_DATE(to_char(iph.sell_time,'YYYY/MM'), 'YYYY/MM/DD')
order by TO_DATE(to_char(iph.sell_time,'YYYY/MM'), 'YYYY/MM/DD');

-- средняя цена покупки по дням
select   il.item_id 
		,il.item_name_ru 
		,TO_DATE(to_char(iph.sell_time,'YYYY/MM/DD'), 'YYYY/MM/DD') as sell_time_dt
		,round(avg(iph.price/iph.amount)) as avg_price
from stalcraft.auctioneer.item_list il 
	join stalcraft.auctioneer.item_price_hist iph on iph.item_id = il.item_id 
where il.item_id = 'Ry9G'
group by il.item_id, il.item_name_ru, TO_DATE(to_char(iph.sell_time,'YYYY/MM/DD'), 'YYYY/MM/DD')
order by TO_DATE(to_char(iph.sell_time,'YYYY/MM/DD'), 'YYYY/MM/DD');


-- минимальная/средння/максимальная цена за песледние 7 дней (в разрезе дня)
with tmp1 as (
select   il.item_id 
		,il.item_name_ru
		,TO_DATE(to_char(iph.sell_time,'YYYY/MM/DD'), 'YYYY/MM/DD')
		,round(min(iph.price/iph.amount)) as min_price
		,round(avg(iph.price/iph.amount)) as avg_price
		,round(max(iph.price/iph.amount)) as max_price
from stalcraft.auctioneer.item_list il 
	join stalcraft.auctioneer.item_price_hist iph on iph.item_id = il.item_id 
where 1 = 1
	  --and il.item_id = '26n1'
	  and iph.sell_time between now() - INTERVAL '7 DAY' and now()
group by il.item_id, il.item_name_ru, TO_DATE(to_char(iph.sell_time,'YYYY/MM/DD'), 'YYYY/MM/DD'))

select  tmp1.item_id 
	   ,tmp1.item_name_ru 
	   ,round(min(tmp1.min_price)) as min_price
	   ,round(avg(tmp1.avg_price)) as avg_price
	   ,round(max(tmp1.max_price)) as max_price
from tmp1
where tmp1.item_id = '26n1'
group by tmp1.item_id, tmp1.item_name_ru;



-- минимальная/средння/максимальная цена за песледние 7 дней (в разрезе одного лота)
select   il.item_id 
		,il.item_name_ru 
		,round(min(iph.price/iph.amount)) as min_price
		,round(avg(iph.price/iph.amount)) as avg_price
		,round(max(iph.price/iph.amount)) as max_price
		,round(avg(iph.price/iph.amount)*0.85) as profit_price
		,count(iph.row_id) as cnt_lot_sell
from stalcraft.auctioneer.item_list il 
	join stalcraft.auctioneer.item_price_hist iph on iph.item_id = il.item_id 
where 1 = 1
	  and il.item_id = '26n1'
	  and iph.sell_time between now() - INTERVAL '7 DAY' and now()
group by il.item_id, il.item_name_ru;




select   il.item_id 
		,il.item_name_ru 
		,to_char(iph.sell_time,'YYYY/MM') as sell_time_dt
from stalcraft.auctioneer.item_list il 
	join stalcraft.auctioneer.item_price_hist iph on iph.item_id = il.item_id 
where il.item_id = 'Ry9G';