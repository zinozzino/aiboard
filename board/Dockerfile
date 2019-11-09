FROM node:10-alpine AS build

WORKDIR /app

COPY package.json yarn.lock tsconfig.json ./
RUN yarn install --frozen-lockfile

COPY src ./src
RUN yarn run build

FROM node:10-alpine

WORKDIR /app

RUN wget -O /usr/local/bin/dumb-init https://github.com/Yelp/dumb-init/releases/download/v1.2.2/dumb-init_1.2.2_amd64
RUN chmod +x /usr/local/bin/dumb-init

RUN apk update && \
  apk add --no-cache netcat-openbsd

COPY package.json yarn.lock entrypoint.sh ./
RUN yarn install --production --frozen-lockfile

COPY --from=build /app/dist ./dist

ENV PORT "8000"
EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["node", "dist/index.js"]
