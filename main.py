import csv, datetime, time, json
import os.path
from os.path import getmtime
from SousJlailu import SousJlailu
from ImageGenerator import *

DIRNAME = os.path.dirname(__file__)


def import_spreadsheet(annuaire):
    """ Import the data from u/CitoyenEuropeen spreadsheet """

    file_time = datetime.date.fromtimestamp(getmtime(annuaire))
    updated_time = file_time.strftime("%Y-%m-%d")

    print(f"Import '{annuaire}' (Last updated : {updated_time})")

    sousjlailus = []  # List of SousJlailu objects

    sub_number = 0

    with open(annuaire, 'r') as file:

        reader = csv.reader(file, delimiter=',')

        for row in reader:
            category = row[1]
            name = row[4]
            description = row[7]
            restrictions = row[13]
            lang = row[14]
            if len(name) > 2:  # Ignore empty lines
                sousjlailus.append(SousJlailu(name,
                                              category=category,
                                              lang=lang,
                                              restrictions=restrictions,
                                              description=description))
                sub_number += 1

    # Sort the list
    sousjlailus.sort(key=lambda sub: sub.name.lower())

    print(f"Subreddits loaded : {len(sousjlailus)}/{sub_number}")
    return sousjlailus


def dict_to_object(sub_dict):
    sub_list = []
    for name, data in sub_dict.items():
        sub_list.append(SousJlailu(name,
                                   category=data['category'],
                                   description=data['description'],
                                   lang=data['lang'],
                                   restrictions=data['restrictions'],
                                   subscribers=data['subscribers']))
    return sub_list


def object_to_dict(sub_list):
    sub_dict = {}
    for sub in sub_list:
        sub_dict[sub.name] = {'category': sub.category,
                              'description': sub.description,
                              'lang': sub.lang,
                              'restrictions': sub.restrictions,
                              'subscribers': sub.subscribers}
    return sub_dict


def create_todays_annuaire():
    """ Create annuaire.json from the subreddits list """
    """ Fetch the subscribers number and loop until it's done"""
    start = time.time()
    date = datetime.date.today().strftime("%Y-%m-%d")
    annuaire_filename = os.path.join(DIRNAME, 'export', date, 'annuaire.json')

    if os.path.isfile(annuaire_filename) is False:
        # 'annuaire.json' doesn't exists, create and fill it

        os.makedirs(os.path.join(DIRNAME, 'export', date))
        with open(annuaire_filename, 'w') as annuaire_file:
            annuaire_file.write(json.dumps(object_to_dict(import_spreadsheet('FG-Network - r_annuaire.csv')), indent=4))

    continuer = True

    while continuer:
        sub_to_update = 0
        with open(annuaire_filename, 'r') as annuaire_file:
            annuaire = json.load(annuaire_file)

        sub_list = dict_to_object(annuaire)
        for sub in sub_list:
            if type(sub.subscribers) is not int and sub.restrictions.lower() == 'public':
                if sub.update() is False:
                    sub_to_update += 1

        new_annuaire = object_to_dict(sub_list)
        elapsed = time.time() - start
        print(f"Subreddits to update : {sub_to_update}. Saving file. "
              f"Time elapsed : {int(elapsed//60)}m{int(elapsed%60)}s")
        with open(annuaire_filename, 'w') as annuaire_file:
            annuaire_file.write(json.dumps(new_annuaire, indent=4))

        if sub_to_update == 0:
            continuer = False


if __name__ == '__main__':

    create_todays_annuaire()
    date = datetime.date.today().strftime("%Y-%m-%d")

    with open(f'export/{date}/annuaire.json', 'r') as file:
        sub_list = dict_to_object(json.loads(file.read()))

    new_list = [sub for sub in sub_list if type(sub.subscribers) == int]
    new_list.sort(key=lambda sub: sub.subscribers, reverse=True)

    bi_list = []
    fr_list = []
    for sub in new_list:
        if sub.lang == 'bi' and len(bi_list) < 10:
            bi_list.append(sub)
        if sub.lang == 'fr' and len(fr_list) < 10:
            fr_list.append(sub)
    date_txt = datetime.date.today().strftime("%d-%m-%Y")
    generate_image(bi_list, 'Top 10 des sousjlailus bilingues', date_txt, f'export/{date}/top10_bi.png', panel=1)
    generate_image(fr_list, 'Top 10 des sousjlailus francophones', date_txt, f'export/{date}/top10_fr.png', panel=2)






