from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()

# Позитивный тест GET API key
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):

    status, result = pf.get_api_key(email, password)

    assert status == 200
    assert 'key' in result

# Негативный тест GET API key
# Загружаем недействительные регистрационные данные
def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result

# Позитивный тест GET API pets
def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

# Негативный тест GET API pets
# загружаем недействительные регистрационные данные
def test_get_all_pets_with_invalid_key(filter=''):

    _, auth_key = pf.get_api_key(invalid_email, invalid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 403
    assert 'key' not in result

# Позитивный тест POST API (1) add information about new pet with photo
def test_add_new_pet_with_valid_data(name='кот', animal_type='коты',
                                     age='1', pet_photo='images/1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname('images'), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

# Позитивный тест POST API(2)add information about new pet with photo
def test_add_new_pet_with_valid_data(name='pet', animal_type='pets',
                                     age='2', pet_photo='images/2.jpg'):

    pet_photo = os.path.join(os.path.dirname('images'), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name

# Негативный тест POST API (1) add information about new pet with photo
# Загружаем недействительные регистрационные данные
def test_add_new_pet_with_invalid_key(name='pet', animal_type='pets',
                                     age='2', pet_photo='images/2.jpg'):

    auth_key = pf.get_api_key(invalid_email, invalid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 403
    assert result['name'] != name

# Негативный тест POST API (2) add information about new pet with photo
# Загружаем неподдерживаемый формат фото
def test_add_new_pet_with_invalid_photo(name='pet', animal_type='pets',
                                     age='2', pet_photo='images/питомц.csv'):

    auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 403
    assert result['name'] != name

# Позитивный тест POST API add information about new pet without photo
def test_add_new_pet_without_photo(name='кот_без_фото', animal_type='коты_без_фото',
                                     age='1'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

# Негативный тест POST API add information about new pet without photo
# загружаем недействительные регистрационные данные
def test_neg_add_new_pet_without_photo(name='кот_без_фото', animal_type='коты_без_фото',
                                     age='1'):

    auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 403
    assert result['name'] != name


# Позитивный тест DELETE API delete pet from database
def test_successful_delete_self_pet():
    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "pet", "pets", "2", "images/2.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

# Негативный тест DELETE API delete pet from database
# загружаем недействительные регистрационные данные
def test_negative_delete_self_pet():

    _, auth_key = pf.get_api_key(invalid_email, invalid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "pet", "pets", "2", "images/2.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)


    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 403
    assert pet_id not in my_pets.values()

# Позитивный тест PUT API update information about new pet
def test_successful_update_self_pet_info(name='кот', animal_type='коты', age=1):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

# Негативный тест PUT API update information about new pet
# загружаем недействительные регистрационные данные
def test_negative_update_self_pet_info(name='кот', animal_type='коты', age=3):
    _, auth_key = pf.get_api_key(invalid_email, invalid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 403
        assert result['name'] != name
    else:
        raise Exception("There is no my pets")