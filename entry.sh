mkdir $HOME/.postgresql/ ; cp ./config/root.crt $HOME/.postgresql/

uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4 --proxy-headers
