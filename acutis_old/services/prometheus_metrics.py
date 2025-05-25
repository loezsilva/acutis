from flask import request, g
from prometheus_client import make_wsgi_app, Counter, Histogram, Gauge
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import time

REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total de requisições HTTP',
    ['method', 'endpoint']
)

REQUEST_LATENCY = Histogram(
    'http_request_latency_seconds',
    'Latência das requisições HTTP',
    ['endpoint']
)

RESPONSE_SIZE = Histogram(
    'http_response_size_bytes',
    'Tamanho das respostas HTTP em bytes',
    ['endpoint']
)

HTTP_ERRORS = Counter(
    'http_errors_total', 
    'Total de erros HTTP',
    ['endpoint', 'status_code']
)

ACTIVE_REQUESTS = Gauge(
    'http_requests_active',
    'Número de requisições HTTP ativas',
    ['endpoint']
)

CPU_USAGE = Gauge(
    'cpu_usage_percent',
    'Uso de CPU em percentual'
)

MEMORY_USAGE = Gauge(
    'memory_usage_bytes',
    'Uso de memória da aplicação em bytes'
)

DISK_USAGE = Gauge(
    'disk_usage_bytes',
    'Uso de disco em bytes'
)

DB_CONNECTIONS = Gauge(
    'db_connections_active',
    'Número de conexões de banco de dados ativas'
)

DB_QUERY_TIME = Histogram(
    'db_query_time_seconds',
    'Tempo de execução de consultas ao banco de dados',
    ['query_type']
)

QUEUED_JOBS = Gauge(
    'queued_jobs_total',
    'Número de jobs na fila'
)

PROCESSED_JOBS = Counter(
    'processed_jobs_total',
    'Número de jobs processados'
)

ACTIVE_USERS = Gauge(
    'active_users_total',
    'Número de usuários ativos'
)


def setup_prometheus(app):
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
        '/acutis-metrics': make_wsgi_app()
    })

    @app.before_request
    def before_request():
        g.start_time = time.time()
        ACTIVE_REQUESTS.labels(request.path).inc()

    @app.after_request
    def after_request(response):
        latency = time.time() - g.get("start_time", time.time())

        REQUEST_COUNT.labels(request.method, request.path).inc()
        REQUEST_LATENCY.labels(request.path).observe(latency)
        RESPONSE_SIZE.labels(request.path).observe(len(response.data))

        if response.status_code >= 400:
            HTTP_ERRORS.labels(request.path, response.status_code).inc()

        ACTIVE_REQUESTS.labels(request.path).dec()

        return response

