# Docker
docker build -f Dockerfile -t streamlit-app:latest . 
docker run -p 8501:8501 streamlit-app:latest