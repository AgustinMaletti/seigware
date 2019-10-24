import pathlib

# PATH = pathlib.Path(__file__).parent
# DB_PATH = PATH.joinpath('static/db.db').resolve().__str__()

# print(DB_PATH)
# print(type(PATH.__str__()))
# print(PATH.__str__())
# print(DB_PATH.__str__())

print('hello')

PATH = pathlib.Path(__file__).parent
path_to_driver = PATH.joinpath('static/geckodriver').resolve().__str__()

print(path_to_driver)