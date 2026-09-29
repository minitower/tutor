with source as (

    select * from {{ source('raw', 'raw_customers') }}

),

renamed as (

    select
        customer_id,
        region,
        segment,
        updated_at::timestamp as updated_at

    from source

)

select * from renamed
