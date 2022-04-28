WEB_IMAGE_NAME=data-warden-web
PULLER_IMAGE_NAME=periodic-puller

build-web:
        @echo '<<<Building Data Warden Web Docker image..>>>'
        docker build -t $(WEB_IMAGE_NAME):latest data_warden/periodic_puller/.

build-puller:
        @echo '<<<Building Periodic Puller Docker image..>>>'
        docker build -t $(PULLER_IMAGE_NAME) data_warden/web/.

build-images: build-web build-puller

run:
        docker-compose up -d

shutdown:
        docker-compose down