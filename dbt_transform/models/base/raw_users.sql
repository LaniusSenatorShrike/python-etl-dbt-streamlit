WITH raw_data AS (
    SELECT      *
    FROM        ({{raw_data_layer('users')}}) AS base_table
)
SELECT      customer_id,
            customer_name,
            customer_email
FROM        raw_data
