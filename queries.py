drop_staging_table = "DROP TABLE IF EXISTS realtime_weather_staging;"
drop_location_table = "DROP TABLE IF EXISTS location;"
drop_current_weather_table = "DROP TABLE IF EXISTS current_weather;"
drop_datetime_table = "DROP TABLE IF EXISTS datetime;"


create_staging_table = (
    """
    CREATE TABLE IF NOT EXISTS realtime_weather_staging (
      location varchar,
      region varchar,
      country varchar,
      lat numeric,
      lon numeric,
      timezone varchar,
      local_timestamp int,
      local_datetime varchar(16),
      updated_timestamp int,
      updated_datetime varchar(16),
      temp_c numeric,
      temp_f numeric,
      wind_mph numeric,
      wind_kph numeric,
      wind_degree int,
      wind_dir varchar(3),
      pressure_mb numeric,
      pressure_in numeric,
      precip_mm numeric,
      precip_in numeric,
      humidity int,
      cloud int,
      feelslike_c numeric,
      feelslike_f numeric,
      vis_km numeric,
      vis_miles numeric,
      uv numeric,
      gust_mph numeric,
      gust_kph numeric
    );
    """
)

create_location_table = (
    """
    CREATE TABLE IF NOT EXISTS location (
      location_id serial primary key,
      datetime_id timestamp,
      location varchar,
      region varchar,
      country varchar,
      lat numeric,
      lon numeric
    );
    """
)

create_current_weather_table = (
    """
    CREATE TABLE IF NOT EXISTS current_weather (
      record_id serial primary key,
      updated_time_id timestamp,
      retrieve_time_id timestamp,
      location_id int,
      temp_c numeric,
      feelslike_c numeric,
      temp_f numeric,
      feelslike_f numeric,
      wind_mph numeric,
      wind_kph numeric,
      wind_degree int,
      wind_dir varchar(3),
      pressure_mb numeric,
      pressure_in numeric,
      precip_mm numeric,
      precip_in numeric,
      humidity int,
      cloud int,
      vis_km numeric,
      vis_miles numeric,
      uv numeric,
      gust_mph numeric,
      gust_kph numeric
    );
    """
)

create_datetime_table = (
    """
    CREATE TABLE IF NOT EXISTS datetime (
      datetime_id timestamp primary key,
      minute smallint,
      hour smallint,
      day smallint,
      month smallint,
      year smallint
    );
    """
)

insert_staging_table = (
    """
    INSERT INTO realtime_weather_staging (
      location, region, country, lat, lon, timezone, local_timestamp, local_datetime, 
      updated_timestamp, updated_datetime, temp_c, temp_f, wind_mph, wind_kph, wind_degree, wind_dir, 
      pressure_mb, pressure_in, precip_mm, precip_in, humidity, cloud, feelslike_c, feelslike_f, 
      vis_km, vis_miles, uv, gust_mph, gust_kph
    ) 
    VALUES (
      %s, %s, %s, %s, %s, %s, %s, %s, 
      %s, %s, %s, %s, %s, %s, %s, %s, 
      %s, %s, %s, %s, %s, %s, %s, %s, 
      %s, %s, %s, %s, %s
    );
    """
)

create_table_queries = [create_staging_table, create_current_weather_table, create_location_table,
                        create_datetime_table]
drop_table_queries = [drop_staging_table, drop_current_weather_table, drop_location_table, drop_datetime_table]
