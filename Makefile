YOUR_LOCATION=Berlin

install:
	@pip install -r requirements.txt

pull:
	@bash ./scripts/pull.sh ${YOUR_LOCATION}

run:
	@bash ./scripts/run.sh

check:
	@python ./etl/check_result.py --temp
