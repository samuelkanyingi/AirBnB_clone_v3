#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """serializes instances to a JSON file & deserializes back to instances"""

    # string - path to the JSON file
    __file_path = "file.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """returns the dictionary __objects"""
        if cls is not None:
            new_dict = {}
            for key, value in FileStorage.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return FileStorage.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            FileStorage.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        json_objects = {}
        for key in FileStorage.__objects:
            json_objects[key] = self.__objects[key].to_dict()
        with open(FileStorage.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(FileStorage.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                FileStorage.__objects[key] = (
                        classes[jo[key]["__class__"]](**jo[key])
                        )
        except Exception as e:
            pass

    def delete(self, obj=None):
        """delete obj from __objects if it’s inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in FileStorage.__objects:
                del FileStorage.__objects[key]

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()

    def get(self, cls, id):
        """ retrieves one object """
        if cls and id:
            key = ""
            if isinstance(cls, str):
                key = "{}.{}".format(cls, id)
            else:
                if cls.__name__ in classes.keys():
                    # create key
                    key = "{}.{}".format(cls.__name__, id)
            # search key
            if key in FileStorage.__objects.keys():
                return FileStorage.__objects[key]
        return None

    def count(self, cls=None):
        """ method to count the number of objects in storage"""
        if cls is None:
            return len(FileStorage.__objects)
        elif isinstance(cls, str):
            cls = classes.get(cls)
            return len(self.all(cls))
        else:
            return len(self.all(cls))
