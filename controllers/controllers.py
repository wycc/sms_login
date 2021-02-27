# -*- coding: utf-8 -*-
from odoo import http
from odoo.addons.web.controllers.main import Home
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
import time
import requests
import traceback
class SmsLoginHome(Home):
      @http.route('/web/login/', type='http', auth='none')
      def web_login(self, **kw):
                try:
                        mobile = http.request.params['login']
                        users=http.request.env['res.users'].sudo().search([('partner_id.mobile','=',mobile)])
                        if len(users) > 0:
                                http.request.params['login'] = users[0].login
                except:
                        print(traceback.format_exc())
                        pass
        
                res = super(SmsLoginHome, self).web_login(kw)
                return res

class SmsLoginSignup(AuthSignupHome):

        def send_sms(self,phone,msg):
                params = {
                        'username':'xxxx',
                        'password':'#####',
                        'dstaddr':phone,
                        'smbody':msg
                }
                print("send request")
                r = requests.get("http://api.kotsms.com.tw/kotsmsapi-1.php",params=params)
                print(r.url)
                print(r.text)

        @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
        def web_auth_signup(self, *args, **kw):
                qcontext = self.get_auth_signup_qcontext()
                try:
                        mobile = qcontext.get("mobile")
                        print("mobile=%s" % mobile)
                        if mobile == '' or mobile == None:
                                return http.request.render('sms_login.signup_mobile', qcontext)        
                        try:
                                otp = int(qcontext.get("otp"))
                                sotp = http.request.session['otp']
                                print('[%s] [%s]' % (otp,sotp))
                                if otp == sotp:
                                        print('match')
                                        try:
                                                res = super(SmsLoginSignup, self).web_auth_signup(*args,**kw)
                                        except:
                                                print(traceback.format_exc())
                                                response = http.request.render('auth_signup.signup', qcontext)
                                                response.headers['X-Frame-Options'] = 'DENY'
                                                return response
                                        user = http.request.env['res.users'].sudo().search([('login','=',qcontext.get("login"))])
                                        if user:
                                                user.partner_id.mobile = qcontext.get("mobile")
                                                
                                        return res                                
                                else:
                                        print('not match')
                                        return http.request.render('sms_login.signup_otp', qcontext)        
                        except:
                                print(traceback.format_exc())
                                http.request.session['otp'] =  (int(time.time()*1000000) % 800000) +100000
                                msg = '%s Please use this code to verify the sign up page. ' %  http.request.session['otp']
                                self.send_sms(mobile,msg)

                                return http.request.render('sms_login.signup_otp', qcontext)
                except:
                        print(traceback.format_exc())
                        return http.request.render('sms_login.signup_mobile', qcontext)

        @http.route('/web/reset_password', type='http', auth='public', website=True, sitemap=False)
        def web_auth_reset_password(self, *args, **kw):
                qcontext = self.get_auth_signup_qcontext()
                if not qcontext.get('reset_password_enabled'):
                        raise werkzeug.exceptions.NotFound()
                mobile = qcontext.get("mobile")
                if mobile == '' or mobile == None:
                        return http.request.render('sms_login.reset_password',qcontext)
                try:
                        otp = int(qcontext.get("otp"))
                        sotp = http.request.session['otp']
                        print('[%s] [%s]' % (otp,sotp))
                        if otp == sotp:
                                print('match')
                                try:
                                        user = http.request.env['res.users'].sudo().search([('partner_id.mobile','=',mobile)])
                                        res={}
                                        if len(user) > 1:
                                                res['error'] = _('Duplicated phone number:')+qcontext.get('login')
                                                return http.request.render('sms_login.reset_password_otp',qcontext)
                                        elif len(user) == 0:
                                                res['error'] = 'Phone number %s is not available' % qcontext.get('login')
                                                return http.request.render('sms_login.reset_password_otp',qcontext)
                                        if qcontext.get('password') != qcontext.get('confirm'):
                                                res['error'] = 'password is not matched'
                                                return http.request.render('sms_login.reset_password_otp',qcontext)
                                        token = ""
                                        try:
                                                user.write({'password': qcontext.get('password')})
                                                http.request.env.cr.commit()	 # as authenticate will use its own cursor we need to commit the current transaction
                                                uid = http.request.session.authenticate(http.request.session.db, user.login, qcontext.get('password'))
                                                com = http.request.cr.commit()
                                                res['uid'] = uid
                                                res['com'] = com
                                                res['error'] = ''
                                        except Exception as e:
                                                res['error'] = e.message
                                        return http.redirect_with_hash("/")
                                except:
                                        print(traceback.format_exc())
                                        response = http.request.render('sms_login.reset_password_otp',qcontext)
                                        response.headers['X-Frame-Options'] = 'DENY'
                                        return response
                                user = http.request.env['res.users'].sudo().search([('login','=',qcontext.get("login"))])
                                if user:
                                        user.partner_id.mobile = qcontext.get("mobile")
                                        
                                return res                                
                        else:
                                print('not match')
                                return http.request.render('sms_login.reset_password_otp',qcontext)
                except:
                        http.request.session['otp'] =  (int(time.time()*1000000) % 800000) +100000
                        msg = '%s Please use this code to verify' %  http.request.session['otp']
                        self.send_sms(mobile,msg)
                        return http.request.render('sms_login.reset_password_otp',qcontext)


