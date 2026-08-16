# CampusEats — Web Services Assignment 2

## Team Members

| Member | Name | Responsibility |
|---|---|---|
| 1 | **Anurag Sharma (Leader)** | Identity & Administration Service |
| 2 | **Mohit Tailor** | Catalogue Service |
| 3 | **Harshita Rathore** | Order Service |
| 4 | **Harendra Godara** | Payment Service |

## Project Overview

CampusEats is a campus food ordering system. Students can discover food, search menus, select food items, place orders, pay when required, track orders, view previous orders and select pickup locations.

Food providers can manage menus and food availability, receive incoming orders, accept or reject them, prepare food and update order status. Administrators manage users, food providers and system information.

## Service Architecture

### Identity & Administration Service — Anurag Sharma (Leader)
Owns Users, Roles, Food Provider profiles and Administrator access.

Operations: `registerUser`, `getUser`, `verifyAccess`

### Catalogue Service — Mohit Tailor
Owns Restaurants, Menus, Food Items, Categories, Availability and Pickup Locations.

Operations: `searchItems`, `getItem`, `checkItems`, `updateAvailability`

### Order Service — Harshita Rathore
Owns Orders, Order Items, Order Status and Pickup selections.

Operations: `createOrder`, `getOrder`, `updateStatus`, `listStudentOrders`

### Payment Service — Harendra Godara
Owns Payments, Payment Status and Payment Transactions.

Operations: `authorizePayment`, `getPayment`, `refundPayment`

## Main Communication

```text
Identity Service --verifyAccess--> Order Service
Order Service --checkItems--> Catalogue Service
Order Service --authorizePayment--> Payment Service
```

## placeOrder

The Order Service receives the student's selected items and pickup location, verifies access when required, asks Catalogue Service to validate availability/current prices, and calls Payment Service when payment is required. After successful validation, the order is created and the student receives the order ID, status and total.

Possible errors:
- Invalid or unavailable food item
- Invalid quantity
- Invalid pickup location
- Access denied
- Payment declined

## Database Ownership

**Identity:** `users`, `provider_profiles`

**Catalogue:** `restaurants`, `categories`, `menus`, `food_items`, `pickup_locations`

**Order:** `orders`, `order_items`

**Payment:** `payments`

Each service owns its own data.

## Files

- `design.pdf` — capabilities, services, contracts, `placeOrder` specification and validation
- `services.drawio` — editable service architecture diagram
- `services.png` — service architecture image
- `schema.drawio` — editable database diagram
- `schema.png` — database diagram image
- `schema.sql` — SQL CREATE TABLE statements
- `README.md` — this documentation

## Opening Draw.io Files

Go to **https://app.diagrams.net/** → **File → Open From → Device** → select `services.drawio` or `schema.drawio`.

## Submission Checklist

- [x] design.pdf
- [x] services.drawio
- [x] services.png
- [x] schema.drawio
- [x] schema.png
- [x] schema.sql
- [x] README.md

## Team Responsibilities

**Anurag Sharma (Leader):** team coordination and Identity & Administration.

**Mohit Tailor:** Catalogue Service.

**Harshita Rathore:** Order Service.

**Harendra Godara:** Payment Service.

All members review the integrated submission before final submission.
