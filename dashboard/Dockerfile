FROM node:14.17.6-alpine3.11 AS build

WORKDIR /

COPY package.json .
RUN npm i

COPY public/ public/
COPY src/ src/

RUN npm run build

FROM byjg/nginx-extras:1.21
COPY --from=build /build/ /var/www/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
