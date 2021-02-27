# sms_login

This is a module for ODOO. Currently, it is tested in ODOO13. However, it should work for other versions as well. Let me know if it works for other versions so that I can update the information here.

In order to enable the support, you need to have an web SMS account and update the information in the controllers/controller.py. Please looging for the send_sms function and update the http request there for your account. Currently, it works for a SMS provider(簡訊王) in Taiwan. We may need to modify it to support the SMS gateway in the ODOO. However, it is hard-coded right now.

TODO
* Support ODOO SMS gateway
* Make the SMS message can be customized in the UI.
