# 🍽️ CampusEats

**Design Benchmark** · CS 543 — Web Services · `Group 16`

---

## Team Members

| Name                 | Roll Number | GitHub                                                 | Role       | Service                   |
| -------------------- | ----------- | ------------------------------------------------------ | ---------- | ------------------------- |
| **Anurag Sharma**    | 20251651027 | [@anuragsharma-01](https://github.com/anuragsharma-01) | **Leader** | Identity & Administration |
| **Mohit Tailor**     | 20251651058 | [@mohit-taylor](https://github.com/mohit-taylor)                                        | Member     | Catalogue                 |
| **Harshita Rathore** | 20251651043 | [@harendra-godara](https://github.com/harendra-godara)                                      | Member     | Order                     |
| **Harendra Godara**  | 20251651041 | [@harshitarathore768](https://github.com/harshitarathore786)                                           | Member     | Payment                   |

---

## Repository Architecture

```text
campuseats/
│
├── README.md                     ← you are here
├── .gitignore
│
├── Assignment1/                  HTTP basics & mock API
│   ├── README.md                 write-up
│   ├── brief.md                  system brief
│   ├── http-log.md               HTTP request/response log
│   └── network-analysis.md       DevTools network analysis
│
├── Assignment2/                  Service design benchmark
│   ├── README.md                 write-up
│   ├── design.pdf                capabilities, contracts, placeOrder & validation
│   ├── services.drawio           editable service design
│   ├── services.png              service design diagram
│   ├── schema.drawio             editable database schema
│   ├── schema.png                database schema diagram
│   └── schema.sql                CREATE TABLE statements
│
└── docs/
```

---

## Assignments

| #     | Assignment                                                                          | Covers                                                                                    |
| ----- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| **1** | [Assignment 1](https://github.com/anuragsharma-01/campuseats/tree/main/Assignment1) | System brief, mock REST API, HTTP logging, network analysis                               |
| **2** | [Assignment 2](https://github.com/anuragsharma-01/campuseats/tree/main/Assignment2) | Capabilities, service decomposition, contracts, `placeOrder`, database schema, validation |

---

## Assignment 2 — Service Responsibilities

| Service                               | Responsible Member         | Data Owned                                                                 |
| ------------------------------------- | -------------------------- | -------------------------------------------------------------------------- |
| **Identity & Administration Service** | **Anurag Sharma — Leader** | Users, Roles, Food Provider profiles, Administrator access                 |
| **Catalogue Service**                 | **Mohit Tailor**           | Restaurants, Menus, Food Items, Categories, Availability, Pickup Locations |
| **Order Service**                     | **Harshita Rathore**       | Orders, Order Items, Order Status, Order Pickup selections                 |
| **Payment Service**                   | **Harendra Godara**        | Payments, Payment Status, Payment Transactions                             |

---

## Contributors

* **Anurag Sharma** — Team Leader
* **Mohit Tailor** — Team Member
* **Harshita Rathore** — Team Member
* **Harendra Godara** — Team Member

---

Indian Institute of Information Technology, Vadodara · Semester 3
