latest_10_days_average_temperature = (
    """
    SELECT date, location, temperature_celsius, temperature_fahrenheit
    FROM daily_temperature
    ORDER BY date DESC
    LIMIT 10;
    """
)
