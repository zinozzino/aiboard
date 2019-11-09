import { Entity, Column, PrimaryGeneratedColumn, ManyToOne } from 'typeorm';
import { Exclude } from 'class-transformer';
import Article from './article';

@Entity()
export default class ArticleDraft {
  @Exclude()
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ type: 'text', default: '' })
  title: string;

  @Column({ type: 'text', default: '' })
  body: string;

  @Column({
    type: 'timestamp with time zone',
    default: () => 'CURRENT_TIMESTAMP',
  })
  createdTime: Date;

  @Exclude()
  @ManyToOne(
    () => Article,
    article => article.drafts
  )
  article: Article;
}
