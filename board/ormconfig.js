const {
  PGHOST = '127.0.0.1',
  PGPORT = '5432',
  PGDATABASE = 'aiboard',
  PGUSER = 'postgres',
  PGPASSWORD = '',
} = process.env;

module.exports = {
  type: 'postgres',
  host: PGHOST,
  port: parseInt(PGPORT, 10),
  username: PGUSER,
  password: PGPASSWORD,
  database: PGDATABASE,
  entities: ['src/models/**/*'],
  migrations: ['src/migrations/**/*'],
};
