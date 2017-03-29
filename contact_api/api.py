# TODO:
# Make is_deleted check a helper function so all functions can use it
# Refactor any of the existing functions that could be combined
# ensure audit info is persisted in each contact record

# email address is the primary key of the store
# used here as 'contact'

def create(store, contact):
    contact['is_deleted'] = False
    #contact['created_by'] =
    store[contact['email_address']] = contact


def replace(store, contact):
    # copy audit info
    contact_data = store[contact].deepcopy()
    # delete existing record
    del(store[contact])
    # create a new record
    # add in audit info
    store[contact['email_address']] = contact


def get(store, contact):
    active_contacts = {}
    # Ensure records are not deleted before showing them to the client
    for email_address, contact in store.items():
        if contact['is_deleted'] == False:
            active_contacts[email_address] = contact
    return active_contacts


def filter(store, email=None):
    active_contacts = {}
    # filter out deleted contact records
    for email_address, contact in store.items():
        if contact['is_deleted'] == False:
            active_contacts[email_address] = contact
    # if an email address was provided, return matching contact record
    if email:
        return active_contacts[email]
    # otherwise, return all live records
    else:
        return active_contacts


def delete(store, email):
    store[email]['is_deleted'] = True
