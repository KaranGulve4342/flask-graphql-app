import graphene
from graphene import ObjectType, String, Int, List, Field, Mutation
from database import db
from bson import ObjectId


# ============================================================================
# CUSTOMIZE THIS SECTION FOR YOUR MICROSERVICE
# ============================================================================

class User(ObjectType):
    """
    User Type - Customize fields based on your database schema
    
    Example: For a Product database, you might change this to:
    class Product(ObjectType):
        id = String()
        name = String()
        price = Float()
        category = String()
    """
    id = String()
    name = String()
    age = Int()


class Query(ObjectType):
    """
    Query definitions - Customize based on your needs
    
    You can add more queries like:
    - get_user_by_email
    - search_users
    - get_users_by_age_range
    """
    
    # Get all users
    users = List(User)
    
    # Get user by ID
    user = Field(User, id=String(required=True))
    
    # Get users by name (example of custom query)
    users_by_name = List(User, name=String(required=True))
    
    def resolve_users(self, info):
        """Fetch all users from the database"""
        collection = db.get_collection('users')  # Change collection name as needed
        users_data = collection.find()
        
        return [
            User(
                id=str(user['_id']),
                name=user.get('name'),
                age=user.get('age')
            )
            for user in users_data
        ]
    
    def resolve_user(self, info, id):
        """Fetch a single user by ID"""
        collection = db.get_collection('users')  # Change collection name as needed
        
        try:
            user = collection.find_one({'_id': ObjectId(id)})
            if user:
                return User(
                    id=str(user['_id']),
                    name=user.get('name'),
                    age=user.get('age')
                )
        except Exception as e:
            print(f"Error fetching user: {e}")
            return None
    
    def resolve_users_by_name(self, info, name):
        """Fetch users by name (case-insensitive search)"""
        collection = db.get_collection('users')  # Change collection name as needed
        users_data = collection.find({'name': {'$regex': name, '$options': 'i'}})
        
        return [
            User(
                id=str(user['_id']),
                name=user.get('name'),
                age=user.get('age')
            )
            for user in users_data
        ]


class CreateUser(Mutation):
    """
    Mutation to create a new user
    
    Example: For a Product database, you might change this to:
    class CreateProduct(Mutation):
        class Arguments:
            name = String(required=True)
            price = Float(required=True)
            category = String()
    """
    
    class Arguments:
        name = String(required=True)
        age = Int(required=True)
    
    user = Field(User)
    
    def mutate(self, info, name, age):
        collection = db.get_collection('users')  # Change collection name as needed
        
        new_user = {
            'name': name,
            'age': age
        }
        
        result = collection.insert_one(new_user)
        
        return CreateUser(
            user=User(
                id=str(result.inserted_id),
                name=name,
                age=age
            )
        )


class UpdateUser(Mutation):
    """Mutation to update an existing user"""
    
    class Arguments:
        id = String(required=True)
        name = String()
        age = Int()
    
    user = Field(User)
    
    def mutate(self, info, id, name=None, age=None):
        collection = db.get_collection('users')  # Change collection name as needed
        
        update_data = {}
        if name is not None:
            update_data['name'] = name
        if age is not None:
            update_data['age'] = age
        
        try:
            collection.update_one(
                {'_id': ObjectId(id)},
                {'$set': update_data}
            )
            
            updated_user = collection.find_one({'_id': ObjectId(id)})
            
            if updated_user:
                return UpdateUser(
                    user=User(
                        id=str(updated_user['_id']),
                        name=updated_user.get('name'),
                        age=updated_user.get('age')
                    )
                )
        except Exception as e:
            print(f"Error updating user: {e}")
            return None


class DeleteUser(Mutation):
    """Mutation to delete a user"""
    
    class Arguments:
        id = String(required=True)
    
    success = graphene.Boolean()
    
    def mutate(self, info, id):
        collection = db.get_collection('users')  # Change collection name as needed
        
        try:
            result = collection.delete_one({'_id': ObjectId(id)})
            return DeleteUser(success=result.deleted_count > 0)
        except Exception as e:
            print(f"Error deleting user: {e}")
            return DeleteUser(success=False)


class Mutations(ObjectType):
    """
    Root Mutations - Add your custom mutations here
    """
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()


# Create the schema
schema = graphene.Schema(query=Query, mutation=Mutations)

# ============================================================================
# END OF CUSTOMIZATION SECTION
# ============================================================================
