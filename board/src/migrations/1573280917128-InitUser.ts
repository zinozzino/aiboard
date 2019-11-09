import { MigrationInterface, QueryRunner } from 'typeorm';

export class InitUser1573280917128 implements MigrationInterface {
  name = 'InitUser1573280917128';

  public async up(queryRunner: QueryRunner): Promise<any> {
    await queryRunner.query(
      `CREATE TABLE "user" ("id" character varying(8) NOT NULL, "first_name" character varying(64) NOT NULL, "last_name" character varying(64) NOT NULL, "email" character varying(256) NOT NULL, "user_name" character varying(64) NOT NULL, "password" character varying(128) NOT NULL, "created_time" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP, CONSTRAINT "UQ_e12875dfb3b1d92d7d7c5377e22" UNIQUE ("email"), CONSTRAINT "PK_cace4a159ff9f2512dd42373760" PRIMARY KEY ("id"))`,
      undefined
    );
  }

  public async down(queryRunner: QueryRunner): Promise<any> {
    await queryRunner.query(`DROP TABLE "user"`, undefined);
  }
}
