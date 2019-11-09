FROM node:10-slim AS build

WORKDIR /app

COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile

COPY src tsconfig.json ./
RUN yarn run build

FROM node:10-slim

WORKDIR /app

RUN wget -O /usr/local/bin/dumb-init https://github.com/Yelp/dumb-init/releases/download/v1.2.2/dumb-init_1.2.2_amd64
RUN chmod +x /usr/local/bin/dumb-init

COPY --from=build package.json yarn.lock ./
RUN yarn install --production --frozen-lockfile

COPY entrypoint.sh ./

COPY --from=build dist ./

ENV PORT "8000"
EXPOSE 8000
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["yarn", "run", "start"]
