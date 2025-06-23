# Moodle App
This project is a Moodle web application designed using web services.

## Features
- Course and content management
- Login with JWT, roles (student, teacher, admin)
- Course content upload stored in MongoDB
- CRUD operations

# Architecture
1. Academia - stores student, teacher and lecture data in a MariaDB container. Handles user - course relation.
2. Materials - stores lecture content / materials in a MongoDB container.
3. IDM - authentication service implemented with gRPC and Redis for blacklisting JWT's. 
## Technologies
React

FastAPI - RESTful services

gRPC

MariaDB, MongoDB

Docker, Docker-Compose

Redis