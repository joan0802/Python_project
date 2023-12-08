import sys, os

class Record:
    """Represent a record."""
    def __init__(self, category, descript, amount):
        """Initialize the Record"""
        self._category = category
        self._descript = descript
        self._amount = amount
    
    @property
    def category(self):
        """Return the category of a record"""
        return self._category
    @property
    def descript(self):
        """Return the description of a record"""
        return self._descript
    @property
    def amount(self):
        """Return the amount of a record"""
        return self._amount
    
class Records:
    """Maintain a list of all the 'Record's and the initial amount of money."""
    
    def __init__(self):
        """Read data from 'records.txt' and initialize attributes."""
        try:
            fh = open('records.txt', 'r')
            L = fh.readlines()
            fh.seek(0)
            if len(L) == 0: # the file is empty
                raise FileNotFoundError
        except FileNotFoundError: #file not found or file is empty
            try:
                self._money = int(input("How much money do you have? "))
            except ValueError:
                sys.stderr.write("Invalid value for money. Set to 0 by default.\n")
                self._money = 0
            self._rec = []
        else: # file has opend succesfully
            try:
                self._money = int(fh.readline())
                self._rec = []
                for line in fh.readlines():
                    part = line.split(' ')
                    if len(part) != 3: # check if the format is valid
                        raise ValueError
                    self._rec.append(Record(part[0], part[1], int(part[2])))
                print('Welcome back!\n')

            except ValueError:
                sys.stderr.write("Invalid format in records.txt. Deleting the contents.\n")
                fh = open('records.txt', 'w') # delete the contents
                fh.close()
                try:
                    self._money = int(input("How much money do you have? "))
                except ValueError:
                    sys.stderr.write("Invalid value for money. Set to 0 by default.\n")
                    self._money = 0
                self._rec = []

            fh.close()
 
    def add(self, categories):
        """Add a new record"""
        try:
            print('Add an expense or income record with category, description, and amount (separate by spaces): ')
            print('｜\033[1m1\033[0m｜ Cancel')
            temp = tuple(input().split(' ')) #split the description and the amount
            
            if temp[0] == '1':
                return
            if len(temp) != 3: # The format is incorrect
                raise IndexError
            if categories.is_category_valid(temp[0], categories._categories) == False:
                raise Exception

            self._money = int(self._money) + int(temp[2])
            self._rec += [Record(temp[0], temp[1], int(temp[2]))] #create tuple to include the information of description and amount of each income/expense

        except ValueError: # the value is invalid(not int)
            sys.stderr.write("Invalid value for money.\nFail to add a record.\n")
        except IndexError: # the input format is invalid
            sys.stderr.write("The format of a record should be like this: meal breakfast -50.            \nFail to add a record.\n")
        except Exception:
            sys.stderr.write(f'The specified category is not in the category list.\nYou can check the category list by command "view categories".                             \nFail to add a record.\n')
 
    def view(self):
        """View all the records"""
        cat = {}
        print('\n---Expense and Income Records:---\n')
        print("Category        Description          Amount")
        print("=============== ==================== ======")
        for i in self._rec: # print the record
            if i.category in cat:
                cat[i.category] += int(i.amount)
            else:
                cat[i.category] = int(i.amount)
            print(f'{i.category:<16}{i.descript:<21}{int(i.amount):<6d}')
        print("=============== ==================== ======")
        print(f'\nNow you have {self._money} dollars.')

        if cat:
            max_cost = min(cat.values())
            highest_category = [key for key, value in cat.items() if value == max_cost]
            if max_cost < 0:
                print(f"You spent the most of your money on {' and '.join(highest_category)}!")
            else: # The record only has income record
                print(f"You don\'t have any spend record!")
        else:
            print(f'You don\'t have any spend record!')
 
    def delete(self):
        """Delete a record"""
        try:
            print('Which expense/cost do you want to delete? ')
            print('｜\033[1m1\033[0m｜ Cancel')
            s = input().split(' ')
            if s[0] == '1':
                return
            if len(s) != 3: # check if the format is valid
                raise ValueError
            s = (s[0], s[1], int(s[2])) # turn the value from str to int

        except ValueError: # The format is incorrect
            sys.stderr.write("The format of a record should be like this: meal breakfast -50.\nFail to delete a record.\n")
        else:
            delete_list = [] # record the index of record that match our need
            for i, v in enumerate(self._rec): # To find the item in the list that we want to delete
                if(v.category == s[0] and v.descript == s[1] and v.amount == s[2]): 
                    delete_list.append(i)

            if len(delete_list) == 1: # only one record that match
                self._money = int(self._money) - int(self._rec[ delete_list[0] ].amount) # remove the amount from money
                del(self._rec[ delete_list[0] ])
            elif len(delete_list) == 0: 
                sys.stderr.write(f'There\'s no record with {str(s[0])} {str(s[1])} {str(s[2])}.\nFail to delete a record.\n')
            elif len(delete_list) > 1: # over one records that match
                try:
                    d = input(f"You have {len(delete_list)} records that match your needs, which one do you want to delete? ")
                    self._money = int(self._money) - int(self._rec[ delete_list[0] ].amount)
                    del(self._rec[ delete_list[int(d)-1] ])
                except IndexError:
                    sys.stderr.write(f"You don't have that much records of {str(s[0])} {str(s[1])} {str(s[2])}\n")
    
    def find(self, tpe, to_find, categories):
        """To find all of the records under a category"""
        filtered_records = []
        
        if not categories.is_category_valid(to_find, categories._categories):
            sys.stderr.write(f'There is no "{to_find}" category')
            return
        for i in tpe:
            filtered_records += list(filter(lambda record: record.category == i, self._rec))
        
        if len(filtered_records) == 0:
            sys.stderr.write(f'There is no expense or income records under the category {to_find}')
            return
        else:
            print(f'Here\'s your expense and income records under category "{to_find}:"')
            print("Category        Description          Amount")
            print("=============== ==================== ======")
            total = 0
            for i in filtered_records:
                total += int(i.amount)
                print(f'{i.category:<16}{i.descript:<21}{int(i.amount):<6d}')
            print("=============== ==================== ======")
            print(f'\nThe total amount under {to_find} is {total} dollars.')

    def save(self):
        """Save the records"""
        with open('records.txt', 'w') as fh:
            fh.write(str(self._money)+'\n')
            fh.writelines(f"{line.category} {line.descript} {line.amount}\n" for line in self._rec)

class Categories:
    """Maintain the category list and provide some methods."""
    def __init__(self):
        """Init category"""
        self._categories =  ['expense', ['food', ['meal', 'snack', 'drink'], 
                'transportation', ['bus', 'railway']], 
                'income', ['salary', 'bonus']]
 
    def view(self, L, indentation = 0):
        """Show all the categories"""
        for i in L:
            if type(i) == list:
                self.view(i, indentation+1)
            else:
                print(' '*indentation*2 + '- ' + i)
 
    def is_category_valid(self, category, categories):
        """To check if the category is exist"""
        for i in categories:
            if type(i) == type([]):
                if self.is_category_valid(category, i) == True:
                    return True
            else:
                if i == category:
                    return True
        return False
 
    def find_subcategories(self, category):
        """Find subcategories of a category"""
        def find_subcategories_gen(category, categories, found=False):
            """This is a generator that yields the target category and its subcategories"""
            if type(categories) == list:
                for index, child in enumerate(categories):
                    yield from find_subcategories_gen(category, child, found)
                    if child == category and index + 1 < len(categories)                         and type(categories[index + 1]) == list:
                        for sub in categories[index + 1]:
                            yield from find_subcategories_gen(category, sub, True)
            else:
                if categories == category or found:
                    yield categories
        
        return find_subcategories_gen(category, self._categories)
    
categories = Categories()
records = Records()

while(True):
    print("""
 *－－－\033[34mPymoney$\033[0m－－－*
｜\033[1m1\033[0m｜add             ｜
｜\033[1m2\033[0m｜view            ｜
｜\033[1m3\033[0m｜delete          ｜
｜\033[1m4\033[0m｜find            ｜
｜\033[1m5\033[0m｜view categories ｜
｜\033[1m6\033[0m｜exit            ｜
 *－－－－－－－－－－ *
    """)
    oper = input("What do you want to do? ")
    #print(f'rec = {rec}')
    if(oper == "add" or oper == '1'):
        records.add(categories)

    elif (oper == "view" or oper == '2'):
        records.view()
        
    elif (oper == "delete" or oper == '3'):
        records.delete()
        
    elif (oper == "find" or oper == '4'):
        print('Which category do you want to find? ')
        print('｜\033[1m1\033[0m｜ Cancel')
        category = input()
        if category == '1':
            continue
        target_categories = categories.find_subcategories(category)
        records.find(target_categories, category, categories)
        
    elif (oper == "view categories" or oper == '5'):
        categories.view(categories._categories)

    elif (oper == 'exit' or oper == '6'):
        records.save()
        print('\n\033[34mSee you again!')
        break

    else: # unknown function
        sys.stderr.write('Invalid command. Try again.\n')
