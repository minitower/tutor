{{
    config(
        materialized='incremental',
        unique_key='order_id',
        incremental_strategy='delete+insert',
    )
}}

-- Тот же watermark-паттерн, что мы писали вручную в лекции про Airflow (extract_incremental_orders):
-- при инкрементальном запуске берём только строки, обновлённые позже максимума, который уже лежит в таблице.
select
    order_id,
    customer_id,
    category,
    amount,
    amount_bucket,
    order_ts,
    updated_at
from {{ ref('stg_orders') }}

{% if is_incremental() %}
where updated_at > (select coalesce(max(updated_at), '1970-01-01'::timestamp) from {{ this }})
{% endif %}
