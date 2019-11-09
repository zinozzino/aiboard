import { Entity, BaseEntity, Column, BeforeInsert, OneToMany } from 'typeorm';
import nanoid from 'nanoid';
import ms from 'ms';

import config from '../config';
import User from './user';

@Entity()
export default class RefreshToken extends BaseEntity {
  @Column({ type: 'character varying', length: 64, primary: true })
  token: string;

  @Column({
    type: 'timestamp with time zone',
    default: () => 'CURRENT_TIMESTAMP',
  })
  createdTime: Date;

  @Column({ type: 'timestamp with time zone' })
  expiredTime: Date;

  @OneToMany(
    () => User,
    user => user.refreshTokens
  )
  user: User;

  @BeforeInsert()
  beforeInsert() {
    this.token = nanoid(64);
    this.expiredTime = new Date(Date.now() + ms(config.refreshTimeout));
  }
}
