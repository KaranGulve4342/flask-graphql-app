# Flask + GraphQL Microservice Server

A flexible, production-ready Flask + GraphQL server that can be easily adapted for any microservice by simply changing the schema configuration.

## 🎯 Features

- **Modular Schema Design**: Easy to customize for different databases and use cases
- **MongoDB Integration**: Out-of-the-box support for MongoDB
- **CORS Enabled**: Ready for cross-origin requests
- **Health Check Endpoints**: Monitor server and database status
- **Production Ready**: Can be easily deployed and hosted
- **Microservice Friendly**: Designed for easy integration into any architecture

## 📁 Project Structure

```
flask-graphql-app/
├── app.py              # Main Flask application
├── schema.py           # ⭐ GraphQL schema (CUSTOMIZE THIS)
├── database.py         # MongoDB connection handler
├── config.py           # Configuration management
├── requirements.txt    # Python dependencies
├── .env               # Environment variables
└── README.md          # Documentation
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Edit `.env` file with your database credentials:

```env
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
DB_NAME=graphql
COLLECTION_NAME=users
DEBUG=True
HOST=0.0.0.0
PORT=5000
```

### 3. Run the Server

```bash
python app.py
```

The server will start at `http://localhost:5000`

## 📝 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/graphql` | POST | GraphQL endpoint |
| `/health` | GET | Detailed health status |

## 🔧 Customizing for Your Microservice

### Step 1: Update the Schema (`schema.py`)

This is the **ONLY file** you need to modify to adapt the server for different databases!

**Example: Change from Users to Products**

```python
# In schema.py, replace the User class:

class Product(ObjectType):
    id = String()
    name = String()
    price = Float()
    category = String()
    stock = Int()

class Query(ObjectType):
    products = List(Product)
    product = Field(Product, id=String(required=True))
    
    def resolve_products(self, info):
        collection = db.get_collection('products')
        products_data = collection.find()
        
        return [
            Product(
                id=str(product['_id']),
                name=product.get('name'),
                price=product.get('price'),
                category=product.get('category'),
                stock=product.get('stock')
            )
            for product in products_data
        ]
```

### Step 2: Update Environment Variables

```env
COLLECTION_NAME=products  # Change collection name
```

That's it! Your server is now ready for the new schema.

## 📊 Example GraphQL Queries

### Query All Users

```graphql
{
  users {
    id
    name
    age
  }
}
```

### Query User by ID

```graphql
{
  user(id: "68f3b9087dfc3804c12c551b") {
    id
    name
    age
  }
}
```

### Search Users by Name

```graphql
{
  usersByName(name: "Alice") {
    id
    name
    age
  }
}
```

### Create a New User

```graphql
mutation {
  createUser(name: "John Doe", age: 30) {
    user {
      id
      name
      age
    }
  }
}
```

### Update a User

```graphql
mutation {
  updateUser(id: "68f3b9087dfc3804c12c551b", name: "Alice Smith", age: 29) {
    user {
      id
      name
      age
    }
  }
}
```

### Delete a User

```graphql
mutation {
  deleteUser(id: "68f3b9087dfc3804c12c551b") {
    success
  }
}
```

## 🌐 Testing with cURL

```bash
# Query all users
curl -X POST http://localhost:5000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ users { id name age } }"}'

# Create a user
curl -X POST http://localhost:5000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { createUser(name: \"Jane Doe\", age: 25) { user { id name age } } }"}'
```

## 🐳 Deployment Options

### Option 1: Deploy to Heroku

```bash
# Add Procfile
echo "web: python app.py" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

### Option 2: Deploy to Railway

1. Connect your GitHub repository
2. Add environment variables from `.env`
3. Deploy!

### Option 3: Deploy to AWS/GCP/Azure

Use Docker or traditional deployment methods with the provided configuration.

## 🔒 Production Considerations

1. **Environment Variables**: Never commit `.env` to version control
2. **Database Security**: Use strong credentials and connection encryption
3. **Rate Limiting**: Add rate limiting for production use
4. **Authentication**: Implement JWT or OAuth for protected endpoints
5. **Logging**: Add proper logging for monitoring and debugging

## 🛠️ Advanced Customization

### Adding Authentication

```python
# In app.py
from functools import wraps

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Add your auth logic here
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/graphql', methods=['POST'])
@require_auth
def graphql_server():
    # ... rest of the code
```

### Adding More Collections

```python
# In schema.py
class Query(ObjectType):
    users = List(User)
    products = List(Product)  # Add new types
    orders = List(Order)
    
    def resolve_products(self, info):
        collection = db.get_collection('products')
        # ... implementation
```

## 📚 Resources

- [GraphQL Documentation](https://graphql.org/)
- [Graphene Python](https://docs.graphene-python.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [MongoDB Documentation](https://docs.mongodb.com/)

## 🤝 Contributing

Feel free to customize and extend this server for your specific needs!

## 📄 License

MIT License - Use freely in your microservices!
