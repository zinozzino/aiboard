const {
  HOST = '0.0.0.0',
  PORT = '8000',
  PGHOST = '127.0.0.1',
  PGPORT = '5432',
  PGDATABASE = 'aiboard',
  PGUSER = 'postgres',
  PGPASSWORD = '',
  SECRET_KEY = '',
} = process.env;

const config = {
  host: HOST,
  port: parseInt(PORT, 10),
  secretKey: SECRET_KEY,
  database: {
    host: PGHOST,
    port: parseInt(PGPORT, 10),
    name: PGDATABASE,
    username: PGUSER,
    password: PGPASSWORD,
  },
};

export type IConfig = typeof config;

export default config;
