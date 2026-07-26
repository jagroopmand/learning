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


class PRGraph:
    def __init__(self):
        iam_graph_data = [
            ("tech", "engineer", {"constraints": {"min_trust_score": 85, "requires_mfa": True}, "permissions": ("RO",)}),
            ("engineer", "senior_engineer", {"constraints": {}, "permissions": ()}),
            ("senior_engineer", "contractor", {"constraints": {}, "permissions": ()}),
        ]



        {
            'tech':{
                'engineer': {'constraints': {}, 'permissions': {}}
            },
            'engineer': {
                      'contractor': {'constraints': {}, 'permissions': {}},
                      'repoA': {'constraints': 'RO', 'permissions': {'min_trust_score': 85, 'requires_mfa': True}},
                      'repoB': {'constraints': 'RW', 'permissions': {'min_trust_score': 85, 'requires_mfa': True}}
            },
            'senior_engineer': {
                'engineer': {'constraints': {}, 'permissions': {}}
            }, 
            'contractor': {},
            'repoA': {},
            'repoB': {}
        }