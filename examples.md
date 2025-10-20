# Example GraphQL Queries and Mutations

## Queries

### 1. Get All Users
```json
{
  "query": "{ users { id name age } }"
}
```

### 2. Get User by ID
```json
{
  "query": "{ user(id: \"68f3b9087dfc3804c12c551b\") { id name age } }"
}
```

### 3. Search Users by Name
```json
{
  "query": "{ usersByName(name: \"Alice\") { id name age } }"
}
```

## Mutations

### 1. Create User
```json
{
  "query": "mutation { createUser(name: \"Bob Smith\", age: 35) { user { id name age } } }"
}
```

### 2. Update User
```json
{
  "query": "mutation { updateUser(id: \"68f3b9087dfc3804c12c551b\", name: \"Alice Johnson Updated\", age: 30) { user { id name age } } }"
}
```

### 3. Delete User
```json
{
  "query": "mutation { deleteUser(id: \"68f3b9087dfc3804c12c551b\") { success } }"
}
```

## Using Variables (Recommended)

### Query with Variables
```json
{
  "query": "query GetUser($userId: String!) { user(id: $userId) { id name age } }",
  "variables": {
    "userId": "68f3b9087dfc3804c12c551b"
  }
}
```

### Mutation with Variables
```json
{
  "query": "mutation CreateUser($name: String!, $age: Int!) { createUser(name: $name, age: $age) { user { id name age } } }",
  "variables": {
    "name": "Charlie Brown",
    "age": 28
  }
}
```

## cURL Examples

### Query All Users
```bash
curl -X POST http://localhost:5000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ users { id name age } }"}'
```

### Create User
```bash
curl -X POST http://localhost:5000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { createUser(name: \"David Lee\", age: 42) { user { id name age } } }"}'
```

### Update User
```bash
curl -X POST http://localhost:5000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { updateUser(id: \"YOUR_USER_ID\", age: 29) { user { id name age } } }"}'
```

## Testing with Postman

1. Set method to **POST**
2. URL: `http://localhost:5000/graphql`
3. Headers: `Content-Type: application/json`
4. Body (raw JSON):
   ```json
   {
     "query": "{ users { id name age } }"
   }
   ```

## Testing with GraphiQL or GraphQL Playground

If you want to use a GraphQL IDE, you can install GraphiQL:

```bash
pip install flask-graphql
```

Then update `app.py`:
```python
from flask_graphql import GraphQLView

app.add_url_rule(
    '/graphiql',
    view_func=GraphQLView.as_view('graphiql', schema=schema, graphiql=True)
)
```

Visit `http://localhost:5000/graphiql` for an interactive GraphQL IDE!
