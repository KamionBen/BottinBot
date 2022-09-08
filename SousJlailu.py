import json.decoder

import requests


class SousJlailu:
    def __init__(self, name, category=None, lang=None, restrictions=None, subscribers=None, description=None):
        self.name = name
        self.about = f'http://www.reddit.com/{name}/about.json'

        self.category = category
        self.lang = lang  # 'fr' or 'bi'
        self.restrictions = restrictions  # 'public', 'pivate' or 'banned'

        self.subscribers = subscribers

        self.description = description

    def get_subscribers(self):  # TODO : Static
        """ Return a readable version of the subscribers number """
        if self.subscribers > 1000000:
            return f"{round(self.subscribers / 1000000, 2)}M"
        elif self.subscribers > 1000:
            return f"{round(self.subscribers / 1000)}k"
        else:
            return self.subscribers

    def update(self):  # TODO Mettre ailleurs
        response = requests.get(self.about)
        try:
            file = response.json()
            self.subscribers = file['data']['subscribers']
            return True
        except KeyError:
            file = response.json()
            if file['error'] == 429:
                pass
            elif file['error'] == 404 and self.restrictions != 'banned':
                print(f"{self} : Previous restriction '{self.restrictions}' set to 'banned'")
                self.restrictions = 'banned'
            elif file['error'] == 403 and self.restrictions != 'private':
                print(f"{self} : Previous restriction '{self.restrictions}' set to 'private'")
                self.restrictions = 'private'
            else:
                print(file['error'])
            return False
        except json.decoder.JSONDecodeError:
            print(f"JSONDecodeError : {self}")

    def dict(self):
        return {self.name: {'category': self.category,
                            'description': self.description,
                            'lang': self.lang,
                            'restrictions': self.restrictions,
                            'subscribers': self.subscribers}}

    def list(self):
        """ 0: name, 1: category, 2: lang, 3: restrictions, 4: subscribers, 5: description """
        return [self.name, self.category, self.lang, self.restrictions, self.subscribers, self.description]

    def __repr__(self):
        return self.name


class SousJlailuGroup:
    def __init__(self, *args):
        self.sousjlailus = [sub for sub in args]

    def add(self, sousjlailu):
        # TODO check if the sub already exists
        if type(sousjlailu) == SousJlailu:
            self.sousjlailus.append(sousjlailu)
        else:
            raise TypeError("sousjlailu must be a SousJlailu object")

    def __iter__(self):
        return iter(self.sousjlailus)


if __name__ == '__main__':
    france = SousJlailu("r/france", lang="bi", restrictions="public", category="france")
    rance = SousJlailu("r/rance")

    group = SousJlailuGroup(france, rance)

    print(france.dict().items())