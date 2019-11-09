import express from 'express';
import { body, validationResult, matchedData } from 'express-validator';
import { classToPlain } from 'class-transformer';
import { getRepository } from 'typeorm';

import Article from '../models/article';

const router = express.Router();

router.get('/', async (req, res) => {
  const repository = getRepository(Article);

  const articleList = await repository.find({});

  return res.status(200).json(classToPlain(articleList));
});

router.post(
  '/',
  ...[
    body('title')
      .not()
      .isEmpty(),
    body('body')
      .not()
      .isEmpty(),
  ],
  async (req, res) => {
    const repository = getRepository(Article);

    const errors = validationResult(req);

    if (!errors.isEmpty()) {
      return res.status(422).json({ errors: errors.array() });
    }

    const newArticle = repository.create({
      ...matchedData(req, { locations: ['body'] }),
    });

    try {
      await repository.save(newArticle);
    } catch (e) {
      return res.status(400).json({ message: `${e}` });
    }

    return res.status(201).json(classToPlain(newArticle));
  }
);

export const path = '/articles';

export default router;
