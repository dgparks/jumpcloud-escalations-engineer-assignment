graph_user_associations_list has a required positional argument, targets, that is supposed to be a list of strings. but if you pass a list of 2 or more strings, we get the following response:

HTTP response body: {"message":"failed to list graph associations (org=60e87fecf568ca763a3bc278,from=user:60efa55e3206b934ea7a5d0a,targets=[application,system]): must provide exactly 1 target, got 2","status":"INVALID_ARGUMENT"}


`filter` is a reserved keyword in python, but I continually see it being used as a variable name in api method examples

why is there no way to retrieve a list of all users in v2?