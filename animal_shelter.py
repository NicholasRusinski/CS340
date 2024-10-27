from pymongo import MongoClient

# crud class for AAC mongo DB

# author Nicholas Rusinski 
# created 10-01-24
# added crud functionality for mongo DB AAC databse

# updated 10-07-24
# added password arguments to handled at isntaitation

# updated 10-19-24
# added functionality to handle mlti valued queries

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, username, password):
        # Connection Variables
        USER = username
        PASS = password
        HOST = 'nv-desktop-services.apporto.com'
        PORT = 30743
        DB = 'AAC'
        COL = 'animals'

        # Initialize Connection
        self.client = MongoClient(f'mongodb://{USER}:{PASS}@{HOST}:{PORT}')
        self.database = self.client[DB]
        self.collection = self.database[COL]
       
    # Create method to implement the C in CRUD.
    def create(self, data):
        try:
            insert_result = self.collection.insert_one(data)  # data should be a dictionary
            return insert_result.inserted_id
        except Exception as e:
            print(f"error inserting document: {e}")
            return False
        
    # updated read method to handle large multi valued queries 
    def read(self, query=None):
        try:
            # takes query dictionary item
            if query is not None:
                cursor = self.collection.find(query)
            else:
                cursor = self.collection.find()

            return list(cursor)  

        except Exception as e:
            print(f"error reading animals with query '{query}': {e}")
            return []
        
    # update method for mongo DB    
    def update(self, query_key, query_value, update_data, update_many=False):
        try:
            
            #define query
            query = {query_key: query_value}
            
            # update one or many
            if update_many:
                result = self.collection.update_many(query, {'$set': update_data})
            else:
                result = self.collection.update_one(query, {'$set': update_data})

            # part of the mongo upade object that access how many items were updated 
            return result.modified_count

        except Exception as e:
            print(f"error updating documents: {e}")
            return 0  
        
    # delete crud method
    def delete(self, query_key, query_value, delete_many=False):
        try:
            #define query
            query = {query_key: query_value}

            # delete one or many
            if delete_many:
                result = self.collection.delete_many(query)
            else:
                result = self.collection.delete_one(query)

            # part of the mongo upade object that access how many items were updated 
            if result.deleted_count == 0:
                print("Nothong to delete")
            
            return result.deleted_count

        except Exception as e:
            print(f"error deleting documents: {e}")
            return 0  # Return 0 in case of error