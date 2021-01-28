## Daily Temperature ETL Demo

Quick ETL job to extract weather data from [WeatherAPI.com](https://www.weatherapi.com/)
to PostgreSQL database.

### Prerequisites
1. Apply an API Key from [RapidAPI](https://rapidapi.com/marketplace)
2. Python: 3.7.4
3. virtualenv
4. GNU Make
5. PostgreSQL: 12

### Quickstart

#### Create a seperated virtual environment
```
sudo apt install virtualenv
virtualenv -p python3 venv
source venv/bin/activate
```

#### Clone the repository
```
git clone https://github.com/samuelTyh/ETLdemo.git /to/your/working/directory
cd /to/your/working/directory
```
#### Set up `config.cfg`
Create `config.cfg` and fill in your API Key, DB's configuration, etc.
```
[weather-api]
API_KEY=<YOUR-API-KEY>

[DB]
HOST=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_PORT=
```
#### Run jobs
```
make install     # install dependencies 
make pull        # pull the data from API
make run         # run ETL jobs
```
#### Check results in your terminal
```
make check
```

### TODO
1. Set up cron job to pull data routinely
2. try-catch error
3. Dockerize
