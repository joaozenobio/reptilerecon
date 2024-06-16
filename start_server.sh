mkdir -p reptilerecon/media
cd reptilerecon && daphne -b 200.239.134.154 -p 8000 reptilerecon.asgi:application
