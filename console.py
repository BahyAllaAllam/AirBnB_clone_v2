#!/usr/bin/python3
"""This module defines the HBNBCommand class,
        a command interpreter for HBNB project."""

import cmd
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models import storage
import sys
from os import getenv

storage_type = getenv("HBNB_TYPE_STORAGE")


class HBNBCommand(cmd.Cmd):
    """Command interpreter class."""

    prompt = "(hbnb) "
    classes = ("BaseModel", "User", "State", "City",
               "Amenity", "Place", "Review")

    def emptyline(self):
        """Do nothing on empty input line"""
        pass

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """Exit the program with EOF (Ctrl+D)"""
        print()
        return True

    def do_create(self, arg):
        """Create command to create a new instance of BaseModel"""
        if not arg:
            print("** class name missing **")
            return
        args = arg.split()
        class_name = args[0]

        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        param_dict = {}
        for a in args[1:]:
            if '=' in a:
                key, value = a.split('=')
                if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
                    value = value[1:-1].replace('_', ' ').replace('\\"', '"')
                elif '.' in value:
                    try:
                        value = float(value)
                    except ValueError:
                        pass
                else:
                    try:
                        value = int(value)
                    except ValueError:
                        pass
                param_dict[key] = value

        new_instance = eval(class_name)()
        for key, value in param_dict.items():
            setattr(new_instance, key, value)

        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """Show command to print string representation of an instance"""
        arg_list = arg.split()
        if not arg_list:
            print("** class name missing **")
            return

        class_name = arg_list[0]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        if len(arg_list) < 2:
            print("** instance id missing **")
            return

        obj_id = arg_list[1]
        obj_key = "{}.{}".format(class_name, obj_id)
        all_objs = storage.all()
        if obj_key not in all_objs:
            print("** no instance found **")
            return
        else:
            print(all_objs[obj_key])

    def do_destroy(self, arg):
        """Destroy command to delete an instance"""
        if not arg:
            print("** class name missing **")
            return

        arg_list = arg.split()
        class_name = arg_list[0]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        if len(arg_list) < 2:
            print("** instance id missing **")
            return

        obj_id = arg_list[1]
        obj_key = "{}.{}".format(class_name, obj_id)
        all_objs = storage.all()
        if obj_key not in all_objs:
            print("** no instance found **")
        else:
            del all_objs[obj_key]
            storage.save()

    def do_all(self, arg):
        """All command to print string representation of all instances"""
        all_objs = storage.all()
        if arg:
            arg_list = arg.split()
            class_name = arg_list[0]
            if class_name not in self.classes:
                print("** class doesn't exist **")
                return

            print([str(obj) for key, obj in all_objs.items() if key.startswith(
                    arg + ".")])
        else:
            print([str(obj) for obj in all_objs.values()])
            return

    def do_update(self, arg):
        """Update command to update an instance attribute"""
        if not arg:
            print("** class name missing **")
            return

        arg_list = arg.split()
        class_name = arg_list[0]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        if len(arg_list) < 2:
            print("** instance id missing **")
            return

        obj_id = arg_list[1]
        obj_key = "{}.{}".format(class_name, obj_id)
        all_objs = storage.all()
        if obj_key not in all_objs:
            print("** no instance found **")
            return

        if len(arg_list) < 3:
            print("** attribute name missing **")
            return

        if len(arg_list) < 4:
            print("** value missing **")
            return

        try:
            obj = all_objs[obj_key]
            attr_name = arg_list[2]
            attr_value = arg_list[3]
            if hasattr(obj, attr_name):
                attr_type = type(getattr(obj, attr_name))
                if attr_type is int:
                    attr_value = int(attr_value)
                elif attr_type is float:
                    attr_value = float(attr_value)
            setattr(obj, attr_name, attr_value)
            obj.save()
        except AttributeError:
            print("** attribute doesn't exist **")
        except ValueError:
            print("** invalid value for attribute type **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
