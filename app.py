"""
Flask + GraphQL Server
----------------------
Main application file - Minimal changes needed when adapting for different microservices.
Just ensure your schema.py is properly configured.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from graphql.execution import ExecutionResult
from schema import schema
from database import db
from config import Config

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Connect to database
db.connect()


@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({
        'status': 'running',
        'message': 'Flask + GraphQL Server is running!',
        'endpoints': {
            'graphql': '/graphql (POST)',
            'health': '/ (GET)'
        }
    })


@app.route('/graphql', methods=['POST'])
def graphql_server():
    """
    GraphQL endpoint
    
    Example queries:
    
    Query all users:
    {
      users {
        id
        name
        age
      }
    }
    
    Query user by ID:
    {
      user(id: "68f3b9087dfc3804c12c551b") {
        id
        name
        age
      }
    }
    
    Create user:
    mutation {
      createUser(name: "John Doe", age: 30) {
        user {
          id
          name
          age
        }
      }
    }
    """
    try:
        data = request.get_json()
        
        query = data.get('query')
        variables = data.get('variables', {})
        
        result = schema.execute(
            query,
            variables=variables,
            context_value=request
        )
        
        response = {}
        
        if result.data:
            response['data'] = result.data
        
        if result.errors:
            response['errors'] = [str(error) for error in result.errors]
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'errors': [str(e)]
        }), 400


@app.route('/health', methods=['GET'])
def health():
    """Detailed health check"""
    try:
        # Test database connection
        db.get_collection().find_one()
        db_status = 'connected'
    except Exception as e:
        db_status = f'error: {str(e)}'
    
    return jsonify({
        'status': 'healthy',
        'database': db_status,
        'config': {
            'db_name': Config.DB_NAME,
            'collection': Config.COLLECTION_NAME
        }
    })


if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Starting Flask + GraphQL Server")
    print("=" * 60)
    print(f"Database: {Config.DB_NAME}")
    print(f"Collection: {Config.COLLECTION_NAME}")
    print(f"Host: {Config.HOST}:{Config.PORT}")
    print("=" * 60)
    print("\n📝 Example GraphQL Query:")
    print("""
    POST http://localhost:5000/graphql
    Content-Type: application/json
    
    {
      "query": "{ users { id name age } }"
    }
    """)
    print("=" * 60)
    
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
