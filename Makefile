.PHONY: docker-image docker-run

docker-image:
	docker build -t ditto .

docker-run:
	docker run -d -p 8080:80 ditto
	@echo Ditto running on port 8080.
