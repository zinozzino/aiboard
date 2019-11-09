import { Entity, Column, BaseEntity, BeforeInsert } from 'typeorm';
import { pbkdf2Sync } from 'crypto';
import nanoid from 'nanoid';
import { isEqual } from 'lodash';

import config from '../config';

@Entity()
export default class User extends BaseEntity {
  @Column({ type: 'character varying', length: 8, primary: true })
  id: string;

  @Column({ name: 'first_name', type: 'character varying', length: 64 })
  firstName: string;

  @Column({ name: 'last_name', type: 'character varying', length: 64 })
  lastName: string;

  @Column({ type: 'character varying', length: 256, unique: true })
  email: string;

  @Column({ name: 'user_name', type: 'character varying', length: 64 })
  userName: string;

  @Column({ type: 'character varying', length: 128 })
  password: string;

  @Column({
    name: 'created_time',
    type: 'timestamp with time zone',
    default: () => 'CURRENT_TIMESTAMP',
  })
  createdTime: Date;

  @BeforeInsert()
  beforeInsert(): void {
    this.id = nanoid(8);
    this.setPassword(this.password);
  }

  setPassword(password: string): void {
    this.password = pbkdf2Sync(
      password,
      config.secretKey,
      100000,
      64,
      'sha256'
    ).toString('base64');
  }

  verifyPassword(password: string) {
    return isEqual(
      pbkdf2Sync(password, config.secretKey, 100000, 64, 'sha256').toString(
        'base64'
      ),
      this.password
    );
  }
}
