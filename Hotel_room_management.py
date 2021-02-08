# room management system
from prettytable import PrettyTable
import sqlite3
import datetime

my_database = sqlite3.connect('contact.db')
# ------------------------------------------------------
try:
    my_database.execute('select * from contacts')
except:
    my_database.execute('''CREATE TABLE contacts
         (NAME          char(30)  NOT NULL,
         Phone_no       INT   NOT NULL,
         ADDRESS        CHAR(50),
         EMAIL_ID       CHAR(50));''')
# --------------------------------------------------------
#print(my_database.execute('select * from contacts'))
try:
    my_database.execute('select * from room_detail')
except:
    my_database.execute('''CREATE TABLE room_detail
         (Room_id    INT NOT NULL,
         NAME          char(30) NOT NULL,
         no_of_person       INT   NOT NULL,
         no_of_bed       INT   NOT NULL,
         room_type        CHAR(10),
         check_in_time char(50),
         check_out_time char(50));''')
try:
    my_database.execute('select * from room_available')
except:
    my_database.execute('''CREATE TABLE room_available
        ( 
        room_type   char(10),
        no_of_room     int  NOT NULL,
        no_of_bed       int NOT NULL,
        price_per_room    int NOT NULL);''')
    #print(my_database.execute('select * from room_detail'))
    my_database.execute('Insert into room_available values("Ac",20,1,900)')
    my_database.execute('Insert into room_available values("Non-aC",20,1,700)')
    my_database.execute('Insert into room_available values("Ac",20,2,1300)')
    my_database.execute('Insert into room_available values("Non-ac",20,2,1100)')
    my_database.commit()


class contacts:
    Name = str()
    Mobile_no = str()
    Address = str()
    Email = str()

    def __init__(self):  # constructor used for declaring variable
        self.Name = ''
        self.Mobile_no = ''
        self.Address = ''
        self.Email = ''

    def show_table_format(self, columns, detail):
        myview = PrettyTable(columns)
        data = []
        for i in detail:
            data.append(i)
        if(not data):
            print('oops no data found !!! :(')
            return
        myview.add_rows(data)
        print(myview)
        return

    def Add_contact(self):
        self.Name = input('Enter the name: ')
        self.Mobile_no = input('Enter the number: ')
        self.Address = input('Enter the address: ')
        self.Email = input('Enter the email: ')

        my_database.execute('Insert into contacts values("{}","{}","{}","{}")'.format(
            self.Name, self.Mobile_no, self.Address, self.Email))
        my_database.commit()
        print('Data saved succesfully')
        return

    def show_contacts(self):
        columns = ['Name', 'Phone no.', 'Address', 'Email Id']
        contact_detail = my_database.execute('select * from contacts')
        self.show_table_format(columns, contact_detail)

    def search_contacts(self):
        columns = ['Name', 'Phone no.', 'Address', 'Email Id']
        search_name = input('Enter the name of contact to search: ')
        data = my_database.execute(
            "select * from contacts where name = '{}' COLLATE NOCASE".format(search_name))
        self.show_table_format(columns, data)


class Rooms(contacts):

    def __init__(self):
        self.room_type = ''
        self.no_of_bed = 0
        self.no_of_person = 0
        self.room_id = ''
        contacts.__init__(self)

    def Book_room(self):
        """Funcion to book rooms """

        self.Add_contact()

        self.room_type = input('Type of room to be booked Ac/Non-ac: ')
        self.no_of_bed = int(input('Enter the no of bed: '))
        self.no_of_person = int(input('Enter the no of person: '))
        self.room_id = input('Enter the room Id: ')
        my_database.execute('Insert into room_detail values({},"{}",{},{},"{}","{}","{}")'.format(
            self.room_id, self.Name, self.no_of_person, self.no_of_bed, self.room_type, ' ', ' '))
        my_database.commit()
        print('Room booked succesfully-:) ')
        return

    def show_room_booked(self):
        columns = ['Room Id', 'Name', 'No of person', 'No of beds',
                   'Room type', 'Check In time', 'Chcck Out time']
        room_detail = my_database.execute('select * from room_detail')
        self.show_table_format(columns, room_detail)
        return

    def check_in(self):

        date = datetime.datetime.now()
        check_in_ID = input('Enter the Room_id of customer for check in: ')
        room_condition = my_database.execute(
            'select room_type,no_of_bed  from room_detail where Room_id = {} COLLATE NOCASE'.format(check_in_ID))
        room_data = []
        for i in room_condition:
            room_data = list(i)
        my_database.execute(
            'UPDATE room_detail set check_in_time = "{}" where Room_id = {} COLLATE NOCASE'.format(str(date), check_in_ID))
        my_database.execute(
            "UPDATE room_available set no_of_room  = no_of_room - 1 Where no_of_bed = {} AND room_type = '{}' COLLATE NOCASE".format(room_data[1], room_data[0]))
        my_database.commit()

        print('Customer checked in - Have a good  day ........')

    def check_out(self):
        check_out_id = input('Enter the room id of customer for check out: ')
        date = datetime.datetime.now()
        my_database.execute('UPDATE room_detail set check_out_time = "{}" where Room_id = {}'.format(
            str(date), check_out_id))
        room_condition = my_database.execute(
            'select room_type,no_of_bed  from room_detail where Room_id = {} COLLATE NOCASE'.format(check_out_id))
        room_data = []
        for i in room_condition:
            room_data = list(i)
           
        my_database.execute(
            "UPDATE room_available set no_of_room  = no_of_room + 1 Where no_of_bed = {} AND room_type = '{}' COLLATE NOCASE".format(room_data[1], room_data[0]))
        print()
        print('-' * 15, 'Customer checked out - Have a good  day ........')
        my_database.commit()
        pass

    def check_available_room(self):
        my_rooms = PrettyTable(
            ['Room type', 'Room available', 'No of bed', 'Price/room'])
        room_availability = my_database.execute('select * from room_available')
        for i in room_availability:
            my_rooms.add_row(i)
        print(my_rooms)
    def get_bill(self):
        try:
            check_out_id = input('Enter the room id of customer for check out: ')
            room_condition = my_database.execute(
                'select room_type,no_of_bed,name,check_in_time,check_out_time,room_id  from room_detail where Room_id = {} COLLATE NOCASE'.format(check_out_id))
            room_data = []
            for i in room_condition:
                room_data = list(i)
                break
            price = my_database.execute("Select price_per_room from room_available WHERE no_of_bed = {}  and  room_type  = '{}' COLLATE NOCASE ".format(room_data[1],room_data[0]))
            for i in price:
                money = int(i[0])
        except:
            print('No data found of room:  ',check_out_id,end  = '\n\n')
        print('='*80)
        print(' '*30,'----Payment Memo----',end  = '\n\n')
        print(' '*8,'Date:',datetime.date.today(),' '*25,'Room Id:',room_data[5],'\n\n')
        print(' '*8,'Name:',room_data[2],end  = '\n\n')
        print(' '*8,'Check In:',room_data[3],end = '\n\n')
        print(' '*8,'Check Out:',room_data[4],end = '\n\n')
        print('='*30,'Total amaount:',money,'='*30,end = '\n\n')
        print('='*18,'Contact:9644XXXXXX,','Adress: Karol bagh Delhi','='*18)


        '''print('Data removed succefully: ...')
        my_database.execute(
       'DELETE FROM ROOM_DETAIL WHERE Room_id = {} COLLATE NOCASE'.format(check_out_id))
        
        '''
        my_database.commit()

def contact_start_up():
    print(' '*15, '1. Press a to add new contact')
    print(' '*15, '2. Press s to show contacts')
    print(' '*15, '5. Press g to search contacts')


def room_start_up():
    print(' '*15, '1. Press b to Book new room')
    print(' '*15, '2. Press s to show room_booked')
    print(' '*15, '3. Press i to checkin details')
    print(' '*15, '4. Press o to checkout details')
    print(' '*15, '5. Press r to availablity of rooms')
    print(' '*15, '6. Press p to availablity of rooms')


def room_manager():
    person = Rooms()
    print('----------------:Welcome to room management system:-------------')

    answer = 'y'
    while answer in ['y', 'Y']:
        room_start_up()
        choice = input('Enter your choice: ')
        if choice in ['b', 'B']:
            person.Book_room()
        elif choice in ['s', 'S']:
            person.show_room_booked()
        elif choice in ['i', 'I']:
            person.check_in()
        elif choice in ['o', 'O']:
            person.check_out()
        elif choice in ['r', 'R']:
            person.check_available_room()
        elif choice in ['p','P']:
            person.get_bill()
        else:
            print('oops invalid choice !!! ')
        answer = input('Want to perform more operation y/n !!')


def contact_manager():
    person = Rooms()
    print('----------------:Welcome to conatact  management system:-------------')

    answer = 'y'
    while answer in ['y', 'Y']:
        contact_start_up()
        choice = input('Enter your choice: ')
        if choice in ['a', 'A']:
            person.Add_contact()
        elif choice in ['s', 'S']:
            person.show_contacts()
        elif choice in ['g', 'G']:
            person.search_contacts()
        else:
            print('oops invalid choice !!! ')
        answer = input('Want to perform more operation y/n !!')


if __name__ == '__main__':

    room_manager()
    contact_manager()

    pass
