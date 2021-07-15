# Escalations Engineer (SmokeJumper) Homework Assignment

## Setup
```bash
git clone https://github.com/dgparks/jumpcloud-escalations-engineer-assignment.git
cd jumpcloud-escalations-engineer-assignment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# NOTE1: normally we would add the /out and /log folders to .gitignore,
#        but they have been included in the repo for our purposes
# NOTE2: the below assumes that you have correctly configured the mongodb
#
# send a new brewery analysis to the /out folder

python scripts/brewery.py

#
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# add JumpCloud API Key to demo_org_config.py
# be sure to replace YOUR_API_KEY_GOES_HERE with an actual API key
echo "API_KEY = 'YOUR_API_KEY_GOES_HERE'" > scripts/demo_org_config.py

# set up demo org according to below specs
python scripts/demo_org_setup.py
```
## Part 1: Database Queries
1. Create and provide a `script` with `logging` to achieve each of the following:
    - Script: [scripts/demo_org_setup.py](scripts/demo_org_setup.py), Log: [log/brewery-2021-07-15_09-14-29.096275.log](log/brewery-2021-07-15_09-14-29.096275.log)
  - We’re coming out with a new hoppy delicious IPA. To let our customers know, we need two mailing lists.
    - One that includes the email addresses of `all of our customers`
      - `Devon's Note`: Since it's a mailing list (ostenibly something we would like to access programatically), I decided to leave the output as a list of objects, and I included the `first_name` and `last_name` of the customers too. If we want just a comma-separated list of strings (email addresses only), it's quite simple to add a line or two to achieve that.
      - ```json
        [
          { "first_name": "Jessica", "last_name": "Patterson", "email": "jpatterson@notarealemail.com" },
          { "first_name": "Alessandro", "last_name": "Leon", "email": "aleon@notarealemail.com" },
          { "first_name": "Konner", "last_name": "Marks", "email": "kmarks@notarealemail.com" },
          ...
        ]
        ```
          See full output here: [out/brewery-2021-07-15_09-14-29.096275.json](out/brewery-2021-07-15_09-14-29.096275.json)
    - Another that includes only the email addresses for customers whose `favorite beer is an IPA`.
      - `Devon's Note`: Again, I interpreted this to mean "includes (at least) the email addresses, *but only for those customers whose favorite beer is an IPA*", as opposed to the more literal reading in which we return *only the email addresses*. In a production environment, I would of course seek clarification from stakeholders before unilaterally deciding which data to return.
      - ```json
        [
          { "first_name": "Kelton", "last_name": "Cobb", "email": "kcobb@notarealemail.com", "type": "IPA" },
          { "first_name": "Judah", "last_name": "Chung", "email": "jchung@notarealemail.com", "type": "IPA" },
          { "first_name": "Santino", "last_name": "Ryan", "email": "sryan@notarealemail.com", "type": "IPA" },
          ...
        ]
        ```
        See full output here: [out/brewery-2021-07-15_09-14-29.096275.json](out/brewery-2021-07-15_09-14-29.096275.json)
  - We need to gather some data on our tap rooms to show which is the `most popular location`. We need to know how many customers have frequented each location between 1/1/2021 - 4/1/2021.
    - ```json
      [ 
        { "_id": "123 Fake Street, Denver, CO", "count": 12 }, 
        { "_id": "987 Fake Blvd, Boulder, CO", "count": 8 } 
      ]
      ```
  - We’re trying to determine what type of beer is most popular with our customers so we can determine what our `next experimental beer` should be! Can you provide us with an array of objects that include the `beer name`, `type`, and `number of customers` where that beer is their favorite?
      - ```json
        [
          { "name": "Super Haze", "type": "Hazy IPA", "count": 115 }, 
          { "name": "Musical Mosaic", "type": "IPA", "count": 33 }, 
          { "name": "Slam Dunk", "type": "Dunkelweizen", "count": 20 },
        ]
        ```
2. Provide the output results for each of these requests.
    - `See above for results and a link to the output file.`

## Part 2: Interacting with JumpCloud
1. Using the programming language of your choice (`Go` or `JavaScript` preferred), complete the following and provide your solution for each:
   - `Devon's Note`: Since there isn't a JS SDK, I elected to use the Python SDK to save time and avoid reinventing the wheel. I certainly *could* have written an ad hoc mini-library in JS to handle auth and endpoint connections, but that seemed a bit outside the scope of the intention here. Let me know if you'd like me to reimplement this in something other than Python.
   - View method declarations in [scripts/demo_org_setup.py](scripts/demo_org_setup.py)
   - `Create and activate 2 Users`
      - ```python
        create_and_activate_users([
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
        ])
        ```
   - `Create a Group of Users`
      - ```python
        create_user_group('Philosophers')
        ```
   - `Associate Users to the Group of Users`
      - ```python
        # Get User and Group Ids
        schopenhauer_id = get_user_id_by_username('arthur.schopenhauer')
        kierkegaard_id = get_user_id_by_username('soren.kierkegaard')
        philosophers_id = get_user_group_id_by_name('Philosophers')

        # Associate Users to User Group
        bind_user_to_user_group(schopenhauer_id, philosophers_id)
        bind_user_to_user_group(kierkegaard_id, philosophers_id)
        ```
   - `Associate one User to the recently added system in JumpCloud`
      - ```python
        my_macbook_id = get_device_id_by_name('Eos-256X.local')
        bind_user_to_device(schopenhauer_id, my_macbook_id)
        ```

2. Log in to the system as the JumpCloud managed user

3. Set agent logs to DEBUG on system and provide a copy of agent logs
    - `Devon's Note`: I could not find any information about setting the agent logs to DEBUG.
    - Agent logs: [log/jcagent_2021-07-15_01-25.log](log/jcagent_2021-07-15_01-25.log)

4. Add a SSO (SAML) Connector in the JumpCloud Admin Console  
*Note: You may choose the web-based application of your choice but many applications/services provide free trials and will allow enabling of SAML authentication. For example: Salesforce (Trailhead) or ThousandEyes allow for SAML configurations with free trial accounts.*. 
   - Configure the SAML authentication on the chosen app/service-side
   - Validate one of your users created in Task 1 can login to the application through the user’s JumpCloud portal
   - Create and provide a HAR file of the SAML request
      - [out/app.thousandeyes.com_21-07-15_10-10-47.har](out/app.thousandeyes.com_21-07-15_10-10-47.har)

## Devon's Feedback
- `graph_user_associations_list` (jcapi-python) has a required positional argument, targets, that is supposed to be a list of strings. But if we pass a list of 2 or more strings, we get the following response:
  - ```http
    HTTP response body: {"message":"failed to list graph associations (org=60e87fecf568ca763a3bc278,from=user:60efa55e3206b934ea7a5d0a,targets=[application,system]): must provide exactly 1 target, got 2","status":"INVALID_ARGUMENT"}
    ```
- `filter` is a reserved keyword in python, but I see it being used as a variable name in `jcapi-python` examples
- It took me longer than I'd like to admit to realize that v1 of the API is required to request a list of all users or devices. Although I now see that there is some text explaining this at the top of their respective v2 sections...it could be helpful to stub in a fake endpoint on the v2 docs with instructions and a link to the v1 endpoint.

