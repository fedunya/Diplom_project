import csv
import os

__all__ = ['create_csv', 'add_data']

def create_csv():
    names_col = ['offer_id', 'price', 'date_time', 'room', 'square',
                 'floor', 'all_floors', 'first/last', 'district']
    with open('realty_dataset.csv', 'w', encoding='utf-8') as f:
        create = csv.writer(f, delimiter=';', lineterminator='\r')
        create.writerow(names_col)

def add_data(offer):
    distric = {'р-н Ворошиловский': 1, 'р-н Железнодорожный': 2, 'р-н Кировский': 3,
               'р-н Ленинский': 4, 'р-н Октябрьский': 5, 'р-н Первомайский': 6,
               'р-н Пролетарский': 7, 'р-н Советский': 8, 'без района': 0}
    data = {}
    data['offer_id'] = offer['offer_id']
    data['price'] = offer['price']
    data['date_time'] = offer['date_time']
    offer['title'] = offer['title'].replace(',', '.')
    if offer['title'].split(' ')[0].split('-')[0].isdigit() or offer['title'].split(' ')[0] == 'Доля':
        data['room'] = offer['title'].split(' ')[0].split('-')[0]
        data['square'] = float(offer['title'].split(' ')[2])
        data['floor'] = offer['title'].split(' ')[4].split('/')[0]
        data['all_floors'] = offer['title'].split(' ')[4].split('/')[1]
    elif offer['title'].split(' ')[0] == 'Аукцион:':
        data['room'] = offer['title'].split(' ')[1].split('-')[0]
        data['square'] = float(offer['title'].split(' ')[3])
        data['floor'] = offer['title'].split(' ')[5].split('/')[0]
        data['all_floors'] = offer['title'].split(' ')[5].split('/')[1]
    elif offer['title'].split(' ')[0] == 'Квартира-студия.':
        data['room'] = 1
        data['square'] = float(offer['title'].split(' ')[1])
        data['floor'] = offer['title'].split(' ')[3].split('/')[0]
        data['all_floors'] = offer['title'].split(' ')[3].split('/')[1]
    elif offer['title'].split(' ')[0] == 'Своб.':
        data['room'] = 1
        data['square'] = float(offer['title'].split(' ')[2])
        data['floor'] = offer['title'].split(' ')[4].split('/')[0]
        data['all_floors'] = offer['title'].split(' ')[4].split('/')[1]
    else: pass
    if data['floor'] == data['all_floors'] or data['floor'] == '1':
        data['first/last'] = 1
    else:
        data['first/last'] = 0
    data['district'] = distric[offer['district']]
    
    with open('realty_dataset.csv', 'a', encoding='utf-8') as f:
        write = csv.DictWriter(f, delimiter=';', lineterminator='\r', fieldnames=data.keys())
        write.writerow(data)
    return data['square']

def main():
    current_directory = os.getcwd()
    if not os.path.exists(current_directory + '/realty_dataset.csv'):
        create_csv()

if __name__ == '__main__':
    main()