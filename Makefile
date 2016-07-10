.PHONY: clean data

data:
	python3 ./src/clonedata.py http://localhost ./data/

clean:
	rm -r data
