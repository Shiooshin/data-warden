WEB_IMAGE_NAME=data-warden-web
PULLER_IMAGE_NAME=periodic-puller
DIST_DIR=dist

build-web:
	@echo '<<<Building Data Warden Web Docker image..>>>'
	docker build -t $(WEB_IMAGE_NAME):latest data_warden/periodic_puller/.

build-puller:
	@echo '<<<Building Periodic Puller Docker image..>>>'
	mkdir $(DIST_DIR)
	cp requirements.txt $(DIST_DIR)
	cp periodic_puller/* $(DIST_DIR)
	cp -R common $(DIST_DIR)/common
	docker build -t $(PULLER_IMAGE_NAME):latest $(DIST_DIR)/.
	rm -r $(DIST_DIR)

build-images: build-web build-puller

run:
	@echo 'Runnning services. For now it will be a stub'
# docker-compose up -d

shutdown:
	@echo 'Stopping services. For now it will be a stub'
# docker-compose down