class item:
    def __init__(self, id, link=None, name=None, desc=None, price=None ,date=None, address=None, tags=None) -> None:
        self._id = id
        self._name = name
        self._link = link
        self._desc = desc
        self._price = price
        self._date = date
        self._address = address
        self._tags = tags

    def get_id(self):
        return self._id
    def get_name(self):
        return self._name
    def get_link(self):
        return self._link
    def get_desc(self):
        return self._desc
    def get_price(self):
        return self._price
    def get_date(self):
        return self._date
    def get_address(self):
        return self._address
    def get_tags(self):
        return self._tags
    
    def set_name(self, name):
        self._name = name
    def set_link(self, link):
        self._link = link
    def set_desc(self, desc):
        self._desc = desc
    def set_price(self, price):
        self._price = price
    def set_date(self, date):
        self._date = date
    def set_address(self, address):
        self._address = address
    def set_tags(self, tags):
        self._tags = tags


    def same(self, other) -> bool:
        if isinstance(other,item):
            return other.get_id() == self.get_id()
        return False

    def to_dict(self) ->dict:
        aditem = dict()
        aditem['arcticle_id'] = self._id
        aditem['arcticle_name'] = self._name
        aditem['arcticle_link'] = self._link
        aditem['arcticle_price'] = self._price
        aditem['arcticle_date'] = self._date      
        aditem['arcticle_desc'] = self._desc
        aditem['arcticle_address'] = self._address
        aditem['arcticle_tags'] = self._tags
        return aditem

    def __eq__(self, __o) -> bool:
        if isinstance(__o, item):
            return __o.get_id() == self.get_id() and \
                __o.get_name() == self.get_name() and \
                    __o.get_link() == self.get_link() and \
                        __o.get_desc() == self.get_desc() and \
                            __o.get_price() == self.get_price() and \
                                __o.get_date() == self.get_date() and \
                                    __o.get_address() == self.get_address() and \
                                        __o.get_tags() == self.get_tags()
        return False

    def __str__(self) -> str:
        return str(self._name) + ' - ' + str(self._address) + ' - ' + str(self._price) +'\n' + str(self._link)

    def __hash__(self) -> int:
        return hash(str(self._id) + str(self._address) + str(self._date) + str(self._desc) + \
                    str(self._link) + str(self._name) + str(self._price) + str(self._tags)) 