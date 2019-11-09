import { BaseEntity, Column, ManyToOne, Entity, BeforeInsert } from 'typeorm';
import { Exclude } from 'class-transformer';
import nanoid from 'nanoid';

import User from './user';
import ArticleDraft from './article-draft';
import Comment from './comment';

@Entity()
export default class Article extends BaseEntity {
  @Column({ type: 'character varying', length: 10, primary: true })
  id: string;

  @Column({
    name: 'created_time',
    type: 'timestamp with time zone',
    default: () => 'CURRENT_TIMESTAMP',
  })
  createdTime: Date;

  @ManyToOne(
    () => User,
    user => user.articles
  )
  owner: User;

  @Exclude()
  @ManyToOne(
    () => ArticleDraft,
    draft => draft.article
  )
  drafts: ArticleDraft[];

  @ManyToOne(
    () => Comment,
    comment => comment.article
  )
  comments: Comment[];

  @BeforeInsert()
  beforeInsert() {
    this.id = nanoid(10);
  }
}
