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
      gust_kph numeric,
      PRIMARY KEY (location, local_timestamp)
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


class InsertData:
    staging_table = (
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
        )
        ON CONFLICT (local_timestamp, location) DO NOTHING;
        """
    )

    location_table = (
        """
        INSERT INTO location (datetime_id, location, region, country, lat, lon)
        SELECT to_timestamp(local_timestamp), location, region, country, lat, lon
        FROM realtime_weather_staging;
        """
    )

    current_weather_table = (
        """
        INSERT INTO current_weather (
          updated_time_id, retrieve_time_id, location_id, temp_c, feelslike_c, temp_f, feelslike_f,
          wind_mph, wind_kph, wind_degree, wind_dir, pressure_mb, pressure_in, precip_mm, precip_in,
          humidity, cloud, vis_km, vis_miles, uv, gust_mph, gust_kph
        )
        SELECT 
          to_timestamp(r.updated_timestamp), to_timestamp(r.local_timestamp), l.location_id, r.temp_c, r.feelslike_c, 
          r.temp_f, r.feelslike_f, r.wind_mph, r.wind_kph, r.wind_degree, r.wind_dir, r.pressure_mb, r.pressure_in, 
          r.precip_mm, r.precip_in, r.humidity, r.cloud, r.vis_km, r.vis_miles, r.uv, r.gust_mph, r.gust_kph
        FROM realtime_weather_staging r
        JOIN location l ON r.location = l.location AND to_timestamp(r.local_timestamp) = l.datetime_id;
        """
    )

    datetime_table = (
        """
        INSERT INTO datetime (datetime_id, minute, hour, day, month, year)
        WITH dt AS (
          SELECT DISTINCT to_timestamp(local_timestamp) ts FROM realtime_weather_staging
          UNION ALL
          SELECT DISTINCT to_timestamp(updated_timestamp) ts FROM realtime_weather_staging
        )
        SELECT DISTINCT
            ts,
            EXTRACT (MINUTE FROM ts) AS minute,
            EXTRACT (HOUR FROM ts) AS hour,
            EXTRACT (DAY FROM ts) AS day,
            EXTRACT (MONTH FROM ts) AS month,
            EXTRACT (YEAR FROM ts) AS year
        FROM dt
        ON CONFLICT (datetime_id) DO NOTHING;
        """
    )


create_table_queries = [create_staging_table, create_current_weather_table, create_location_table,
                        create_datetime_table]
drop_table_queries = [drop_staging_table, drop_current_weather_table, drop_location_table, drop_datetime_table]
