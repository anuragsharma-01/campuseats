# CampusEats — GraphQL Service

## CS543 · Web Services · Assignment 7 of 12

A GraphQL-based service for the **CampusEats** food ordering system.

This project demonstrates how a small CampusEats service can be exposed through a **GraphQL API**, backed by a **MariaDB/MySQL database**, with a simple HTML/CSS frontend.

---

## 📌 Project Overview

For this assignment, we selected the **Menu / Dishes service** from CampusEats.

The service provides:

- A GraphQL schema for dishes
- A Query to retrieve dishes
- A Mutation to add a new dish
- MariaDB/MySQL database integration using `mysql2`
- GraphQL resolvers for database operations
- A simple HTML/CSS frontend
- Live interaction with the GraphQL API

### Architecture

```text
┌─────────────────────┐
│   HTML/CSS Frontend │
│   public/index.html │
└──────────┬──────────┘
           │ fetch()
           ▼
┌─────────────────────┐
│    GraphQL API      │
│      Apollo Server  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│      Resolvers      │
│   Query / Mutation  │
└──────────┬──────────┘
           │ SQL
           ▼
┌─────────────────────┐
│   MariaDB / MySQL   │
│      campuseats     │
│       dishes        │
└─────────────────────┘
```

---

## 🛠️ Technologies Used

- Node.js
- Apollo Server
- GraphQL
- MariaDB / MySQL
- `mysql2`
- HTML
- CSS
- JavaScript
- dotenv

---

## 📁 Project Structure

```text
CS543_A07_CampusEats_GraphQL/
│
├── public/
│   └── index.html
│
├── db.js
├── server.js
├── schema.graphql
├── schema.sql
├── package.json
├── package-lock.json
├── .env
├── .env.example
└── README.md
```

---

## 🍽️ Selected CampusEats Service

### Menu / Dishes Service

We selected the **Dishes/Menu** entity from CampusEats.

Each dish contains:

| Field | Type | Description |
|---|---|---|
| `id` | ID | Unique identifier |
| `name` | String | Name of the dish |
| `price` | Float | Price of the dish |
| `available` | Boolean | Whether the dish is currently available |

---

## 🗄️ Database

Database:

```text
campuseats
```

Table:

```text
dishes
```

The table contains the following fields:

```sql
id
name
price
available
```

### Seed Data

The initial database contains four dishes:

```text
Veg Burger       ₹120
Paneer Pizza     ₹180
Masala Dosa      ₹100
Veg Sandwich      ₹80
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
DB_HOST=localhost
DB_USER=harsh
DB_PASSWORD=YOUR_DATABASE_PASSWORD
DB_NAME=campuseats
DB_PORT=3306
```

> Do not commit the `.env` file to GitHub because it contains database credentials.

---

## ⚙️ Installation

Clone/download the project and enter the project directory:

```bash
cd CS543_A07_CampusEats_GraphQL
```

Install dependencies:

```bash
npm install
```

---

## 🗃️ Database Setup

Create the database:

```sql
CREATE DATABASE campuseats;
```

Grant the application user access:

```sql
GRANT ALL PRIVILEGES ON campuseats.* TO 'harsh'@'localhost';
FLUSH PRIVILEGES;
```

Select the database:

```sql
USE campuseats;
```

Create the `dishes` table and seed data using `schema.sql`.

Alternatively:

```bash
mariadb -u harsh -p campuseats < schema.sql
```

Verify:

```sql
SHOW TABLES;
SELECT * FROM dishes;
```

---

## 🚀 Running the Application

Start the Apollo GraphQL server:

```bash
npm start
```

The GraphQL server runs at:

```text
http://localhost:4000/graphql
```

The frontend is available through the server's public directory.

---

# 🔷 GraphQL Schema

The main GraphQL type is:

```graphql
type Dish {
  id: ID!
  name: String!
  price: Float!
  available: Boolean!
}
```

The API provides:

```graphql
type Query {
  dishes: [Dish!]!
  dish(id: ID!): Dish
}
```

And a mutation for adding a dish:

```graphql
type Mutation {
  addDish(input: AddDishInput!): Dish!
}
```

---

# 🔍 Query — List Dishes

The required query is:

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

### Example Response

```json
{
  "data": {
    "dishes": [
      {
        "id": "1",
        "name": "Veg Burger",
        "price": 120,
        "available": true
      },
      {
        "id": "2",
        "name": "Paneer Pizza",
        "price": 180,
        "available": true
      },
      {
        "id": "3",
        "name": "Masala Dosa",
        "price": 100,
        "available": true
      },
      {
        "id": "4",
        "name": "Veg Sandwich",
        "price": 80,
        "available": true
      }
    ]
  }
}
```

---

# ➕ Mutation — Add a Dish

A new dish can be added using:

```graphql
mutation {
  addDish(input: {
    name: "Paneer Roll"
    price: 90
  }) {
    id
    name
    price
    available
  }
}
```

Example response:

```json
{
  "data": {
    "addDish": {
      "id": "5",
      "name": "Paneer Roll",
      "price": 90,
      "available": true
    }
  }
}
```

---

# ❓ Assignment Questions

## 1. Which CampusEats service did you pick?

We selected the **Menu / Dishes service**.

The service exposes dishes through a GraphQL API and allows clients to retrieve the available dishes and add a new dish.

---

## 2. Name one field a client can skip and one it cannot. Why do we use `!`?

A client can skip:

```graphql
available
```

For example:

```graphql
query {
  dishes {
    id
    name
    price
  }
}
```

The client does not have to request every field.

A field marked with `!` is **non-null**.

For example:

```graphql
name: String!
```

The `!` means that the server must return a value for `name`; it cannot return `null`.

This helps define the GraphQL contract clearly and ensures required data is always available.

---

## 3. Map GraphQL to SQL

For the `dishes` query:

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

The resolver executes an SQL query similar to:

```sql
SELECT id, name, price, available
FROM dishes;
```

For a dish-by-ID query:

```graphql
dish(id: 2) {
  id
  name
  price
  available
}
```

The `id` argument becomes the SQL `WHERE` condition:

```sql
SELECT id, name, price, available
FROM dishes
WHERE id = ?;
```

The `addDish` mutation executes the SQL `INSERT` operation:

```sql
INSERT INTO dishes (name, price, available)
VALUES (?, ?, ?);
```

The **`addDish` resolver** is responsible for running this INSERT operation.

---

# 🔄 Request Flow

### Query

```text
Client
  ↓
GraphQL Query
  ↓
Apollo Server
  ↓
dishes Resolver
  ↓
SELECT SQL Query
  ↓
MariaDB
  ↓
GraphQL Response
```

### Mutation

```text
Client
  ↓
GraphQL Mutation
  ↓
Apollo Server
  ↓
addDish Resolver
  ↓
INSERT SQL Query
  ↓
MariaDB
  ↓
New Dish
  ↓
GraphQL Response
```

---

# 🧪 Testing

The API was tested using Apollo Server's GraphQL interface.

### Test 1 — Read existing dishes

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

### Test 2 — Add a dish

```graphql
mutation {
  addDish(input: {
    name: "Paneer Roll"
    price: 90
  }) {
    id
    name
    price
    available
  }
}
```

### Test 3 — Verify the new dish

Run the `dishes` query again and verify that the newly added dish appears in the result.

---

# 🖥️ Frontend

The project contains a simple frontend at:

```text
public/index.html
```

The frontend uses JavaScript `fetch()` to communicate with the GraphQL endpoint.

It displays the dishes returned by the GraphQL Query and provides a button to execute the Mutation.

---

# 📸 Demonstration

The assignment requires demonstration screenshots showing:

### Before Mutation

The initial list of dishes before adding a new dish.

```text
[ Add Screenshot Here ]
```

### After Mutation

The updated list showing the newly added dish.

```text
[ Add Screenshot Here ]
```

### Demonstration Video

Google Drive video link:

```text
[ Add Google Drive Video Link Here ]
```

---

# 👥 Team Members

| Roll Number | Name |
|---|---|
| YOUR_ROLL_NUMBER | Harendra Godara |
| TEAMMATE_ROLL_NUMBER | TEAMMATE_NAME |

> Replace the placeholders with the actual team members and roll numbers before submission.

---

# 📦 Deliverables

This project contains:

- `schema.graphql` — GraphQL type, Query and Mutation
- `server.js` — Apollo Server and GraphQL resolvers
- `db.js` — MariaDB/MySQL connection
- `schema.sql` — Database table and seed data
- `public/index.html` — Frontend
- `README.md` — Project documentation

---

# 👨‍🏫 Course Information

**Course:** CS543 — Web Services  
**Assignment:** 7 of 12  
**Topic:** GraphQL  
**Institution:** IIIT Vadodara  

**Instructor:** Dr. Pramit Mazumdar

---

## ✅ Assignment Status

| Requirement | Status |
|---|---|
| GraphQL Schema | ✅ Completed |
| Query | ✅ Completed |
| Mutation | ✅ Completed |
| Database | ✅ Completed |
| MySQL/MariaDB Connection | ✅ Completed |
| Resolvers | ✅ Completed |
| Frontend | ✅ Included |
| Before Screenshot | ⏳ Add screenshot |
| After Screenshot | ⏳ Add screenshot |
| Demo Video | ⏳ Add Google Drive link |
| Team Details | ⏳ Add roll numbers |

---

## ▶️ Quick Start

```bash
npm install
```

Configure `.env`:

```env
DB_HOST=localhost
DB_USER=harsh
DB_PASSWORD=YOUR_DATABASE_PASSWORD
DB_NAME=campuseats
DB_PORT=3306
```

Then:

```bash
npm start
```

Open:

```text
http://localhost:4000/graphql
```

Run:

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

The CampusEats GraphQL service is now ready to use.