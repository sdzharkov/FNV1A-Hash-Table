import time


class hashObj(object):
    """docstring for ."""

    def __init__(self, key = None, value = None, deleted = False):
        #super(, self).__init__()
        self.key = key;
        self.value = value;
        self.deleted = False;

    def __repr__(self):
        return str(key)
    # def __str__(self):
    #     return value

class hashTable(object):

    def __init__(self, size):
        self.data = [hashObj() for i in range(size)]
        #self.keys = [];
        self.size = size;
        self.current = 0;

    def __repr__(self):
        return "yes"

    def __str__(self):
        return 'hm'

    def __getitem__(self,index):
        return self.data[index]

    def __setitem__(self,index,value):
        self.bricks.bricksId[index] = value

    def __iter__(self):
        return iter(self.data)

    def next(self): # Python 3: def __next__(self)
        if self.current > self.high:
            raise StopIteration
        else:
            self.current += 1
            return self.current - 1

    def booleanSet(self, key, value):
        if self.data[value].key == None:
            self.data[value].key = key
            self.data[value].value = value
            self.updateCount(value)
            self.checkRehash()

        else:  #if you received a collision
            i = 1
            while True:
                hashNum2 = self.quadratic(i, value)
                i+=1
                if self.data[hashNum2].key == None:
                    self.data[hashNum2].key = key
                    self.data[hashNum2].value = value
                    self.updateCount(hashNum2)
                    self.checkRehash()
                    break

    def quadratic(self, i, key): #               1 4 9 16
        return ((fnv64(key) + i**2) % self.size)#    3 5 7

    def updateCount(self, value):
        if self.data[value].deleted == False:   #To not raise the # of current if going into a deleted area
            self.current += 1;

    def checkRehash(self):
        if float(self.current/self.size) >= .5:
            self.reHash(self.size * 2 + 1)

    def insert(self, key):
        hashNum = fnv64(key) % self.size;
        if self.data[hashNum].key == None:
            self.data[hashNum].key = key
            self.data[hashNum].value = hashNum
            self.updateCount(hashNum)
            self.checkRehash()

        else:  #if you received a collision
            i = 1
            while True:
                hashNum2 = self.quadratic(i, key)
                i+=1
                if self.data[hashNum2].key == None:
                    self.data[hashNum2].key = key
                    self.data[hashNum2].value = hashNum2
                    self.updateCount(hashNum2)
                    self.checkRehash()
                    break

    def get(self, key):  ################## do first none
        hashNum = fnv64(key) % self.size;
        i = 1
        if self.data[hashNum].value != key:
            hashNum2 = self.quadratic(i, key)
            while True:
                i+=1;
                if self.data[hashNum2].value != key and i <= self.size:
                    hashNum2 = self.quadratic(i, key)
                elif i > self.size:
                    return None
                else:
                    return self.data[hashNum2]
        else:
            return self.data[hashNum]


    def delete(self, key):
        x = self.get(key)
        if x != None:
            x.value = None
            x.deleted = True


    def floatLoad(self):                            # Simple float load implementation
        return float(self.current/self.size)


    def reHash(self, size):                         # Creates a new temporary data list with objects
        newData = [hashObj() for i in range(size)]
        tempData = []
        for item in self.data:
            if item.key != None:
                tempData.append(item)               # temporary list for later insertions to new hashtable
                #print("\n item: ", item.value)

        self.data = newData                         #inserting the new table 
        self.size = size
        self.current = 0
        for x in tempData:
            self.insert(x.key)



def fnv64(myStr):                                   #actual implementation of fnv64
    hval = 0x811c9dc5;                              #my offset basis
    FNV_prime = 0x1000193;
    for i in range(len(myStr)):
        hval ^= ord(myStr[i])
        hval = hval * FNV_prime
    #return hash1
    return hval


def main():
    x = hashTable(11)                               #starting low proves to be more effective over 400,000 words
    f = open('word3.txt', 'r')
    for line in f:
        x.insert(line.rstrip())
        #x.booleanSet(line.rstrip(), fnv64(line.rstrip))

    # #print('\n')
    # for num in range(x.size):
    #     print(x[num].value, " | ", x[num].key, " | ", x[num].deleted)

    # print('\nload: ',x.floatLoad(), ' size: ', x.size, " current: ", x.current, "\n")



if __name__ == '__main__':
    start_time = time.time()
    main()

    print("--- %s seconds ---" % (time.time() - start_time))






    # def fnvHash(myStr):            #FNV 32A implementation for hashing
    #     offsetBasis = 0x811c9dc5;
    #     hval = offsetBasis;
    #     for i in range(len(myStr)):
    #         hval ^= ord(myStr[i])
    #         hval += (hval << 1) + (hval << 4) + (hval << 7) + (hval << 8) + (hval << 24);
    #
    #     return hval >> 0
    #
    #
    # # def encodeToBytes(b):
    # #     bytesThing = b.encode("ascii")
    #
    # def fnv64(data):
    #     hash_ = 0xcbf29ce484222325
    #     for b in data:
    #         hash_ *= 0x100000001b3
    #         hash_ &= 0xffffffffffffffff
    #         hash_ ^= b
    #     return hash_
