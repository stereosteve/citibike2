echo "`date`: drop + create"
cat schema.sql | clickhouse-client -mn

echo "`date`: start load"

for filename in data/parquet/*.parquet; do
  cat $filename | clickhouse-client --query="insert into r2 format Parquet"
  echo "`date`: loaded ${filename}"
done;

echo "`date`: load done"


# echo "`date`: stations"
# cat sql/stations_raw.sql | clickhouse-client -mn

# echo "`date`: routes"
# cat sql/routes_raw.sql | clickhouse-client -mn

# echo "`date`: trips_ntile"
# cat sql/trips_ntile.sql | clickhouse-client -mn

echo "`date`: done"