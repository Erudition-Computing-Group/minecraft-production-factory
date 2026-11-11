.PHONY: test test-python test-java build demo ci clean

# Run all tests
test: test-python test-java

# Python tests
test-python:
	docker compose run --rm python-tests

# Java tests
test-java:
	docker compose run --rm java-tests

# Build plugin JAR
build:
	docker compose run --rm java-build

# Run particle demo
demo:
	docker compose run --rm python-demo

# Full CI (all checks)
ci:
	docker compose run --rm ci

# Clean up
clean:
	docker compose down --volumes --remove-orphans
	rm -rf src/java_plugins/build
	rm -rf .pytest_cache
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
