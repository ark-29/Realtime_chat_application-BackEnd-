FastAPI Real-Time Chat Backend

A Real-time chat backend system built using FastAPI, WebSockets and MySQL, featuring user registration, authentication, group chat management, and live messaging — entirely backend-driven with SQLModel ORM and bcrypt security.

### Features

*  User Registration & Login with hashed passwords (bcrypt)
*  Create and join chat groups
*  Real-time messaging via WebSockets
*  Persistent message storage in MySQL
*  SQLModel-based relational database design
*  Input validation with Pydantic
*  Token-less design (user_id-based authorization)
*  Tested entirely via Swagger UI — no frontend required

### Tech Stack

| Category                    | Technologies Used              |
| --------------------------- | ------------------------------ |
| **Backend Framework**       | FastAPI                        |
| **Database**                | MySQL (via SQLModel + PyMySQL) |
| **Authentication**          | bcrypt password hashing        |
| **Real-time Communication** | WebSockets                     |
| **Language**                | Python 3.x                     |


### Setup & Run Instructions

####  Install dependencies

--> in Requirements

####  Update database configuration

--> update database 

####  Run the server

uvicorn main:app --reload

#### Open Swagger UI

Access all APIs and test WebSocket endpoints via:

```
http://127.0.0.1:8000/docs
```

### API Endpoints

| Endpoint        | Method    | Description               |
| --------------- | --------- | ------------------------- |
| `/register`     | POST      | Register a new user       |
| `/login`        | POST      | Authenticate user         |
| `/create_group` | POST      | Create new chat group     |
| `/join_group`   | POST      | Join existing chat group  |
| `/all_groups`   | GET       | List all chat groups      |
| `/users`        | GET       | View all users            |
| `/protected`    | GET       | Verify user access        |
| `/ws/`          | WebSocket | Real-time group messaging |

---

### 🧠 Database Models

* **User** → id, name, email, password
* **Group** → id, name, code
* **UserGroup** → id, user_id, group_id
* **Message** → id, content, timestamp, sender_id, group_id

Each message is linked to a sender (User) and a group (Group).
Users can belong to multiple groups, and all messages are persisted in MySQL.

### Note
 * created tokens but never used in this application development, please ignore Jose from all codes

### 🤝 Author

**👨‍💻 Avanapu Abhiram**
📧 abhiramavanapu29@gmail.com
💼 [LinkedIn Profile](www.linkedin.com/in/avanapu-abhiram-krishna-a20aab371)
⭐ Don’t forget to star the repo if you found it useful!


Would you like me to include a **short 2-line project summary** for the GitHub repo sidebar (like the “About” section under the description)?
It’ll make your repo look polished and recruiter-friendly.
