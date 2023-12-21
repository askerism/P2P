from pymongo import MongoClient


# Includes database operations
class DB:
    # db initializations
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['p2p-chat']
        self.accounts = self.db['accounts']
        self.online_peers = self.db['online_peers']


    # checks if an account with the username exists

    def is_account_exist(self, username):
        return self.accounts.count_documents({'username': username}) > 0

    # registers a user
    def register(self, username, password):
        account = {
            "username": username,
            "password": password
        }
        self.accounts.insert_one(account)

    # retrieves the password for a given username
    def get_password(self, username):
        user = self.accounts.find_one({"username": username})
        if user:
            return user["password"]
        else:
            return None

    # checks if an account with the username is online
    def is_account_online(self, username):
        return self.online_peers.count_documents({"username": username}) > 0

    def get_online_peers(self):
        online_users = self.online_peers.find()
        return [user["username"] for user in online_users]

    # logs in the user

    def user_login(self, username, ip, port):
        online_peer = {
            "username": username,
            "ip": ip,
            "port": port
        }
        self.online_peers.insert_one(online_peer)

    # logs out the user
    def user_logout(self, username):
        self.online_peers.delete_many({"username": username})

    # retrieves the ip address and the port number of the username
    def get_peer_ip_port(self, username):
        user = self.online_peers.find_one({"username": username})
        if user:
            return user["ip"], user["port"]
        else:
            return None, None


def get_online_peers():
    return None
