{{
    config(
        materialized='table',
        contract={'enforced': true},
    )
}}

-- Бизнес-витрина: выручка по региону и месяцу — аналог refresh_gold() из лекции про Airflow,
-- только порядок выполнения (после fct_orders и dim_customers) dbt выводит сам из ref().
select
    c.region,
    date_trunc('month', o.order_ts)::date as order_month,
    sum(o.amount)::numeric(12, 2) as revenue,
    count(*)::integer as orders_cnt
from {{ ref('fct_orders') }} o
join {{ ref('dim_customers') }} c on o.customer_id = c.customer_id
group by c.region, date_trunc('month', o.order_ts)
