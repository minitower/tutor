with source as (

    select * from {{ source('raw', 'raw_orders') }}

),

renamed as (

    select
        order_id,
        customer_id,
        lower(trim(category)) as category,
        amount::numeric(10, 2) as amount,
        order_ts::timestamp as order_ts,
        updated_at::timestamp as updated_at,
        {{ order_amount_bucket('amount') }} as amount_bucket

    from source
    where amount is not null

)

select * from renamed
