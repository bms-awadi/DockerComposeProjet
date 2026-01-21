FROM nginx:alpine

# code source directement dans l'image
COPY ../frontend/src /usr/share/nginx/html

EXPOSE 80