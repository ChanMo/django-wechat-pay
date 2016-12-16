基于django的微信支付功能模块
============================


快速开始:
---------

安装django-wechat-pay:

.. code-block::

    pip install django-wechat-pay


修改settings.py文件:

.. code-block::

    INSTALLED_APPS = (
        ...
        'wechat',
        'wechat_pay',
        ...
    )



在settings.py文件底部添加:

.. code-block::

    # wechat config
    WECHAT = [
        {
            'appid': 'demo',
            'appsecret': 'demo',
            'token': 'demo',
            'mch_id': 'demo',
            'key': 'demo',
            'body': 'demo',
        },
    ]


版本更改:
---------
- v0.1 第一版
