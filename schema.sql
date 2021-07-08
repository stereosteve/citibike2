-- drop table r2;

create or replace table r2
(
    `bike_id` String,
    `rideable_type` LowCardinality(String),

    `birth_year` UInt16,
    `gender` LowCardinality(String),
    `is_member` Bool,

    `ride_id` String,
    `duration` UInt32,

    `start_lat` Float64,
    `start_lng` Float64,
    `start_id` LowCardinality(String),
    `start_name` LowCardinality(String),
    `start_ts` DateTime,

    `end_lat` Float64,
    `end_lng` Float64,
    `end_id` LowCardinality(String),
    `end_name` LowCardinality(String),
    `end_ts` DateTime

)
ENGINE = MergeTree
partition by toYYYYMM(start_ts)
order by (start_id, end_id);