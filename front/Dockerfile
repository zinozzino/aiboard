FROM node:10-slim

WORKDIR /app
COPY package.json yarn.lock ./
RUN yarn install --production --frozen-lockfile

COPY . ./

EXPOSE 8000

CMD ["yarn", "run", "start"]
