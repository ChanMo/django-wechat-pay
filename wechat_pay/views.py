import time
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic.base import View
from django.core.urlresolvers import reverse
from django.conf import settings
import xmltodict
from wechat_member.views import WxMemberView
from .api import Pay as PayApi

class PayView(View):
    """
    wechat base pay view
    receive post data: order_id, price, title, notify_url, redirect_url
    ..remove WxMemberView
    """
    def get(self, request, *args, **kwargs):
        try:
            order_id = request.GET['order_id']
            price = request.GET['price']
            notify_url = request.GET['notify_url']
            redirect_url = request.GET['redirect_url']
            openid = request.GET['openid'] # get instead
        except KeyError:
            return HttpResponse("PARAM ERROR")

        out_trade_no = str(int(time.time())) + str(order_id)
        total_fee = str(int(float(price) * 100))
        param = {
            'xml': {
                #'openid': request.session['wx_member']['openid'],
		        'openid': openid,
                'body': settings.WECHAT[0]['body'],
                'out_trade_no': out_trade_no,
                'total_fee': total_fee,
                'spbill_create_ip': request.META['REMOTE_ADDR'],
                'notify_url': notify_url,
            }
        }
        pay = PayApi()
        pay.set_prepay_id(param)
        data = {
            'data': pay.get_pay_data(),
            'redirect_uri': redirect_url,
        }
        return render(request, 'wechat_pay/pay.html', data)


class WxPayNotifyView(View):
    """
    Receive wechat service data
    valid and send order_id, pay_number to notify_url
    """
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(WxPayNotifyView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pay = PayApi()
        data = request.body
        data = dict(xmltodict.parse(data)['xml'])
        result = {}
        sign = data['sign']
        del data['sign']
        #check_sign = wx.get_sign(data)
        if sign:
            order_id = data['out_trade_no'][10:]
            pay_number = data['transaction_id']
            result = handle_order(order_id, pay_number)
        else:
            result['return_code'] = 'FAIL'
            result['return_msg'] = 'ERROR'

        result_xml = pay.dict_to_xml(result)
        return HttpResponse(result_xml)

    def handle_order(self, order_id, pay_number):
        """ Need user extends, for order """
        return {'return_code':'SUCCESS','return_msg':'OK'}
