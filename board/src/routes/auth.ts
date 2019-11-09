import express from 'express';
import { body, validationResult, matchedData } from 'express-validator';
import { getRepository } from 'typeorm';
import { isUndefined } from 'lodash';

import User from '../models/user';
import RefreshToken from '../models/refresh-token';

const router = express.Router();

router.post(
  '/token',
  ...[
    body('username')
      .not()
      .isEmpty(),
    body('password')
      .not()
      .isEmpty(),
  ],
  async (req, res) => {
    const errors = validationResult(req);

    if (!errors.isEmpty()) {
      return res.status(422).json({ errors: errors.array() });
    }

    const bodyData = matchedData(req, { locations: ['body'] });

    const repository = getRepository(User);
    const tokenRepo = getRepository(RefreshToken);

    const user = await repository.findOne({ userName: bodyData.username });

    if (isUndefined(user)) {
      return res.status(404).send({});
    }

    if (!user.verifyPassword(bodyData.password)) {
      return res.status(401).send({});
    }

    const accessToken = user.createToken();
    const refreshToken = tokenRepo.create({ user });

    try {
      await tokenRepo.save(refreshToken);
    } catch {}

    return res
      .status(201)
      .cookie('access_token', accessToken, { httpOnly: true })
      .cookie('refresh_token', refreshToken, { httpOnly: true })
      .json({
        accessToken,
        refreshToken: refreshToken.token,
      });
  }
);

export const path = '/auth';

export default router;
