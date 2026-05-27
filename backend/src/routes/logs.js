const express = require('express');
const prisma = require('../lib/prisma');

const router = express.Router();

function parsePaginationQuery(query) {
  const limit = query.limit === undefined ? 10 : Number.parseInt(query.limit, 10);
  const offset = query.offset === undefined ? 0 : Number.parseInt(query.offset, 10);

  if (Number.isNaN(limit) || limit <= 0) {
    return { error: 'limit must be a positive integer.' };
  }

  if (Number.isNaN(offset) || offset < 0) {
    return { error: 'offset must be a non-negative integer.' };
  }

  return { limit, offset };
}

function buildWhereClause(query) {
  const where = {};

  if (query.action) {
    where.action = String(query.action);
  }

  if (query.userId !== undefined) {
    const userId = Number.parseInt(query.userId, 10);

    if (Number.isNaN(userId)) {
      return { error: 'userId must be a number.' };
    }

    where.userId = userId;
  }

  return { where };
}

router.get('/', async (req, res, next) => {
  try {
    const pagination = parsePaginationQuery(req.query);

    if (pagination.error) {
      return res.status(400).json({ message: pagination.error });
    }

    const whereResult = buildWhereClause(req.query);

    if (whereResult.error) {
      return res.status(400).json({ message: whereResult.error });
    }

    const { limit, offset } = pagination;
    const { where } = whereResult;
    const [items, total] = await Promise.all([
      prisma.auditLog.findMany({
        where,
        orderBy: {
          createdAt: 'desc',
        },
        skip: offset,
        take: limit,
        select: {
          id: true,
          action: true,
          entity: true,
          entityId: true,
          detail: true,
          createdAt: true,
          user: {
            select: {
              id: true,
              name: true,
              email: true,
              role: true,
            },
          },
        },
      }),
      prisma.auditLog.count({ where }),
    ]);

    return res.json({
      items,
      pagination: {
        limit,
        offset,
        total,
      },
    });
  } catch (error) {
    return next(error);
  }
});

module.exports = router;
