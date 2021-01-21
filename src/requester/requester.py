from requester.amazon import amazon

class Request:
    def __init__(self, search):
        self.amazonResults = amazon.AmazonRequest(search).getItems()
        # self.magaluResults = magalu.MagaluRequest(search).getItems()
        # self.aliexpressResults = ali.AliResultsRequest(search).getItems()
        # ...

        for i in self.amazonResults:
            print(i)