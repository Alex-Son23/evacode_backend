import hashlib
import json
from pprint import pprint
from django.db.utils import IntegrityError
from urllib.parse import urlencode
import requests
from datetime import datetime
from django.utils.timezone import make_aware

from django.core.serializers import serialize
from .serializers import GoodsSerializer

from .models import ImageModel, GroupOfGoods, GoodsModel

from dotenv import load_dotenv
import os

load_dotenv()


class BusinessRuAPIClient:
    api_secret = os.getenv('API_SECRET')
    app_id = os.getenv('APP_ID')
    base_url = 'https://a46291.business.ru/api/rest'
    token = ''
    app_psw = ''

    def __init__(self):
        self.repair_hash = self.get_hash(params={'app_id': self.app_id})
        self.set_token()

    def set_token(self) -> None:
        response = requests.get(f'{self.base_url}/repair.json?app_id={self.app_id}&app_psw={self.repair_hash}')
        data = dict(json.loads(response.content))
        self.token = data['token']
        self.app_psw = data['app_psw']

    def get_hash(self, params: dict, token='') -> str:
        params = dict(sorted(params.items()))
        hashed = hashlib.md5((token + self.api_secret + urlencode(params)).encode()).hexdigest()
        return hashed

    def get_goods_group(self) -> list:
        params = {'app_id': self.app_id}
        hashed = self.get_hash(params=params, token=self.token)
        response = requests.get(f'{self.base_url}/groupsofgoods.json?app_id={self.app_id}&app_psw={hashed}')
        # print(response.content)
        data = dict(json.loads(response.content))
        # pprint(data)
        return data['result']

    def get_goods(self, page: int = 1, with_remains: int = 1, filter_positive_free_remains: int = 1,
                  with_prices: int = 1, filter_positive_remains: int = 1, archive: int = 0) -> list[dict]:
        params = {
            'app_id': self.app_id,
            'page': page,
            'with_prices': with_prices,
            'with_remains': with_remains,
            'filter_positive_free_remains': filter_positive_free_remains,
            'filter_positive_remains': filter_positive_remains,
            'archive': archive,
        }
        hashed = self.get_hash(params=params, token=self.token)
        response = requests.get(f'{self.base_url}/goods.json?{urlencode(params)}&app_psw={hashed}')
        # print(response.content)
        data = dict(json.loads(response.content))
        return data['result']


# c = BusinessRuAPIClient()
# all_prod_rem = []
# all_prod_free_rem = []
# for i in range(1, 100):
#     n = c.get_goods(i)
#     # print(not n, n)
#     print(len(n))
#     if not n:
#         print(i)
#         break
#     all_prod_rem.extend(n)
# pprint(all_prod_rem[0])


class BusinessRuService:
    def __init__(self):
        self.api_client = BusinessRuAPIClient()

    def group_to_model(self):
        group_data = self.api_client.get_goods_group()
        for group in group_data:
            datestr = group["updated"][:19] if len(group["updated"]) >= 21 else group["updated"]
            # print('______________________________________________________\n'
            #       f'{datestr}\n'
            #       '______________________________________________________')
            datetime_object = datetime.strptime(datestr, '%d.%m.%Y %H:%M:%S')
            updated_aware = make_aware(datetime_object)
            # print(datetime_object, group['updated'])
            try:
                g = GroupOfGoods.objects.create(id=int(group['id']),
                                                default_order=group['default_order'],
                                                deleted=group['deleted'],
                                                description=group['description'],
                                                name=group['name'],
                                                parent_id_id=group['parent_id'],
                                                updated=updated_aware)
                g.save()
                # updated=group['updated'])
            except IntegrityError:
                pass
            # print(group['images'])
            if group['images']:
                for image in group['images']:
                    image_object = ImageModel.objects.get_or_create(
                        name=image['name'],
                        url=image['url'],
                        sort=image['sort'],
                        group_id=group['id']
                    )
                    if not (isinstance(image_object, tuple)):
                        image_object.save()

    def goods_to_model(self):
        page = 1
        while True:
            goods_data = self.api_client.get_goods(page=page)
            if not goods_data:
                break
            for good in goods_data:
                defaults = {
                    'id': good['id'],
                    'title': good['full_name'],
                    'description': good['description'],
                    'category_id': good['group_id'],
                    'type': good['type'],
                    'stock': float(good['remains'][0]['amount']['total'])
                }
                # print(good['id'], float(good['remains'][0]['amount']['total']))

                for price in good['prices']:
                    match price['price_type']['name']:
                        case 'Оптовая Цена':
                            defaults['wholesale_price'] = price['price']
                        case 'Крупный опт':
                            defaults['large_wholesale_price'] = price['price']
                        case 'Официальная Цена':
                            defaults['official_price'] = price['price']
                        case 'Розничная Цена':
                            defaults['retail_price'] = price['price']
                        case _:
                            pass

                # print(defaults)

                obj, created = GoodsModel.objects.update_or_create(id=int(good['id']), defaults=defaults,
                                                                   create_defaults=defaults)
                if created:
                    obj.save()

                if good['images']:
                    for image in good['images']:
                        image_object = ImageModel.objects.get_or_create(
                            name=image['name'],
                            url=image['url'],
                            sort=image['sort'],
                            good_id=good['id']
                        )
                        if not (isinstance(image_object, tuple)):
                            image_object.save()
                # print(obj, created)
                # except:
                #     pass
            page += 1
            goods_to_delete = GoodsModel.objects.filter(stock__isnull=True) | GoodsModel.objects.filter(stock=0)

            # Удаляем найденные объекты
            # pprint(goods_to_delete)
            goods_to_delete.delete()
        print("Goods added successfully!")

    # def add_images(self, images: list, type_of_model: str) -> None:
    #
    #     if images:
    #         for image in images:
    #             if type_of_model == 'good':
    #                 data = {'good_id': image['']}
    #             image_object = ImageModel.objects.get_or_create(
    #                 name=image['name'],
    #                 url=image['url'],
    #                 sort=image['sort'],
    #                 good_id=good['id']
    #             )
    #             if not (isinstance(image_object, tuple)):
    #                 image_object.save()




# with open(r'file.json', "w", encoding='utf-8') as out:
#     mast_point = GoodsSerializer(GoodsModel.objects.all(), many=True).data
#     data = {'result': mast_point}
#     out.write(json.dumps(data, ensure_ascii=False))
