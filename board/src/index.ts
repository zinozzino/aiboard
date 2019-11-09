import 'reflect-metadata';
import express from 'express';
import glob from 'glob';
import cors from 'cors';
import morgan from 'morgan';
import { createConnection } from 'typeorm';

import config from './config';

createConnection({
  type: 'postgres',
  host: config.database.host,
  port: config.database.port,
  username: config.database.username,
  password: config.database.password,
  database: config.database.name,
  logging: true,
  entities: [`${__dirname}/models/**/*`],
  migrations: [`${__dirname}/migrations/**/*`],
})
  .then(() => {
    const app = express();

    app.use(express.urlencoded({ extended: true }));
    app.use(express.json());
    app.use(cors());
    app.use(morgan('combined'));

    Promise.all(
      glob
        .sync(`${__dirname}/routes/**/*`)
        .map(moduleName => import(moduleName))
    ).then(routeModules => {
      routeModules.map((routeModule: any) => {
        app.use(routeModule.path, routeModule.default);
      });
    });

    app.listen(config.port, config.host, () => {
      console.log(`Server is running at ${config.host}:${config.port}...`);
    });
  })
  .catch((err: Error) => {
    console.log('Application Error');
    console.log(err.stack);
  });
