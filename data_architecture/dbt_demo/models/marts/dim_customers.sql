-- Текущая версия каждого клиента из snapshot'а (SCD Type 2 без единой строчки Python).
select
    customer_id,
    region,
    segment,
    dbt_valid_from as valid_from,
    dbt_valid_to as valid_to
from {{ ref('customers_snapshot') }}
where dbt_valid_to is null
