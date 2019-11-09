import {MigrationInterface, QueryRunner} from "typeorm";

export class AllowEmptyStringOnFirstAndLastName1573282486634 implements MigrationInterface {
    name = 'AllowEmptyStringOnFirstAndLastName1573282486634'

    public async up(queryRunner: QueryRunner): Promise<any> {
        await queryRunner.query(`ALTER TABLE "user" ALTER COLUMN "first_name" SET DEFAULT ''`, undefined);
        await queryRunner.query(`ALTER TABLE "user" ALTER COLUMN "last_name" SET DEFAULT ''`, undefined);
    }

    public async down(queryRunner: QueryRunner): Promise<any> {
        await queryRunner.query(`ALTER TABLE "user" ALTER COLUMN "last_name" DROP DEFAULT`, undefined);
        await queryRunner.query(`ALTER TABLE "user" ALTER COLUMN "first_name" DROP DEFAULT`, undefined);
    }

}
