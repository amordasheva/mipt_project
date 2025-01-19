import uuid
from datetime import datetime, timedelta

class Hub:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Hub, cls).__new__(cls)
            cls.__instance._items = []
            cls.__instance._date = datetime.now()
            cls.__instance._initialized = False
        return cls.__instance

    def __init__(self):
        if not self._initialized:
            self._items = []
            self._date = datetime.now()
            self._initialized = True

    def getitem(self, index):
        return self._items[index]

    def __len__(self):
        return len(self._items)

    def __str__(self):
        return f"Hub (date: {self._date.strftime('%Y-%m-%d %H:%M:%S')}, items count: {len(self)})"

    def __repr__(self):
        items_repr = ", ".join(repr(item) for item in self._items[:3])
        return f"Hub (date: {self._date.strftime('%Y-%m-%d %H:%M:%S')}, items: [{items_repr}])"

    def find_by_id(self, item_id):
        for i, item in enumerate(self._items):
            if item._id == item_id:
                return i, item
        return -1, None

    def has_all_tags(self, tags):
        for item in self._items:
            if item.has_all_tags(tags):
                return True
        return False

    def find_by_tags(self, tags):
        return [item for item in self._items if item.has_all_tags(tags)]

    def remove_item(self, item_or_id):
        if isinstance(item_or_id, Item):
            try:
                self._items.remove(item_or_id)
                return True
            except ValueError:
                return False
        elif isinstance(item_or_id, uuid.UUID):
            for item in self._items:
                if item._id == item_or_id:
                    self._items.remove(item)
                    return True
        else:
            raise TypeError("Item_or_id must be an Item object or a UUID.")
        return False

    def drop_items(self, items):
        for item in items:
            self.remove_item(item)

    def clear(self):
        self._items.clear()

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        if isinstance(value, datetime):
            self._date = value
        else:
            raise TypeError("Date must be a datetime object.")

    def find_by_date(self, *dates):
        if len(dates) == 1:
            date = dates[0]
            return [item for item in self._items if item.ship_date <= date]
        elif len(dates) == 2:
            start_date, end_date = dates
            return [item for item in self._items if start_date <= item.ship_date <= end_date]
        else:
            raise ValueError("Find_by_date accepts 1 or 2 date arguments.")

    def add_item(self, item):
        if isinstance(item, Item):
            self._items.append(item)
        else:
            raise TypeError("Item must be an Item object or its subclass.")

    def find_most_valuable(self, amount=1):
        sorted_items = sorted(self._items, key=lambda item: item.cost, reverse=True)
        return sorted_items[:amount]

class Item:
    def __init__(self, name, description, ship_date, tags=None, cost=0):
        self._id = uuid.uuid4()
        self.name = name
        self.description = description
        self.ship_date = ship_date
        self._tags = set(tags) if tags else set()
        self._cost = cost

    def __repr__(self):
        return f"Item(name={self.name}, cost={self.cost})"

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, value):
        if isinstance(value, (int, float)) and value >= 0:
            self._cost = value
        else:
            raise ValueError("Cost must be a non-negative number.")

    def __lt__(self, other):
        if not isinstance(other, Item):
            raise TypeError("Can only compare Item objects.")
        return self.cost < other.cost

    def add_tag(self, tag):
        self._tags.add(tag)

    def remove_tag(self, tag):
        self._tags.discard(tag)

    def has_all_tags(self, tags):
        return self._tags.issuperset(tags)

    def __str__(self):
        tags_str = ", ".join(self._tags) if self._tags else "No tags"
        return (f"Item:\n"
                f"  ID: {self._id}\n"
                f"  Name: {self.name}\n"
                f"  Description: {self.description}\n"
                f"  Shipment Date: {self.ship_date.strftime('%Y-%m-%d')}\n"
                f"  Tags: {tags_str}\n"
                f"  Cost: {self.cost} RUB")

    def __len__(self):
        return len(self._tags)

    def copy(self) -> 'Item':
        return Item(
            name=self.name,
            description=self.description,
            ship_date=self.ship_date,
            tags=self._tags.copy(),
            cost=self.cost
        )



hub = Hub()

hub.clear()

items = [
    Item("Car", "A toy for racing, blue", datetime.now() + timedelta(days=1), cost=1500),
    Item("Doll", "A beautiful doll in a red dress", datetime.now() - timedelta(days=1), cost=5000),
    Item("Train", "A green train on rails", datetime.now(), cost=10000),
    Item("Board game", "A board game for children from 5 to 8 years old", datetime.now() + timedelta(days=2), cost=1200),
    Item("House", "A house for Barbies, pink", datetime.now() + timedelta(days=5), cost=30000),
    Item("Bear", "A brown bear", datetime.now(), cost=1200),
    Item("Fox", "A red fox", datetime.now() + timedelta(days=2), cost=1000),
]

for item in items:
    hub.add_item(item)

B = [item for item in hub.find_by_tags([]) if item.name.lower().startswith('b')]
hub.drop_items(B)

Outdated = hub.find_by_date(hub.date)
hub.drop_items(Outdated)

MostValuable = hub.find_most_valuable(10)
hub.drop_items(MostValuable)

Others = hub.find_by_tags([])

print("Starting with B:", B)
print("Outdated:", Outdated)
print("MostValuable:", MostValuable)
print("Others:", Others)