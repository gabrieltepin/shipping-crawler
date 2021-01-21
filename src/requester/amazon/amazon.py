import requests
from bs4 import BeautifulSoup
from requester import shipping_item

class AmazonRequest:
    def __init__(self, search):
        self.parameters = {
            '__mk_pt_BR': '%C3%85M%C3%85%C5%BD%C3%95%C3%91', # dunno, maybe tells it is to look up to BR results
            'i':'aps', # dunno
            'k': search, # tells what to search to
            's': 'relevanceblender', #this can be for price ordered or date ordered though, just need to check url parameter at the site
            'ref': 'nb_sb_noss_1', # dunno
            'url': 'search-alias=aps' # dunno
        }

        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,fr;q=0.6',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        }

        self.items = []

    def getPriceText(self, item):
        for index, text in enumerate(item):
            if 'R$' in text:
                priceText = text.split('R$')[1]
                priceText = priceText.replace(",", ".")
                return (priceText, index)
        return ("",0)

    def getShippingCost(self, item):
        for text in item:
            if 'frete' in text:
                if any(char.isdigit() for char in text):
                    costText = text.split()
                    cost = costText[0].split('R$')[1]
                    cost = cost.replace(",", ".")
                    return cost
        return '0'

    def getItems(self):
        try:
            response = requests.get('https://www.amazon.com.br/s?', headers=self.headers, params=self.parameters, timeout=0.8)
            response.raise_for_status()
            print(response)

            soup = BeautifulSoup(response.content, "html.parser")

            for div in soup.find_all('div', attrs={"data-index": True}):
                divText = div.text.splitlines()
                item = list(filter(lambda x: x != '', divText))

                price, index = self.getPriceText(item)
                shippingCost = self.getShippingCost(item)

                if(price != ""):
                    replies = "No replies"
                    if (all((char.isdigit() or char == '.') for char in item[index-1])):
                        replies = str(item[index-1])
                        index -= 1

                    rating = "No rating"
                    if ('estrelas' in item[index-1]):
                        rating = str(item[index-1])
                        index-=1

                    title = "".join(str(string)+' ' for string in item[:index])

                    totalPrice = float(price) + float(shippingCost)

                    self.items.append(shipping_item.Item(title, rating, replies, price))

        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        return self.items
