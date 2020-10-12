class Customer():

    def __init__(self, id, name, address, email="", password="Nice try pal..."):
        self.id = id
        self.name = name
        self.address = address
        self.email = email
        self.password = password