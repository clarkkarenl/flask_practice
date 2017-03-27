# TODO:
# Make is_deleted check a helper function so all functions can use it
# Refactor any of the existing functions that could be combined


def create(store, contact):
    contact['is_deleted'] = False
    store[contact['email_address']] = contact


def replace(store):
    # copy audit info
    # delete existing record
    # create a new record
    # add in audit info
    pass


def get(store, id):
    # TODO don't include internal flags like is_deleted here
    return store[id]


def filter(store, email=None):
    active_contacts = {}

    # filter out deleted contact records
    # TODO refactor this to be more clear once is_deleted implemented
    for email_address, contact in store.items():
        if contact['is_deleted'] == False:
            active_contacts[email_address] = contact

    # if there was an email address provided, return matching contact record
    if email:
        return active_contacts[email]
    # otherwise, return all live records
    else:
        return active_contacts


def delete(store, email):
    store[email]['is_deleted'] = True
