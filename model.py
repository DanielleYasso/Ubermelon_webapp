import sqlite3

class Melon(object):
    """A wrapper object that corresponds to rows in the melons table."""
    def __init__(self, id, melon_type, common_name, price, imgurl, flesh_color, rind_color, seedless):
        self.id = id
        self.melon_type = melon_type
        self.common_name = common_name
        self.price = price
        self.imgurl = imgurl
        self.flesh_color = flesh_color
        self.rind_color = rind_color
        self.seedless = bool(seedless)

    def price_str(self):
        return "$%.2f"%self.price

    def __repr__(self):
        return "<Melon: %s, %s, %s>"%(self.id, self.common_name, self.price_str())

class Customer(object):
    def __init__(self, id, email, givenname, surname, password, telephone, tos_agree, gender, dob, 
        billto_address1, billto_address2, billto_city, billto_state, billto_postalcode, shipto_address1, shipto_address2,
        shipto_city, shipto_state, shipto_postalcode, region):
      self.id = id
      self.email = email
      self.givenname = givenname
      self.surname = surname
      self.password = password
      self.telephone = telephone
      self.tos_agree = tos_agree
      self.gender = gender
      self.dob = dob
      self.billto_address1 = billto_address1
      self.billto_address2 = billto_address2
      self.billto_city = billto_city
      self.billto_state = billto_state
      self.billto_postalcode = billto_postalcode
      self.shipto_address1 = shipto_address1
      self.shipto_address2 = shipto_address2
      self.shipto_city = shipto_city
      self.shipto_state = shipto_state
      self.shipto_postalcode = shipto_postalcode
      self.region = region

def connect():
    conn = sqlite3.connect("melons.db")
    cursor = conn.cursor()
    return cursor

def get_melons():
    """Query the database for the first 30 melons, wrap each row in a Melon object"""
    cursor = connect()
    query = """SELECT id, melon_type, common_name,
                      price, imgurl,
                      flesh_color, rind_color, seedless
               FROM melons
               WHERE imgurl <> ''
               LIMIT 30;"""

    cursor.execute(query)
    melon_rows = cursor.fetchall()

    melons = []

    for row in melon_rows:
        melon = Melon(row[0], row[1], row[2], row[3], row[4], row[5],
                      row[6], row[7])

        melons.append(melon)

    print melons

    return melons

def get_melon_by_id(id):
    """Query for a specific melon in the database by the primary key"""
    cursor = connect()
    query = """SELECT id, melon_type, common_name,
                      price, imgurl,
                      flesh_color, rind_color, seedless
               FROM melons
               WHERE id = ?;"""

    cursor.execute(query, (id,))

    row = cursor.fetchone()
    
    if not row:
        return None

    melon = Melon(row[0], row[1], row[2], row[3], row[4], row[5],
                  row[6], row[7])
    
    return melon

def get_customer_by_email(email):
    cursor = connect()
    query = 
