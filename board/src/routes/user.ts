import express from 'express';
import { body, matchedData, validationResult } from 'express-validator';
import { getRepository } from 'typeorm';
import { classToPlain } from 'class-transformer';
import { isUndefined } from 'lodash';
import User from '../models/user';

const router = express.Router();

router.get('/', async (req, res) => {
  const userRepository = getRepository(User);

  const userList = await userRepository.find({});

  return res.status(200).json(classToPlain(userList));
});

router.post(
  '/',
  ...[
    body('user_name')
      .not()
      .isEmpty(),
    body('password')
      .not()
      .isEmpty(),
    body('email').isEmail(),
    body('first_name').optional(),
    body('last_name').optional(),
  ],
  async (req, res) => {
    const userRepository = getRepository(User);

    const errors = validationResult(req);

    if (!errors.isEmpty()) {
      return res.status(422).json({ errors: errors.array() });
    }

    const bodyData = matchedData(req, { locations: ['body'] });

    const newUser = userRepository.create({
      ...bodyData,
      userName: bodyData.user_name,
      firstName: bodyData.first_name,
      lastName: bodyData.last_name,
    });

    try {
      await userRepository.save(newUser);
    } catch (e) {
      return res.status(400).json({ message: `${e}` });
    }

    return res.status(201).json(classToPlain(newUser));
  }
);

router.put('/:id', async (req, res) => {
  const { id } = req.params;
  const userRepository = getRepository(User);

  const user = userRepository.findOne({ id });

  if (isUndefined(user)) {
    return res.status(404).json({});
  }

  userRepository.update(id, req.body);

  return res.status(200).json(classToPlain(user));
});

router.delete('/:id', async (req, res) => {
  const { id } = req.params;

  const userRepository = getRepository(User);

  userRepository.delete({ id });

  return res.status(204).json({});
});

export const path = '/users';

export default router;
