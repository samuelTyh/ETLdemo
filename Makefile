YOUR_CITY=Berlin

install:
		pip install -r requirements.txt

pull:
		bash ./scripts/pull.sh ${YOUR_CITY}

run:
		bash ./scripts/run.sh