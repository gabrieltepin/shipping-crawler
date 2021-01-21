class Item:
    def __init__(self, title, rating, replies, price):
        self.rating = rating
        self.replies = replies
        self.title = title
        self.price = price

    def __str__(self):
        return '%s\nrating: %s\nreplies: %s\nprice: %s\n' % (self.title,self.rating, self.replies, self.price)