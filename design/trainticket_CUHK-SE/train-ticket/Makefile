NS ?= "ts22"
PORT ?= "30080"

.PHONY: deploy

deploy:
	@if helm status $(NS) -n $(NS) >/dev/null 2>&1; then \
		echo "Uninstalling existing $(NS) release"; \
		helm uninstall $(NS) -n $(NS); \
		sleep 5; \
	else \
		echo "No existing $(NS) release found"; \
	fi; \
	helm install $(NS) manifests/helm/generic_service --create-namespace -n $(NS) \
		--set global.monitoring=opentelemetry \
		--set global.otelcollector="http://opentelemetry-collector-deployment.monitoring:4317" \
		--set skywalking.enabled=false \
		--set global.image.tag=637600ea \
		--set services.tsUiDashboard.nodePort=$(PORT)