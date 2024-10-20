{% macro raw_data_layer(feed) %}
SELECT      *
FROM        {{feed}}
{% endmacro %}
