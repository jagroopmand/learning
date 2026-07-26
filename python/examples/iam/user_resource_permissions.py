'''
permissions_map = [
   ( "user1", "resourceA", {"permissions" : ("R", "W)}),
   ( "user1", "resourceB", {"permissions" : ("R")}),
   ( "user2", "resourceA", {"permissions" : ("W)}),
   ( "user2", "resourceB", {"permissions" : ("R", "W)})
]
'''
import logging
class UserRespourcePermissions:
    def __init__(self, data: list = None):
        data = data if data is not None else []
        self.logger = logging.getLogger(__name__)
        self._permissions_map = {}
        self.build_permissions_map(data)


    def build_permissions_map(self, data: list) -> None:
        if not data:
            self.logger.warning("permissions_map is empty")

        for user,resource,permissions in data: 
            if user not in self._permissions_map:
                self._permissions_map[user] = {}    
            self._permissions_map[user][resource] = permissions


    def check_permission(self, user:str, resource:str, permission:str) -> bool:
        if user not in self._permissions_map:
            self.logger.debug("user: %s not found in permissions_map", user)
            return False

        if resource not in self._permissions_map[user]:
            self.logger.debug("resource: %s not found for user: %s in permissions_map", resource, user)
            return False

        return permission in self._permissions_map[user][resource]["permissions"]



if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

    permissions_data = [
        ("user1", "resourceA", {"permissions" : ['R', 'W']}),
        ( "user1", "resourceB", {"permissions" : ['R']}),
        ( "user2", "resourceA", {"permissions" : ['W']}),
        ( "user2", "resourceB", {"permissions" : ['R', 'W']})
    ]

    permissions_obj = UserRespourcePermissions(permissions_data)
    # permissions_obj.logger.debug("permissions_data: %s", permissions_obj._permissions_map)

    permitted = permissions_obj.check_permission("user1", "resourceA", "W")
    permissions_obj.logger.info("permission for user1 on resourceA: %s", permitted)

    permitted = permissions_obj.check_permission("user1", "resourceB", "W")
    permissions_obj.logger.info("permission for user1 on resourceB: %s", permitted)


    permitted = permissions_obj.check_permission("user2", "resourceB", "R")
    permissions_obj.logger.info("permission for user2 on resourceB: %s", permitted)

    permitted = permissions_obj.check_permission("user2", "resourceC", "W")
    permissions_obj.logger.info("permission for user2 on resourceC: %s", permitted)
