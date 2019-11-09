import { Entity, Column, BaseEntity, BeforeInsert, ManyToOne } from 'typeorm';
import { pbkdf2Sync } from 'crypto';
import nanoid from 'nanoid';
import { isEqual } from 'lodash';
import { Exclude } from 'class-transformer';
import jwt from 'jsonwebtoken';
import ms from 'ms';

import config from '../config';
import Article from './article';
import Comment from './comment';
import RefreshToken from './refresh-token';

@Entity()
export default class User extends BaseEntity {
  @Column({ type: 'character varying', length: 8, primary: true })
  id: string;

  @Column({
    name: 'first_name',
    type: 'character varying',
    length: 64,
    default: '',
  })
  firstName: string;

  @Column({
    name: 'last_name',
    type: 'character varying',
    length: 64,
    default: '',
  })
  lastName: string;

  @Column({ type: 'character varying', length: 256, unique: true })
  email: string;

  @Column({ name: 'user_name', type: 'character varying', length: 64 })
  userName: string;

  @Exclude()
  @Column({ type: 'character varying', length: 128 })
  password: string;

  @Column({
    name: 'created_time',
    type: 'timestamp with time zone',
    default: () => 'CURRENT_TIMESTAMP',
  })
  createdTime: Date;

  @Exclude()
  @ManyToOne(
    () => Article,
    article => article.owner
  )
  articles: Article[];

  @Exclude()
  @ManyToOne(
    () => Comment,
    comment => comment.owner
  )
  comments: Comment[];

  @Exclude()
  @ManyToOne(
    () => RefreshToken,
    refreshToken => refreshToken.user
  )
  refreshTokens: RefreshToken[];

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

  createToken() {
    return jwt.sign({ id: this.id }, config.secretKey, {
      expiresIn: ms(config.accessTimeout),
    });
  }
}
