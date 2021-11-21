from Item import item

class cache:
    def __init__(self, capacity:int) -> None:
        self._capacity = capacity
        self._list = list()
        self._head = 0
        self._init_list()

    def _init_list(self):
        for i in range(self._capacity):
            self._list.append(None)

    def add(self, item:item):
        if self._head == self._capacity:
            self._head = 0
        index = self._head % self._capacity
        self._list[index] = item
        self._head +=1
    
    def isin(self, aditem:item) -> item:
        for i in range(len(self._list)):
            if aditem.same(self._list[i]):
                return self._list[i]
        return None
    
    def replace(self, old, new):
        for i in range(len(self._list)):
            if self._list[i] == old:
                self._list[i] = new
                return

    def get_queue(self) -> list:
        return self._list

    def to_dict(self) -> dict:
        c = dict()
        for i in self._list:
            if isinstance(i, item):
                c['aditem_'+str(i.get_id())] = i.to_dict()
        return c