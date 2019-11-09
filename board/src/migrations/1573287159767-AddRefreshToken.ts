import {MigrationInterface, QueryRunner} from "typeorm";

export class AddRefreshToken1573287159767 implements MigrationInterface {
    name = 'AddRefreshToken1573287159767'

    public async up(queryRunner: QueryRunner): Promise<any> {
        await queryRunner.query(`CREATE TABLE "refresh_token" ("token" character varying(64) NOT NULL, "createdTime" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP, "expiredTime" TIMESTAMP WITH TIME ZONE NOT NULL, CONSTRAINT "PK_c31d0a2f38e6e99110df62ab0af" PRIMARY KEY ("token"))`, undefined);
        await queryRunner.query(`ALTER TABLE "user" ADD "refreshTokensToken" character varying(64)`, undefined);
        await queryRunner.query(`ALTER TABLE "user" ADD CONSTRAINT "FK_d072928781b8bae99e03da324b5" FOREIGN KEY ("refreshTokensToken") REFERENCES "refresh_token"("token") ON DELETE NO ACTION ON UPDATE NO ACTION`, undefined);
    }

    public async down(queryRunner: QueryRunner): Promise<any> {
        await queryRunner.query(`ALTER TABLE "user" DROP CONSTRAINT "FK_d072928781b8bae99e03da324b5"`, undefined);
        await queryRunner.query(`ALTER TABLE "user" DROP COLUMN "refreshTokensToken"`, undefined);
        await queryRunner.query(`DROP TABLE "refresh_token"`, undefined);
    }

}
