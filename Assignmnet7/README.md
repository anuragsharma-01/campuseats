# CS543 Web Services — Assignment 7
## Build one CampusEats service in GraphQL

### Team
Members : 
Anurag Sharma (Leader) ,
Harendra Godara ,
Mohit Taylor ,
Harshita Rathore ,

### 1. Which CampusEats service did you pick?
We picked the **Menu/Dish service**. The GraphQL API exposes dishes with `id`, `name`, `price`, and `available` fields.

### 2. One field a client can skip and one it cannot
A client can skip `available` because it is not marked with `!` in the `AddDishInput` input type; the resolver supplies `true` by default.

The `name` and `price` fields cannot be skipped when adding a dish because they are marked with `!`. The `!` means the field is **non-null/required** in GraphQL.

### 3. Map it to SQL
For the `dish(id: ID!)` query, the GraphQL `id` argument becomes the SQL `WHERE` condition:

```sql
SELECT id, name, price, available
FROM dishes
WHERE id = ?
```

The `addDish` mutation resolver runs the SQL `INSERT`:

```sql
INSERT INTO dishes (name, price, available)
VALUES (?, ?, ?)
```

### Files
- `schema.graphql` — GraphQL type, Query and Mutation
- `server.js` — Apollo Server + Express + resolvers
- `db.js` — mysql2 connection pool
- `schema.sql` — table and 4 seed rows
- `public/index.html` — HTML/CSS/JS frontend

### Run
1. Install Node.js and MySQL.
2. Create the database and seed rows:
   ```bash
   mysql -u root -p < schema.sql
   ```
3. Copy environment settings:
   ```bash
   cp .env.example .env
   ```
4. Edit `.env` with your MySQL password.
5. Install dependencies:
   ```bash
   npm install
   ```
6. Start:
   ```bash
   npm start
   ```
7. Open:
   `http://localhost:4000`

GraphQL endpoint:
`http://localhost:4000/graphql`

### Required demonstration
1. Show the initial 4 dishes in the webpage.
2. Add a dish using the **Add Dish** button.
3. Show the new dish after mutation.
4. Take two screenshots: **before** and **after** the mutation.
5. Add the screenshots and your Google Drive demonstration-video link to the final GitHub repository.

### Minimum GraphQL operations

Query:
```graphql
query {
  dishes {
    id
    name
    price
    available
  }
}
```

Mutation:
```graphql
mutation {
  addDish(input: { name: "Paneer Roll", price: 90 }) {
    id
    name
    price
  }
}
```
