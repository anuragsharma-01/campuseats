const fs = require('fs');
const path = require('path');
const express = require('express');
const cors = require('cors');
const { ApolloServer } = require('@apollo/server');
const { expressMiddleware } = require('@apollo/server/express4');
const { readFileSync } = require('fs');
const pool = require('./db');

const typeDefs = readFileSync(path.join(__dirname, 'schema.graphql'), 'utf8');

const resolvers = {
  Query: {
    dishes: async () => {
      const [rows] = await pool.query(
        'SELECT id, name, price, available FROM dishes ORDER BY id'
      );
      return rows;
    },
    dish: async (_, { id }) => {
      const [rows] = await pool.query(
        'SELECT id, name, price, available FROM dishes WHERE id = ?',
        [id]
      );
      return rows[0] || null;
    }
  },

  Mutation: {
    addDish: async (_, { input }) => {
      const available = input.available ?? true;
      const [result] = await pool.query(
        'INSERT INTO dishes (name, price, available) VALUES (?, ?, ?)',
        [input.name, input.price, available]
      );

      const [rows] = await pool.query(
        'SELECT id, name, price, available FROM dishes WHERE id = ?',
        [result.insertId]
      );
      return rows[0];
    },

    updateDish: async (_, { id, name, price, available }) => {
      const fields = [];
      const values = [];

      if (name !== undefined) { fields.push('name = ?'); values.push(name); }
      if (price !== undefined) { fields.push('price = ?'); values.push(price); }
      if (available !== undefined) { fields.push('available = ?'); values.push(available); }

      if (fields.length === 0) {
        const [rows] = await pool.query(
          'SELECT id, name, price, available FROM dishes WHERE id = ?',
          [id]
        );
        return rows[0] || null;
      }

      values.push(id);
      await pool.query(
        `UPDATE dishes SET ${fields.join(', ')} WHERE id = ?`,
        values
      );

      const [rows] = await pool.query(
        'SELECT id, name, price, available FROM dishes WHERE id = ?',
        [id]
      );
      return rows[0] || null;
    }
  }
};

async function start() {
  const apollo = new ApolloServer({ typeDefs, resolvers });
  await apollo.start();

  const app = express();
  app.use(cors());
  app.use(express.json());

  app.use('/graphql', expressMiddleware(apollo));
  app.use(express.static(path.join(__dirname, 'public')));

  const port = Number(process.env.PORT || 4000);
  app.listen(port, () => {
    console.log(`CampusEats running at http://localhost:${port}`);
    console.log(`GraphQL endpoint: http://localhost:${port}/graphql`);
  });
}

start().catch(err => {
  console.error('Failed to start server:', err);
  process.exit(1);
});
