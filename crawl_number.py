import json
from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup


def is_prime(num):
    if num > 1:
        # check for factors
        for i in range(2, num):
            if (num % i) == 0:
                return False
                break
        else:
            return True


def get_pow(number, num_id):
    url2 = "http://aisnumber.wisdomcloud.net/api/request2.php?tel={number}".format(number=number)
    r = requests.request("GET", url2)
    re = r.json()
    chart = re['data']['chart']
    power = chart['pw1'] + chart['pw2'] + chart['pw3'] + chart['pw4'] + chart['pw5'] + chart['pw6']
    return {
        'id': num_id,
        'number': number,
        'power': power,
        'chart': [chart['pw1'], chart['pw2'], chart['pw3'], chart['pw4'], chart['pw5'], chart['pw6']]
    }


def get_detail(num_id):
    print(num_id)
    try:
        url = "https://become-ais-family.ais.co.th/select-number/{num}".format(num=num_id)
        r = requests.request("GET", url)
        soup = BeautifulSoup(r.text, 'html.parser')
        e = soup.find("div", {"class": "num_txt_packtel"})
        phone_number = e.get_text().replace('-', '')
        score = soup.find("div", {"class": "num_txt_packsum"}).find("b").get_text()
        detail = get_pow(phone_number, num_id)
        detail['preview_link'] = "http://decoder.ais.co.th/decoder-number?tel={}".format(phone_number)
        detail['buy_link'] = "https://become-ais-family.ais.co.th/select-number/{}".format(num_id)
        all_numbers[phone_number] = detail
        with open("number.txt", "a") as f:
            f.write(json.dumps(detail) + '\n')
            f.flush()
        return detail
    except Exception as e:
        pass
    return None


if __name__ == '__main__':
    all_numbers = {}
    start = 230000
    end = 300000
    p = Pool(8)
    details = p.map(get_detail, range(start, end))
