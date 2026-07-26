from collections import deque
import logging
class PRGraph:
    def __init__(self, data: dict={}):
        self._access_records = {}
        self.logger = logging.getLogger(__name__)
        self.initialize(data)

    def  initialize(self, data):
        self._access_records = data

    def build_permissions_set(self, user_group) -> set:
        grants = set()
        grants.update(self._access_records[user_group]["grants"])
        denies = set()
        denies.update(self._access_records[user_group]["denies"])

        visited = list()
        final_permissions = set()
        queue = deque(self._access_records[user_group].get("parents", []))

        if "parents" in self._access_records[user_group]:
           while queue:
                parent = queue.popleft()
                self.logger.debug("====================")
                self.logger.debug("visiting parent: %s", parent)
                if parent not in visited:
                    parent_grants = self._access_records[parent]["grants"]  
                    self.logger.debug("parent_grants:: %s", parent_grants)
                    grants.update(parent_grants)
        
                    parent_denies = self._access_records[parent]["denies"]
                    self.logger.debug("parent_denies:: %s", parent_denies)
                    denies.update(parent_denies)    

                    if "parents" in self._access_records[parent]:
                        queue.extend(self._access_records[parent]["parents"])
                    visited.append(parent)
        else: 
              self.logger.debug("group: %s has no parents", user_group)

        for grant in grants:
            if grant not in denies:
                final_permissions.add(grant)
        return final_permissions        
    
    def check_permissions(self, user_group:str ) -> set:
        if user_group in self._access_records:
            return self.build_permissions_set(user_group)
        else:
            self.logger.debug("group: %s missing from access data:", user_group)
            return set()
            
    def list_permissions(self, user_groups: list) -> set:
        permissions_list = set() 
        for group in user_groups:
            permissions_list.update(self.check_permissions(group))
        return permissions_list

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    access_data = {
       "eng": {"grants": {"read_repo"}, "denies": {}},
       "senior_eng": {"grants": {"merge_pr"}, "denies": {}, "parents": ["eng"]},
       "contractor": {"grants": {}, "denies": {"merge_pr"}, "parents": ["senior_eng"]}
    } 
    prgraph_obj = PRGraph(access_data)
    user_group_membership = ["contractor"]
    permissions = prgraph_obj.list_permissions(user_group_membership)
    prgraph_obj.logger.info("permissions for user_groups: %s = %s", user_group_membership,  permissions)


'''
Input:
groups = {
  "eng": {grants: {"read_repo"}, denies: {}},
  "senior_eng": {grants: {"merge_pr"}, denies: {}, parents: ["eng"]},
  "contractor": {grants: {}, denies: {"merge_pr"}, parents: ["senior_eng"]}
}
user_groups = ["contractor"]

Output: {"read_repo"}   // merge_pr denied despite inheriting it

'''