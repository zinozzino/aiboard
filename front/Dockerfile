FROM node:10-slim

WORKDIR /app

RUN wget -O /usr/bin/dumb-init https://github.com/Yelp/dumb-init/releases/download/v1.2.2/dumb-init_1.2.2_amd64
RUN chmod +x /usr/bin/dumb-init

COPY package.json yarn.lock ./
RUN yarn install --production --frozen-lockfile

COPY . ./

EXPOSE 8000

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["yarn", "run", "start"]
