FROM python:3.9-slim AS dependencies

SHELL ["/bin/bash", "-c"]
RUN apt-get update && apt-get install -y build-essential ffmpeg python3-dev libasound2-dev libportaudio2 libportaudiocpp0 portaudio19-dev

WORKDIR /app

COPY requirements.txt .

RUN python -m venv venv
RUN source venv/bin/activate

RUN python -m pip install -r requirements.txt

FROM dependencies AS app

WORKDIR /app

COPY --from=dependencies /app/venv /app/venv

COPY . .

RUN source venv/bin/activate

CMD ["python", "playground.py"]