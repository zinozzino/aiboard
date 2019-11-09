import express from 'express';
import { getRepository } from 'typeorm';
import User from '../models/user';

const router = express.Router();

router.get('/', async (req, res) => {
  const userRepository = getRepository(User);

  const userList = userRepository.find({});

  return res.status(200).send(JSON.stringify(userList));
});

router.post('/', async (req, res) => {
  const userRepository = getRepository(User);

  const newUser = userRepository.create({ ...req.body });

  await userRepository.save(newUser);

  return res.status(201).send(JSON.stringify(newUser));
});

export const path = '/users';

export default router;
