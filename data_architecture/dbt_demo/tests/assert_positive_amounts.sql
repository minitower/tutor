-- Singular-тест: должен вернуть 0 строк, иначе dbt test считает его проваленным.
-- Аналог validate_orders_batch(...) из лекции про Airflow, только в одну декларативную SQL-строку.
select order_id, amount
from {{ ref('fct_orders') }}
where amount <= 0
