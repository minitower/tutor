{% macro order_amount_bucket(amount_column) %}
    case
        when {{ amount_column }} < 50 then 'low'
        when {{ amount_column }} < 200 then 'medium'
        else 'high'
    end
{% endmacro %}
