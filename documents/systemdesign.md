# System Design

Welcome to the system design document for Data Processing Assignment. This document serves as a comprehensive guide detailing the architecture, components, and functionalities of the system. It aims to provide a clear understanding of the design choices, technical specifications, and implementation strategies involved in building and maintaining our frontend and API for the Netflix Usecase.

Within these pages, you'll discover an in-depth exploration of the system's objectives, scope, and key features. Additionally, this document outlines the interactions between various modules and security measures employed to ensure the robustness and reliability of our system.

## Architecture Design

```mermaid
flowchart LR
    api["API"]
    db[("PostgreSQL")]
    fe["Frontend"]
    api<-- SQL -->db
    fe<-- JSON, XML -->api
```

## Backups

For backups we suggest following the 3-2-1 rule. That means.

+ 3 Copies of Data – Have three copies of data
+ 2 Different Media – Use two different media types for storing the data.
+ 1 Copy Offsite – Keep one copy offsite to prevent the possibility of data loss due to a site-specific failure.

We have created two scripts to help with the backup and restore process.
These create/restore a snapshot of the database, and are called ```backup.sh``` and ```restore.sh```.

The number of backups stored should be minimized. The retention period for the stored backups should also be minimized.
Our advice is to not keep backup files for longer then 1 month.

## API

The API will function as a middleman system between the front-end and the database and will satisfy at least the following conditions:

#### Framework Choice

Our project team decided to use Flask because a member of our team had some experience with Flask. Additionally, making an API in Python just sounded nice.

#### External Integration

As we are making an Netflix API, we decided that it's only fitting to use a public movie API to display additional information about the movies.

#### Data Handling

Clients using the API have the choice to request JSON or XML data using the ```Accept:``` HTTP header.

#### Endpoints and Response Handling

The comprehensive openapi specifications of the endpoints can be found at ```/api/v1/docs``` when connected to the web server.

#### Database Interaction

The API connects to the database with psycopg using a connection string.

#### Security and Authentication

User password are stored in the database in a hashed and salted format. The user privileges are managed by the database making it harder to access privileged information by accident.

We implemented an interesting way to handle user sessions. That we consider secure by our threat model.
We decided to go this route because we wanted to maintain the user roles in the DBMS for extra security.

When the user logs in, their input is validated. We only accept letters, numbers, and underscores in both password and username. This reduces the possible password complexity but that can be mitigated by using longer passwords. The login information is then encrypted on the server and stored in the JWT token, this is used as a unique identity because we had to work around multithreading, and this was the fastest to implement solution that we have identified. This might sound insecure but here's the reason why why think it's not. First and foremost, in a production environment the requests would be protected by TLS when it transit. The JWT token protects against modifying it's contents, and the login information is encrypted.

In our view, the only way to recover the password is to either, have access to the server or to have full access to the user's computer and log their inputs. That, for us is out of our scope.

To demonstrate here's an example of a JWT token.

```{"alg":"HS256","typ":"JWT"}{"fresh":false,"iat":1705842060,"jti":"17d4bace-eee4-4921-addc-dfc4a584939e","type":"access","sub":"{\"nonce\": \"dScKqOy0cUY=\", \"ciphertext\": \"D24w/JfHdOFXjEDMttJ90Q==\"}","nbf":1705842060,"csrf":"3864eba3-e0d9-4822-86e4-7bc22471698e","exp":1705845660}```

Here, ```sub``` contains the encrypted information.

```{"nonce": "dScKqOy0cUY=", "ciphertext": "D24w/JfHdOFXjEDMttJ90Q=="}```

Please, feel free to decode the above strings with base64, and see for yourself that we are not leaking information.

### Class Diagram

![Class Diagram](Class_Diagram.jpg "Class Diagram")

## Database

We decided to use PostgreSQL for our database because none in our team had any experience with it, wanted to try a relational database other than MySQL, and because it's popular/commonly used.

### Entity Relationship Diagram (ERD)

![ERD](erd.jpg "ERD")

### Views, stored procedures, triggers, functions
For this project we have used extensively several elements of postgres which allow to prebuilt queries. Mostly functions and stored procedures were implemented for the APIs.

Most of the prebuilt queries are functions and stored procedures. The reason why this was chosen is because functions over views or stored procedures is because functions have several advantages over views and stored procedures, at least in the cases that they were used.

One of the main advantage of a function over a view is that a function can accept parameters, while the view cant. This means that functions are clearly better in cases where a specific piece of data needs to be extracted, such as the age of a specific profile (because the id is provided as a parameter, which views cant accept). However, some of the postgres functions that were created do not have any parameters. They could be replaced with a view, however for the sake of standardization, functions were still implemented.

For our case the triggers are not really helpful. Triggers trigger whenever a specific event occurs such as select query. This functionality is not needed for the sake of the project. One of the main reasons is that the database api user has no rights to execute queries on the tables(for data security and integrity), the api user can only execute functions and that would make the trigger redundant.

Stored procedures are used but not that extensively. Compared to functions they do not have a return value of any sort, which makes them useful for queries which change the database, but not the ones which extract information. Thus they are used for insert and update queries.
