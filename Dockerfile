FROM python:3.12-alpine AS build

RUN mkdir -p /usr/local/src/quickwrench_api/quickwrench_api

COPY pyproject.toml manage.py requirements.txt /usr/local/src/quickwrench_api/
COPY quickwrench_api /usr/local/src/quickwrench_api/quickwrench_api

RUN cd /usr/local/src/quickwrench_api && \
  pip install --no-cache -r requirements.txt && \
  python manage.py collectstatic && \
  pip install --no-cache -U pip .

FROM python:3.12-alpine AS runtime

COPY --from=build /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=build /usr/local/bin /usr/local/bin

EXPOSE 8000

ENTRYPOINT ["/usr/local/bin/quickwrench-server"]
