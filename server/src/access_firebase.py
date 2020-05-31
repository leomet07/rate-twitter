"""
import firebase_admin

default_app = firebase_admin.initialize_app(name="rate-twitter")
print("Imported")
print(default_app.name)
"""
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
cred = credentials.Certificate("rate-twitter.json")

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(
    cred, {"databaseURL": "https://rate-twitter.firebaseio.com"}
)

# As an admin, the app has access to read and write all data, regradless of Security Rules
# ref = db.reference("users")
# print(ref.get())


def check_key(key, uid):

    ref = db.reference("users/" + str(uid) + "/" + "signle_use_id")
    db_id = ref.get()

    print("db_id: " + str(db_id))

    return db_id == key


# print("Returned: " + str(check_key("signle_use_id_test", "developer_uid")))
def set_key(key, uid):
    # Get a database reference to our blog.
    ref = db.reference("users/" + str(uid) + "/" + "signle_use_id")
    ref.set(key)