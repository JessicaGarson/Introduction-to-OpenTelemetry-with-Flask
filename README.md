# Introduction to OpenTelemetry with Flask
OpenTelemetry (OTel) is an open-source, vendor-neutral observability framework designed to work with any backend system. It provides standardized APIs, libraries, and tools to collect telemetry data, such as metrics, logs, and traces. This talk is intended to provide a starting point for working with OpenTelemetry in Flask.

## Slides
You can find slides to accompany this talk in the folder of this repository entitled [slides](https://github.com/JessicaGarson/Introduction-to-OpenTelemetry-with-Flask/tree/main/slides).

## Code
The demo application being shown is a very simple to-do list application.

### Automatic instrumentation
[`app.py`](app.py) is a simple Flask application that can run locally by using the following command: 

```bash
python app.py
```

To use automatic instrumentation for this application, you can run this as follows:

```bash
pip install opentelemetry-distro
opentelemetry-bootstrap -a install
```

Followed by: 

```bash
export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
opentelemetry-instrument \
    --traces_exporter console \
    --metrics_exporter console \
    --logs_exporter console \
    --service_name todo \
    flask run -p 8080
```

### Manual instrumentation 
[`logging.py`](logging.py), [`traces.py`](traces.py), and [`metrics.py`](metrics.py) are demo how you would manually instrument your application. 

### Sending your data to a collector 
You can export your telemetry data to a collector by setting up a [yaml file like this one](tmp/otel-collector-config.yaml) and see it in Elastic. 

You can run this in your terminal:

```bash
docker run -p 4317:4317 \
  -v $(pwd)/tmp/otel-collector-config.yaml:/etc/otel-collector-config.yaml \
  otel/opentelemetry-collector:latest \
  --config=/etc/otel-collector-config.yaml
```

In a different terminal window, you will want to run the following:

```bash
pip install opentelemetry-exporter-otlp
```

Followed by:

```
export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
opentelemetry-instrument --logs_exporter otlp flask run -p 8080
```

### Elastic APM bridge
Another way to see telemetry data from your application in Elastic is to use the Elastic APM bridge. An example can be seen in [`elastic.py`](elastic.py).

You can run this code by the following command:

```
python elastic.py
```

## Resources
- [OpenTelemetry docs](https://opentelemetry.io/)
- [OpenTelemetry collectors](https://opentelemetry.io/docs/collector/) 
- [OpenTelemetry SDKs (including status of signals in each language ecosystem)](https://opentelemetry.io/docs/languages/) 
- [Elastic OpenTelemetry integration](https://www.elastic.co/guide/en/observability/current/apm-open-telemetry.html)
- [Elastic Observability Fundamentals](https://www.elastic.co/training/observability-fundamentals)
- [How To Monitor and Troubleshoot Applications using OpenTelemetry](https://www.youtube.com/watch?v=oTzIieqwMW0)
- [A practical guide to using OpenTelemetry in Python by Tom Eastman](https://www.youtube.com/watch?v=R8BYnL-Yp1w)
- [The State of OpenTelemetry](https://xeraa.net/talks/on-the-bleeding-edge-of-open-telemetry/)
- [APM Agent vs OpenTelemetry](https://discuss.elastic.co/t/elastic-apm-agent-vs-opentelemetry-client/332903)
- [Independence with OpenTelemetry on Elastic](https://www.elastic.co/blog/opentelemetry-observability)
