from bs4 import BeautifulSoup
import requests
import json
import re
import codecs


def main():
    iter_link()


def iter_link():
    base_url = 'https://sollux.pl/'

    product_links = []
    f = codecs.open('result.json', 'w', 'utf8')
    f.write('[')

    for x in range(0, 8):
        r = requests.get(f'https://sollux.pl/pl/menu/kinkiety-152?counter={x}')
        soup = BeautifulSoup(r.content, 'lxml')

        wall_lamp_list = soup.find_all('div',
                                       class_='product col-6 col-sm-4 pt-3 '
                                              'pb-md-3')

        # headers = {'UserAgent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
        #                         'AppleWebKit/537.36 '
        #                         '(KHTML, like Gecko) Chrome/72.0.3626.121 '
        #                         'Safari/537.36'}

        for item in wall_lamp_list:
            for link in item.find_all('a', href=True):
                product_links.append(base_url + link['href'])
                break

        for link in product_links:
            print(f'Page link: {link}')
            json_obj = json.dumps(product_to_dict(link), indent=4)
            f.write(json_obj)
            f.write(',\n')

    print(f'Number of wall lamps: {len(product_links)}')
    f.write()
    f.close()

def product_to_dict(link: str) -> dict:
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html.parser')

    name = soup.find('h1',
                     class_='product_name__name m-0').text.strip()
    price = soup.find('strong',
                      class_='projector_prices__price').text.strip()

    param_names = soup.find_all(class_='dictionary__name_txt')

    param_values = soup.find_all(class_='dictionary__value_txt')

    wall_lamp = {
        'Nazwa': name,
        'Cena': price,
        'Parametry techniczne': {}
    }

    dict_list = []
    for param_name, param_value in zip(param_names, param_values):
        tmp_name = param_name.text.strip()
        tmp_value = param_value.text.strip()
        if tmp_name in ['Wykonanie', 'Kolor']:
            wall_lamp['Parametry techniczne'][tmp_name] = re.split(
                ', |/', tmp_value)
        else:
            wall_lamp['Parametry techniczne'][
                param_name.text.strip()] = \
                tmp_value

    print(wall_lamp)
    return wall_lamp


if __name__ == '__main__':
    main()
