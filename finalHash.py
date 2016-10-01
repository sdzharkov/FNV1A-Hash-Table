import time

class hashObj(object):
    def __init__(self, key = None, value = None, deleted = False):
        self.key = key;
        self.value = value;
        self.deleted = False;

    def __repr__(self):
        return str(self.key)

    def __str__(self):
        return str(self.key)

class hashTable(object):
    def __init__(self, size):
        self.data = [hashObj() for i in range(size)]
        self.size = size;
        self.current = 0;

    def __repr__(self):
        return "yes"

    def __str__(self):
        return 'hm'

    def __getitem__(self,index):
        return self.data[index]

    def __iter__(self):
        return iter(self.data)

    def next(self):
        if self.current > self.high:
            raise StopIteration
        else:
            self.current += 1
            return self.current - 1

    def booleanSet(self, key, value):                       #Guarentees an insertion
        if self.data[value].key == None:
            self.data[value].key = key
            self.data[value].value = value
            self.updateCount(value)
            self.checkRehash()
            return True

        else:                                               #if you received a collision
            i = 1
            while True:
                hashNum2 = self.quadratic(i, key)           #Keep hashing until an empty position is found
                i+=2
                if self.data[hashNum2].key == None:
                    self.data[hashNum2].key = key
                    self.data[hashNum2].value = value       #replace key/value with new values
                    self.updateCount(hashNum2)              #If deleted, do not update count
                    self.checkRehash()                      #Ensures load Factor < .5
                    return True

    def quadratic(self, i, key):
        return ((self.fnv64_2(key) + i) % self.size)        #Not quite quadratic, more so linear with 2 step. Done to maximize
                                                            #Efficiency as the hash/rehash avoid many collisions

    def updateCount(self, value):
        if self.data[value].deleted == False:               #To not raise the # of current if going into a deleted area
            self.current += 1;

    def checkRehash(self):                                  #If the load factor is greater than half, rehash
        if float(self.current/self.size) >= .5:
            self.reHash(self.size * 2 + 1)                  


    def get(self, key): 
        hashNum = self.fnv64(key)                           #Hash to find the value
        i = 1
        if self.data[hashNum].key != key:
            hashNum2 = self.quadratic(i, key)
            while True:                                     #While loop done to continue search through quadratic function
                if self.data[hashNum2].key != key:          #This maximizes efficiency by not looking through all entries
                    if self.data[hashNum2].key == None:
                        return None                         #If nothing exists, return nothing

                    else:
                        hashNum2 = self.quadratic(i, key)   #Continue search
                        i+=2;

                else:
                    return self.data[hashNum2]              #Must be found at this point, return the hashObj
        else:
            return self.data[hashNum]                       #Found


    def delete(self, key):                              #Simple delete utilizing the Get Function
        x = self.get(key)
        if x != None: 
                                      #Set the key to None because other search depends on it
            x.key = None
            x.deleted = True
            return True


    def floatLoad(self):                                # Simple float load implementation
        return float(self.current/self.size)


    def reHash(self, size):                             # Creates a new temporary data list with objects
        newData = [hashObj() for i in range(size)]
        tempData = []
        for item in self.data:
            if item.key != None:
                tempData.append(item)                   # temporary list for later insertions to new hashtable

        self.data = newData                             #inserting the new table 
        self.size = size
        self.current = 0
        for x in tempData:                              #For the temporary values I stored earlier,
            self.booleanSet(x.key, self.fnv64(x.key))   #Insert into the new data array of Hashtable


    def fnv64(self, myStr):                             #actual implementation of fnv64_A
        hval = 0x811c9dc5;                              #I give credit to the authors of the FNV Algorithm, implemented from the explanation found below
        FNV_prime = 0x1000193;                          #http://isthe.com/chongo/tech/comp/fnv/
        for i in range(len(myStr)):
            hval ^= ord(myStr[i])
            hval = hval * FNV_prime
        #return hash1
        return hval % self.size


    def fnv64_2(self, myStr):                           #I needed this to perform the quardratic rehash
        hval = 0x811c9dc5;                              
        FNV_prime = 0x1000193;
        for i in range(len(myStr)):
            hval ^= ord(myStr[i])
            hval = hval * FNV_prime
        #return hash1
        return hval


def main():
    rawInput = input("Please enter a file of words to run (I.E. words.txt contains the dictionary): ")
    x = hashTable(11)                                   #starting low proves to be more effective over 400,000 words
    f = open(rawInput, 'r')
    for line in f:
        y = line.rstrip()
        x.booleanSet(y, x.fnv64(y))

    while True:
        print("Options (Type number to Proceed):")
        print("1. Get Term")
        print("2. Delete Term")
        print("3. View Table")
        print("4. Exit Program")
        rawInput = input("Type number to proceed: ")
        if rawInput == "1":
            raw1 = input("Please enter the word: ")
            gotWord = x.get(raw1)
            if gotWord == None:
                print("This word does not exist, or the file you selected does not contain the word you requested.")
            else:
                print("Word: ", gotWord.key, " Value: ", gotWord.value)
        if rawInput == "2":
            raw1 = input("Please enter the word: ")
            deleteWord = x.delete(raw1)
            if deleteWord != True:
                print("This word does not exist, or the file you selected does not contain the word you requested.")
            else:
                print("Deleted ", raw1)
        if rawInput == "3":
            for num in range(x.size):
                #print(x[num].key, " | ", x[num].value, " | ", x[num].deleted)
                print(repr(x[num].key).ljust(20),repr(x[num].value).ljust(4), repr(x[num].deleted).rjust(6), end='\n') 
                #print(x[num].key.rjust(2), repr(x[num].value).rjust(3), (str(x[num].deleted)).rjust(4), end=' ') 
            print("------------------------------")
            print('Word             Key   Deleted')

        if rawInput == "4":
            break
        else:
            continue


if __name__ == '__main__':
    #start_time = time.time()
    main()
    #print("--- %s seconds ---" % (time.time() - start_time))


