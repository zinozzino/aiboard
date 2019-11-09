import {MigrationInterface, QueryRunner} from "typeorm";

export class AddBoardRelatedModels1573284761164 implements MigrationInterface {
    name = 'AddBoardRelatedModels1573284761164'

    public async up(queryRunner: QueryRunner): Promise<any> {
        await queryRunner.query(`CREATE TABLE "comment" ("id" character varying(12) NOT NULL, "body" text NOT NULL DEFAULT '', "createdTime" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP, CONSTRAINT "PK_0b0e4bbc8415ec426f87f3a88e2" PRIMARY KEY ("id"))`, undefined);
        await queryRunner.query(`CREATE TABLE "article" ("id" character varying(10) NOT NULL, "created_time" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP, "ownerId" character varying(8), "draftsId" integer, "commentsId" character varying(12), CONSTRAINT "PK_40808690eb7b915046558c0f81b" PRIMARY KEY ("id"))`, undefined);
        await queryRunner.query(`CREATE TABLE "article_draft" ("id" SERIAL NOT NULL, "title" text NOT NULL DEFAULT '', "body" text NOT NULL DEFAULT '', "createdTime" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP, "articleId" character varying(10), CONSTRAINT "PK_378506fe8011c050a7f014927bf" PRIMARY KEY ("id"))`, undefined);
        await queryRunner.query(`ALTER TABLE "user" ADD "articlesId" character varying(10)`, undefined);
        await queryRunner.query(`ALTER TABLE "user" ADD "commentsId" character varying(12)`, undefined);
        await queryRunner.query(`ALTER TABLE "user" ADD CONSTRAINT "FK_3508ee6ec22614e73c96f217f76" FOREIGN KEY ("articlesId") REFERENCES "article"("id") ON DELETE NO ACTION ON UPDATE NO ACTION`, undefined);
        await queryRunner.query(`ALTER TABLE "user" ADD CONSTRAINT "FK_bd84d3585680cde8c2c3cc0788f" FOREIGN KEY ("commentsId") REFERENCES "comment"("id") ON DELETE NO ACTION ON UPDATE NO ACTION`, undefined);
        await queryRunner.query(`ALTER TABLE "article" ADD CONSTRAINT "FK_9c7bd5faae7271b4f09dc64a165" FOREIGN KEY ("ownerId") REFERENCES "user"("id") ON DELETE NO ACTION ON UPDATE NO ACTION`, undefined);
        await queryRunner.query(`ALTER TABLE "article" ADD CONSTRAINT "FK_0b41440715f83e18dd89a0f091b" FOREIGN KEY ("draftsId") REFERENCES "article_draft"("id") ON DELETE NO ACTION ON UPDATE NO ACTION`, undefined);
        await queryRunner.query(`ALTER TABLE "article" ADD CONSTRAINT "FK_1e15aea8108998b9b8b7894d012" FOREIGN KEY ("commentsId") REFERENCES "comment"("id") ON DELETE NO ACTION ON UPDATE NO ACTION`, undefined);
        await queryRunner.query(`ALTER TABLE "article_draft" ADD CONSTRAINT "FK_06ce024f351d3ee1abf74764739" FOREIGN KEY ("articleId") REFERENCES "article"("id") ON DELETE NO ACTION ON UPDATE NO ACTION`, undefined);
    }

    public async down(queryRunner: QueryRunner): Promise<any> {
        await queryRunner.query(`ALTER TABLE "article_draft" DROP CONSTRAINT "FK_06ce024f351d3ee1abf74764739"`, undefined);
        await queryRunner.query(`ALTER TABLE "article" DROP CONSTRAINT "FK_1e15aea8108998b9b8b7894d012"`, undefined);
        await queryRunner.query(`ALTER TABLE "article" DROP CONSTRAINT "FK_0b41440715f83e18dd89a0f091b"`, undefined);
        await queryRunner.query(`ALTER TABLE "article" DROP CONSTRAINT "FK_9c7bd5faae7271b4f09dc64a165"`, undefined);
        await queryRunner.query(`ALTER TABLE "user" DROP CONSTRAINT "FK_bd84d3585680cde8c2c3cc0788f"`, undefined);
        await queryRunner.query(`ALTER TABLE "user" DROP CONSTRAINT "FK_3508ee6ec22614e73c96f217f76"`, undefined);
        await queryRunner.query(`ALTER TABLE "user" DROP COLUMN "commentsId"`, undefined);
        await queryRunner.query(`ALTER TABLE "user" DROP COLUMN "articlesId"`, undefined);
        await queryRunner.query(`DROP TABLE "article_draft"`, undefined);
        await queryRunner.query(`DROP TABLE "article"`, undefined);
        await queryRunner.query(`DROP TABLE "comment"`, undefined);
    }

}
