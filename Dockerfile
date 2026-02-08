
FROM python:3.10-slim


WORKDIR /app


COPY ["*.py", "model_C=1.0.bin", "data-week-3.csv", "./"]


RUN pip install flask pandas numpy scikit-learn requests waitress matplotlib


RUN python train.py


EXPOSE 9696


ENTRYPOINT ["waitress-serve", "--listen=0.0.0.0:9696", "predict:app"]