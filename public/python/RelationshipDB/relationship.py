import mysql.connector
import networkx as nx 
from mysql.connector import Error
from mysql.connector import MySQLConnection, Error


mydb = mysql.connector.connect(
  host="bde3mevdri7rlbi3akym-mysql.services.clever-cloud.com",
  user="uowiznytelzqtkhe",
  password="g1J46NIB8mhoYzmJwyAs",
  database="bde3mevdri7rlbi3akym"
)
def connect():
    """ Connect to MySQL database """
    conn = None
    try:
        conn = mysql.connector.connect(
                host="bde3mevdri7rlbi3akym-mysql.services.clever-cloud.com",
                user="uowiznytelzqtkhe",
                password="g1J46NIB8mhoYzmJwyAs",
                database="bde3mevdri7rlbi3akym")
    
        if conn.is_connected():
            print('Connected to MySQL database')

    except Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()


def insert_relationship(documentID1, documentID2,strength, type,Status):
    
    """ Insert relationship """
    query = "INSERT INTO relationshiptb (documentID1, documentID2,strength, type,Status)" \
        "VALUES (%s,%s,%s,%s,%s)"
    args = (documentID1, documentID2,strength, type,Status)
    try:

        mycursor = mydb.cursor()
        mycursor.execute(query,args)

        if mycursor.lastrowid:
            print('last insert id', mycursor.lastrowid)
        else:
            print('last insert id not found')

        mydb.commit()
    except Error as error:
        print(error)


def delete_relationship(relationshipID):
    
    """ Delete relationship """
    query = "DELETE FROM relationshiptb WHERE relationshipID = %s"

    try:
       
        # execute the query
            mycursor = mydb.cursor()
            mycursor.execute(query, (relationshipID,))

        # accept the change
            mydb.commit()
            print("Deleted relationship ID: ",relationshipID)

    except Error as error:
            print(error)



def update_relationshipType(relationshipID, type):
    """ Update Relationship type """
    # prepare query and data
    query = """ UPDATE relationshiptb
                SET type = %s
                WHERE relationshipID = %s """

    data = (type, relationshipID)

    try:

        mycursor = mydb.cursor()
        mycursor.execute(query,data)

        # accept the changes
        mydb.commit()
        print("The Relationshp type has change to: ",type)

    except Error as error:
        print(error)

def update_relationshipStatus(relationshipID, status):
    """ Update Relationship type """
    # prepare query and data
    query = """ UPDATE relationshiptb
                SET status = %s
                WHERE relationshipID = %s """

    data = (status, relationshipID)

    try:

        mycursor = mydb.cursor()
        mycursor.execute(query,data)

        # accept the changes
        mydb.commit()
        print("The Relationshp status has change to: ",status)

    except Error as error:
        print(error)

def retriveAll():
    """ Update Relationship type """
    # prepare query and data
    query = """ SELECT * FROM relationshiptb  """

    try:

        # execute the query
        mycursor = mydb.cursor()
        mycursor.execute(query)

        for row in mycursor:
            print(row)

    except Error as error:
        print(error)

def main():
     connect()
     retriveAll()
     #insert_relationship('10001', '10003','3','D','R')
     #delete_relationship(4)
     #update_relationshipType(2, 'D')
     #update_relationshipStatus(2, 'R')
     
     #inser relationship
     dID1 = int(input("Document ID1: "))
     dID2 = int(input("Document ID2: "))
     strength = float(input("Strength: "))
     type = (input("Type: "))
     status = (input("Status: "))
     insert_relationship(dID1, dID2,strength,type,status)

     #delete relationship
     rID = int(input("Relationship ID: "))
     delete_relationship(rID)

     #update relationship Type
     rID = int(input("Relationship ID: "))
     type = (input("Type: "))
     update_relationshipType(rID, type)

     #update status
     rID = int(input("Relationship ID: "))
     status = (input("Status: "))
     update_relationshipStatus(rID, status)



if __name__ == '__main__':
     main()
