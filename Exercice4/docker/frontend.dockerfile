FROM nginx:alpine

COPY src/index.html /usr/share/nginx/html/

EXPOSE 3000

CMD sed -i 's/80/3000/g' /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'