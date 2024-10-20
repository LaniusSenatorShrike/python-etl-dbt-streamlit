WITH raw_data AS (
    SELECT      *
    FROM        ({{raw_data_layer('products')}}) AS base_table
)
SELECT  subscription_id,
        plan,
        product,
        interval,
        amount,
        status,
        {{ dbt_utils.generate_surrogate_key(['subscription_id', 'plan']) }} AS surrogate_key
FROM    raw_data
