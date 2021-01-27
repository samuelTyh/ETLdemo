## Daily Temperature ETL Demo

Quick ETL job to extract weather data from [WeatherAPI.com](https://www.weatherapi.com/)
to PostgreSQL database.

### Prerequisites
1. Apply an API Key from [RapidAPI](https://rapidapi.com/marketplace)
2. Python: 3.7.4
3. virtualenv
4. GNU Make

### Quickstart

```
sudo apt install virtualenv
virtualenv -p python3 venv
source venv/bin/activate

cd /to/your/working/directory
make install     # install dependencies 
make pull        # pull the data from API
make run         # run ETL jobs
```

### TODO
1. Set up cron job to pull data routinely
