# Expense Tracker API

Features
Here are the features that you should implement in your Expense Tracker API:

Sign up as a new user.
Generate and validate JWT tokens for handling authentication and user session.
List and filter your past expenses. You can add the following filters:
Past week
Past month
Last 3 months
Custom (to specify a start and end date of your choosing).
Add a new expense
Remove existing expenses
Update existing expenses

# Running the project

This project is built upon Docker and Docker-compose, running the following will do the work

    docker-compose up -d
To stop it
    
    docker-compose stop

To remove it
    
    docker-compose rm

If necessary it's possible to change the postgres connection, for this is just updating the .env.dev

For the DB_URL it's important to use the host as the name for the postgres container which is db as specified 
in the docker-compose. 

# APIS Endpoints
POST | /register | Creates a new user

Body
    
{
        "username":"new_user", 
        "password":"test"
    }

Responses

200 {
        "username":"new_user", 
        "password":"test"
    }

Curl example

    curl -d '{"username":"new_user", "password":"test"}' -H "Content-Type: application/json" -X POST base_url/register
    
POST | /login | Retrieves a new JWT token for the account
Body
 {
        "username":"new_user", 
        "password":"test"
    }
Responses

200 {
       "access_token": JWT_TOKEN
    }

    `curl -d '{"username":"new_user", "password":"test"}' -H "Content-Type: application/json" -X POST base_url/login`

POST | /expenses | Creates a new expense

Body
{ 
    "amount": 0, 
    "category_id": 2, 
    "expense_date": '13-09-2024', 
    "description": "Some description"
}

Responses

201, { 
    "id": 1,
    "amount": 0, 
    "category_id": 2, 
    "expense_date": '13-09-2024', 
    "description": "Some description"
}

400, {
    "msg": "Signature verification failed"
}

    `curl -d '{ "amount": 0, "category_id": 2, "expense_date": '13-09-2024', "description": "Some description"}' -H "Content-Type: application/json" -H "Authorization: Bearer TOKEN" -X POST base_url/expenses`

GET | /expenses | List expenses with pagination of 100 items per page

Query params
type = (past_week or past_month or last_3_months)
start_date = '2024-09-13'
end_date = '2024-09-20'
category_id = 1
page = 1

Responses

200, [{
    "id": 1,
    "amount": 0, 
    "category_id": 2, 
    "expense_date": '13-09-2024', 
    "description": "Some description"
}]

400, {
    "msg": "Signature verification failed"
}
    
    curl -H "Content-Type: application/json" -H "Authorization: Bearer TOKEN" -X GET 'base_url/expenses?type=last_3_months&category_id=2'

GET | /expenses/id | Get expense


Responses

200, {
    "id": 1,
    "amount": 0, 
    "category_id": 2, 
    "expense_date": '13-09-2024', 
    "description": "Some description"
}

400, {
    "msg": "Signature verification failed"
}

404, {
    "error": "Expense not found"
}

    curl -H "Content-Type: application/json" -H "Authorization: Bearer TOKEN" -X GET 'base_url/expenses/1'

DELETE | /expenses/id | Delete expense


Responses

204, {
}

400, {
    "msg": "Signature verification failed"
}

    curl -H "Content-Type: application/json" -H "Authorization: Bearer TOKEN" -X DELETE 'base_url/expenses/1'

PUT | /expenses/id | Get expense

All the arguments in the body are mandatory

Body
{ 
    "amount": 0, 
    "category_id": 2, 
    "expense_date": '13-09-2024', 
    "description": "Some description"
}

Responses

200, { 
    "amount": 0, 
    "category_id": 2, 
    "expense_date": '13-09-2024', 
    "description": "Some description"
}

400, {
    "msg": "Signature verification failed"
}

404, {
    "error": "Expense not found"
}

    curl  -d '{ "amount": 0, "category_id": 2, "expense_date": '13-09-2024', "description": "Some description"}' -H "Content-Type: application/json" -H "Authorization: Bearer TOKEN" -X PUT 'base_url/expenses/1'

PATCH | /expenses/id | Get expense

The arguments are optional, but the response will be determined by what it's passed

Body
{ 
    "amount": 0, 
    "category_id": 2, 
    "expense_date": '13-09-2024', 
    "description": "Some description"
}

Responses

200, { 
    "amount": 0, 
    "category_id": 2, 
    "expense_date": '13-09-2024', 
    "description": "Some description"
}

400, {
    "msg": "Signature verification failed"
}

404, {
    "error": "Expense not found"
}

    `curl  -d '{ "amount": 0, "category_id": 2, "expense_date": '13-09-2024', "description": "Some description"}' -H "Content-Type: application/json" -H "Authorization: Bearer TOKEN" -X PATCH 'base_url/expenses/1'`

POST|/categories|Creates a new category

Body
{ 
    "name": "Category name"
}

Responses 
201,
{
    "id": 1,
    "name": "Category name"
}

400, {
    "msg": "Signature verification failed"
}

    `curl -d '{"name":"category"}' -H "Content-Type: application/json" -H "Authorization: Bearer TOKEN" -X POST base_url/categories`


GET|/categories| List categories with pagination of 100 items per page

Query params
name = "category"
page = 1

Responses

200,
[{
    "id": id,
    "name": "category"
}]
400, {
    "msg": "Signature verification failed"
}


    `curl -H "Content-Type: application/json" -H "Authorization: Bearer TOKEN" -X GET base_url/categories`