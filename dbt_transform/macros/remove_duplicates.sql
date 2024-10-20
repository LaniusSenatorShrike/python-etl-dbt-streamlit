{% macro remove_duplicates(model, primary_key) %}
  WITH base AS (
      SELECT
          *,
          row_number() over (PARTITION BY {{ primary_key }}) AS rn
      FROM {{ ref(model) }}
  )
  SELECT *
  FROM base
  WHERE rn = 1
{% endmacro %}