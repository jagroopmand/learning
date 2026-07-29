
from pprint import pprint

class CheckPermissions:
     def __init__(self, data:list):
        self.permissions_map = {}
        self.intialize(data)
       
  
     def intialize(self, data: list):
         for user, resource, permissions in data:
             if user not in self.permissions_map:
                 self.permissions_map[user] = {}
             self.permissions_map[user][resource] = permissions 
        
     
     def is_allowed(self, user: str, resource:str, action:str) -> bool:
         # check if user or resource is not in the pemrissions graph
         print("user: ", user)
         print("resource: ", resource)
         pprint(self.permissions_map[user])
         permissions = self.permissions_map[user][resource]
         pprint(permissions)
         if action in permissions:
             return True

         return False 


if __name__ == "__main__":

    auth_data = [
       ("u1", "r1", {"permissions": ("r","w")}), 
       ( "u1","r2", {"permissions": ("r")})
    ]


    obj = CheckPermissions(auth_data)

    pprint(obj.permissions_map)

    if obj.is_allowed("u1", "r1", "r"):
        print("pass")

    if not obj.is_allowed("u1", "r2", "w"):
        print("pass")

    if not obj.is_allowed("u10", "r2", "w"):
        print("pass")






