import json


EXISTING_ID = 1
NON_EXISTING_ID = 666



data_dict_update = {
    "id": EXISTING_ID,
    "title": "foo",
    "body": "new_bar",
    "userId": 1
}


data_dict_create = {
    "id": NON_EXISTING_ID,
    "title": "new_foo",
    "body": "new_bar",
    "userId": 1
}


data_str_create = json.dumps(data_dict_create)
data_str_update = json.dumps(data_dict_update)
