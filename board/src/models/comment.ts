import { Entity, BaseEntity, Column, OneToMany, BeforeInsert } from 'typeorm';
import { Exclude } from 'class-transformer';
import nanoid from 'nanoid';

import Article from './article';
import User from './user';

@Entity()
export default class Comment extends BaseEntity {
  @Column({ type: 'character varying', length: 12, primary: true })
  id: string;

  @Column({ type: 'text', default: '' })
  body: string;

  @Column({
    type: 'timestamp with time zone',
    default: () => 'CURRENT_TIMESTAMP',
  })
  createdTime: Date;

  @OneToMany(
    () => User,
    user => user.comments
  )
  owner: User;

  @Exclude()
  @OneToMany(
    () => Article,
    article => article.comments
  )
  article: Article;

  @BeforeInsert()
  beforeInsert() {
    this.id = nanoid(12);
  }
}
