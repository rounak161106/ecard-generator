broker_url = "redis://localhost:6379/0"
result_backend = "redis://localhost:6379/1"
Timezone = "Asia/kolkata"
broker_connection_retry_on_startup = False
broker_connection_max_retries = 1
broker_transport_options = {
    'socket_timeout': 1.0,
    'socket_connect_timeout': 1.0
}