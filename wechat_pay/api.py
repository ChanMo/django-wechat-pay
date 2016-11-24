from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
import time
import json
from django.conf import settings
from wechat.api import Base
import xmltodict

class Pay(Base):
    """ Pay Class """
    mch_id = ''
    key = ''
    prepay_id = ''

    def __init__(self):
        super(Pay, self).__init__()
        self.mch_id = settings.WECHAT[0]['mch_id']
        self.key = settings.WECHAT[0]['key']

    def set_prepay_id(self, data):
        data['xml'].update({
            'trade_type': 'JSAPI',
            'appid': self.appid,
            'mch_id': self.mch_id,
            'nonce_str': self.get_random(),
        })
        data['xml']['sign'] = self.get_sign(data['xml'])
        url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
        message = self.dict_to_xml(data)
        result = self.get_data(url, message, 'string')
        data = dict(xmltodict.parse(result))
        self.prepay_id = data['xml']['prepay_id']

    def get_pay_data(self):
        data = {
            'appId': self.appid,
            'timeStamp': str(int(time.time())),
            'nonceStr': self.get_random(),
            'package': 'prepay_id=%s' % self.prepay_id,
            'signType': 'MD5',
        }
        sign = {'paySign': self.get_sign(data),}
        data.update(sign)
        data = json.dumps(data)
        return data
