import jcapiv1, jcapiv2
from jcapiv1.rest import ApiException
from jcapiv2.rest import ApiException
from pprint import pprint
import demo_org_config

# Set up the configuration object with API key for authorization
API_KEY = demo_org_config.API_KEY
configurationv1 = jcapiv1.Configuration()
configurationv1.api_key['x-api-key'] = API_KEY
configuration = jcapiv2.Configuration()
configuration.api_key['x-api-key'] = API_KEY

# common request headers
content_type = "application/json"
accept = "application/json"
x_org_id = ''

# users
demo_users = [
    {
        'email': 'arthur.schopenhauer@dgparks.io',
        'firstname': 'Arthur',
        'lastname': 'Schopenhauer',
        'username': 'arthur.schopenhauer',
        'password': 'SkyFall_1860@',
        'activated': True
    },
        {
        'email': 'soren.kierkegaard@dgparks.io',
        'firstname': 'Soren',
        'lastname': 'Kierkegaard',
        'username': 'soren.kierkegaard',
        'password': 'SkyFall_1855!',
        'activated': True
    }
]

def main():

    # Create and activate 2 Users
    create_and_activate_users(demo_users)

    # Create a Group of Users
    create_user_group('Philosophers')

    # Get User and Group Ids
    schopenhauer_id = get_user_id_by_username('arthur.schopenhauer')
    kierkegaard_id = get_user_id_by_username('soren.kierkegaard')
    philosophers_id = get_user_group_id_by_name('Philosophers')

    # Associate Users to User Group
    bind_user_to_user_group(schopenhauer_id, philosophers_id)
    bind_user_to_user_group(kierkegaard_id, philosophers_id)

    # Associate one User to the recently added system in JumpCloud
    my_macbook_id = get_device_id_by_name('Eos-256X.local')
    bind_user_to_device(schopenhauer_id, my_macbook_id)


"""
dP     dP .d88888b   88888888b  888888ba  .d88888b  
88     88 88.    "'  88         88    `8b 88.    "' 
88     88 `Y88888b. a88aaaa    a88aaaa8P' `Y88888b. 
88     88       `8b  88         88   `8b.       `8b 
Y8.   .8P d8'   .8P  88         88     88 d8'   .8P 
`Y88888P'  Y88888P   88888888P  dP     dP  Y88888P  
oooooooooooooooooooooooooooooooooooooooooooooooooooo
"""

def create_and_activate_users(users):
    api_instance = jcapiv2.BulkJobRequestsApi(jcapiv2.ApiClient(configuration))
    try:
        # Bulk Users Create
        api_response = api_instance.bulk_users_create(content_type, accept, body=users, x_org_id=x_org_id)
        print_bulk_job_results(api_response.job_id)
    except ApiException as e:
        print("Exception when calling BulkJobRequestsApi->bulk_users_create: %s\n" % e)

def get_users():
    api_instance = jcapiv1.SystemusersApi(jcapiv1.ApiClient(configurationv1))
    try:
        # List all system users
        return api_instance.systemusers_list(content_type, accept, x_org_id=x_org_id)
    except ApiException as e:
        print("Exception when calling SystemusersApi->systemusers_list: %s\n" % e)

def get_user_id_by_username(username):
    for user in get_users().results:
        if user.username == username:
            return user._id
    return None

def get_user_associations(user_id):
    api_instance = jcapiv2.GraphApi(jcapiv2.ApiClient(configuration))
    targets = ['system']
    try:
        # List the associations of a User
        api_response = api_instance.graph_user_associations_list(user_id, content_type, accept, targets, x_org_id=x_org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GraphApi->graph_user_associations_list: %s\n" % e)

# helper method for returning information from create_and_activate_users()
def print_bulk_job_results(job_id):
    api_instance = jcapiv2.BulkJobRequestsApi(jcapiv2.ApiClient(configuration))
    try:
        # List Bulk Users Results
        api_response = api_instance.bulk_users_create_results(job_id, content_type, accept, x_org_id=x_org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling BulkJobRequestsApi->bulk_users_create_results: %s\n" % e)

"""
 .88888.   888888ba   .88888.  dP     dP  888888ba  .d88888b  
d8'   `88  88    `8b d8'   `8b 88     88  88    `8b 88.    "' 
88        a88aaaa8P' 88     88 88     88 a88aaaa8P' `Y88888b. 
88   YP88  88   `8b. 88     88 88     88  88              `8b 
Y8.   .88  88     88 Y8.   .8P Y8.   .8P  88        d8'   .8P 
 `88888'   dP     dP  `8888P'  `Y88888P'  dP         Y88888P  
oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
"""

def create_user_group(display_name):
    api_instance = jcapiv2.UserGroupsApi(jcapiv2.ApiClient(configuration))
    body = {
        'name': display_name
    }
    try:
        # Create a new User Group
        api_response = api_instance.groups_user_post(content_type, accept, body=body, x_org_id=x_org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling UserGroupsApi->groups_user_post: %s\n" % e)

def get_user_groups():
    api_instance = jcapiv2.UserGroupsApi(jcapiv2.ApiClient(configuration))
    try:
        user_groups = api_instance.groups_user_list(content_type, accept)
        print(user_groups)
    except ApiException as err:
        print("Exception when calling UserGroupsApi->groups_user_list: %s\n" % err)

def get_user_group_id_by_name(display_name):
    api_instance = jcapiv2.UserGroupsApi(jcapiv2.ApiClient(configuration))
    try:
        user_groups = api_instance.groups_user_list(content_type, accept)
        for group in user_groups:
            if group.name == display_name:
                return group.id
        return None
    except ApiException as err:
        print("Exception when calling UserGroupsApi->groups_user_list: %s\n" % err)

def bind_user_to_user_group(user_id, group_id):
    api_instance = jcapiv2.UserGroupMembersMembershipApi(jcapiv2.ApiClient(configuration))
    body = {
        'id': user_id,
        'op': 'add',
        'type': 'user'
    }
    try:
        # Manage the members of a User Group
        api_instance.graph_user_group_members_post(group_id, content_type, accept, body=body, x_org_id=x_org_id)
    except ApiException as e:
        print("Exception when calling UserGroupMembersMembershipApi->graph_user_group_members_post: %s\n" % e)

"""
888888ba   88888888b dP     dP dP  a88888b.  88888888b .d88888b  
88    `8b  88        88     88 88 d8'   `88  88        88.    "' 
88     88 a88aaaa    88    .8P 88 88        a88aaaa    `Y88888b. 
88     88  88        88    d8' 88 88         88              `8b 
88    .8P  88        88  .d8P  88 Y8.   .88  88        d8'   .8P 
8888888P   88888888P 888888'   dP  Y88888P'  88888888P  Y88888P  
ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
"""

def get_device_ids():
    api_instance = jcapiv1.SystemsApi(jcapiv1.ApiClient(configurationv1))
    try:
        # List All Devices
        return api_instance.systems_list(content_type, accept, x_org_id=x_org_id)
    except ApiException as e:
        print("Exception when calling SystemsApi->systems_list: %s\n" % e)

def get_device_id_by_name(display_name):
    for device in get_device_ids().results:
        if device.display_name == display_name:
            return device.id
    return None

def bind_user_to_device(user_id, device_id):
    api_instance = jcapiv2.GraphApi(jcapiv2.ApiClient(configuration))
    body = {
        'id': user_id,
        'op': 'add',
        'type': 'user'
    }
    try:
        # Manage associations of a System
        api_instance.graph_system_associations_post(device_id, content_type, accept, body=body, x_org_id=x_org_id)
    except ApiException as e:
        print("Exception when calling GraphApi->graph_system_associations_post: %s\n" % e)

if __name__ == "__main__":
    main()