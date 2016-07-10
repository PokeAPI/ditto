.PHONY: clean data

data:
	python3 ./src/clone_data.py http://localhost ./data/

serve:
	python3 ./src/serve_data.py 80 ./data/

clean:
	rm -r data
