from bs4 import BeautifulSoup
import requests

if __name__ == '__main__':
    base_url = 'https://sollux.pl/'

    product_links = []
    for x in range(0, 8):
        r = requests.get(f'https://sollux.pl/pl/menu/kinkiety-152?counter={x}')
        soup = BeautifulSoup(r.content, 'lxml')

        wall_lamp_list = soup.find_all('div',
                                       class_='product col-6 col-sm-4 pt-3 '
                                              'pb-md-3')

        headers = {'UserAgent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                                'AppleWebKit/537.36 '
                                '(KHTML, like Gecko) Chrome/72.0.3626.121 '
                                'Safari/537.36'}

        for item in wall_lamp_list:
            for link in item.find_all('a', href=True):
                product_links.append(base_url + link['href'])
                break

        for link in product_links:
            r = requests.get(link, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')

            name = soup.find('h1',
                             class_='product_name__name m-0').text.strip()
            price = soup.find('strong',
                              class_='projector_prices__price').text.strip()
            # specifications = soup.find('section', class_='dictionary
            # col-12 mb-1 ' 'mb-sm-4').find_all("span",
            # class_='dictionary__name_txt')

            dicionary_name = soup.find_all('span',
                                           class_='dictionary__name_txt')
            dictionary_value = soup.find_all('span',
                                             class_='dictionary__value_txt')

            # for i in range(0, len(specifications)):
            #     print(specifications[i].text.strip())
            print()
            wall_lamp = {
                'Nazwa': name,
                'Cena': price
            }

    print(f'Number of wall lamps: {len(product_links)}')
