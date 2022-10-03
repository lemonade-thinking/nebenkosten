FROM python:3.7-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 80
RUN mkdir ~/.streamlit
RUN cp config.toml ~/.streamlit/config.toml
RUN cp secrets.toml ~/.streamlit/secrets.toml
WORKDIR /app
ENTRYPOINT ["streamlit", "run"]
CMD ["nebenkosten_app.py"]
