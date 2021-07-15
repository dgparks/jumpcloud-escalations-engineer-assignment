import jcapiv2
from jcapiv2.rest import ApiException
from pprint import pprint
import demo_org_config

# 
API_KEY = demo_org_config.API_KEY

# Set up the configuration object with your API key for authorization
configuration = jcapiv2.Configuration()
configuration.api_key['x-api-key'] = API_KEY

# headers
content_type = "application/json"
accept = "application/json"
x_org_id = ''

# Users
demo_users = [
    {
        'email': 'arthur.schopenhauer@jumpcloud.com',
        'firstname': 'Arthur',
        'lastname': 'Schopenhauer',
        'username': 'arthur.schopenhauer',
        'password': 'SkyFall_1860@'
        'activated': True
    },
        {
        'email': 'soren.kierkegaard@jumpcloud.com',
        'firstname': 'Soren',
        'lastname': 'Kierkegaard',
        'username': 'soren.kierkegaard',
        'password': 'SkyFall_1855!'
        'activated': True
    }
]

def main():
    get_user_groups()
    create_and_activate_users(demo_users)
    create_user_group('Philosophers')
    bind_user_to_resource()

def get_user_groups():
    """Make an API call to retrieve all user groups."""
    api_instance = jcapiv2.UserGroupsApi(jcapiv2.ApiClient(configuration))
    try:
        user_groups = api_instance.groups_user_list(content_type, accept)
        print(user_groups)
    except ApiException as err:
        print("Exception when calling UserGroupsApi->groups_user_list: %s\n" % err)

def create_and_activate_users(users):
    """
    Make an API call to create and activate a list of new users.
    :param users: a list of users
    """
    api_instance = jcapiv2.BulkJobRequestsApi(jcapiv2.ApiClient(configuration))
    body = [jcapiv2.BulkUserCreate(user_list)]
    try:
        # Bulk Users Create
        api_response = api_instance.bulk_users_create(content_type, accept, body=body, x_org_id=x_org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling BulkJobRequestsApi->bulk_users_create: %s\n" % e)

def create_user_group(display_name):
    """Make an API call to create a new user group."""
    api_instance = jcapiv2.UserGroupsApi(jcapiv2.ApiClient(configuration))
    body = jcapiv2.UserGroupPost(display_name)
    try:
        # Create a new User Group
        api_response = api_instance.groups_user_post(content_type, accept, body=body, x_org_id=x_org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling UserGroupsApi->groups_user_post: %s\n" % e)

def bind_user_to_resource(user_id, resource_id):
    # create an instance of the API class
    api_instance = jcapiv2.GraphApi(jcapiv2.ApiClient(configuration))
    body = jcapiv2.UserGraphManagementReq({
        'id': resource_id
    })
    try:
        # Manage the associations of a User
        api_instance.graph_user_associations_post(user_id, content_type, accept, body=body, x_org_id=x_org_id)
    except ApiException as e:
        print("Exception when calling GraphApi->graph_user_associations_post: %s\n" % e)

if __name__ == "__main__":
    main()