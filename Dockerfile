FROM continuumio/miniconda3

# Directorio de trabajo
WORKDIR /app

# Copiar environment.yml
COPY environment.yml .

# Crear el entorno conda
RUN conda env create -f environment.yml

# Activar el entorno conda en el shell
SHELL ["conda", "run", "-n", "TFG-IDEALISTA", "/bin/bash", "-c"]

# Copiar el código
COPY . .

# Exponer puertos para Django y Streamlit
EXPOSE 8000 8501

# Comando para iniciar Django y Streamlit
CMD ["conda", "run", "-n", "TFG-IDEALISTA", "bash", "-c", "python backend/manage.py runserver 0.0.0.0:8000 & streamlit run frontend/src/app.py --server.port=8501 --server.address=0.0.0.0"]