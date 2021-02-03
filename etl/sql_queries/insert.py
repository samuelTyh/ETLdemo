class InsertDWH:
    staging_table = (
        """
        INSERT INTO realtime_weather_staging (
          location, region, country, lat, lon, timezone, local_timestamp, local_datetime, updated_timestamp, 
          updated_datetime, temp_c, temp_f, is_day, condition_text, condition_icon, condition_code, wind_mph, 
          wind_kph, wind_degree, wind_dir, pressure_mb, pressure_in, precip_mm, precip_in, humidity, cloud, 
          feelslike_c, feelslike_f, vis_km, vis_miles, uv, gust_mph, gust_kph
        ) 
        VALUES (
          %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
          %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
          %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
          %s, %s, %s
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


class DailyTemperature:
    select_daily_temperature = (
        """
        INSERT INTO daily_temperature (date, location, temperature_celsius, temperature_fahrenheit)
        WITH temp AS (
          SELECT Date(c.retrieve_time_id) dt, l.location, c.temp_c, c.temp_f
          FROM current_weather c
          JOIN location l ON c.location_id = l.location_id
        )
        SELECT dt, location, round(avg(temp_c), 1), round(avg(temp_f), 1)
        FROM temp
        GROUP BY (dt, location)
        ORDER BY (dt, location)
        ON CONFLICT (date, location) DO NOTHING;
        """
    )
