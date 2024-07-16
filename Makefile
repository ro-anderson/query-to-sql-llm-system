.PHONY: build run test clean docker-clean help

SHELL=/bin/bash

# Check if 'docker compose' is available, otherwise fall back to 'docker-compose'
ifeq ($(shell docker compose version 2>/dev/null),)
  DOCKER_COMPOSE := docker-compose
else
  DOCKER_COMPOSE := docker compose
endif

## Build the Docker images
build:
	$(DOCKER_COMPOSE) build

## Build (if needed) and run the Streamlit app in Docker
run: build
	$(DOCKER_COMPOSE) up app

## Build (if needed) and run tests with pytest in Docker
test: build
	$(DOCKER_COMPOSE) run app_test

## Remove Python cache files
clean:
	find . -name "__pycache__" -type d -exec rm -r {} \+

## Remove Docker containers, networks, and volumes
docker-clean:
	$(DOCKER_COMPOSE) down -v --remove-orphans

## Display help information
help:
	@echo "Available commands:"
	@echo "  make build         - Build the Docker images"
	@echo "  make run           - Build (if needed) and run the Streamlit app in Docker"
	@echo "  make test          - Build (if needed) and run tests with pytest in Docker"
	@echo "  make clean         - Remove Python cache files"
	@echo "  make docker-clean  - Remove Docker containers, networks, and volumes"
	@echo "  make help          - Display this help information"

# Default target
.DEFAULT_GOAL := help