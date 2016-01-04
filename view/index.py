# coding:utf-8

import random
from model.user import User
from view import route, url_for, View, LoginView

Rolls = {}

@route('/', name='index')
class Index(View):
    def get(self):
        self.render()


@route('/roll_new', name='roll_new')
class RollNew(LoginView):
    def get(self):
        index = len(Rolls) + 1
        Rolls[index] = {'index': index, 'host': self.current_user().id, 'points': [], 'names': [], 'status':True}
        self.redirect(url_for('roll', index))


@route('/roll/close/(\d+)', name='roll_close')
class RollClose(LoginView):
    def get(self, index):
        index = int(index)
        if index not in Rolls:
            self.write_error(404)
        else:
            Rolls[index]['status'] = False
        self.redirect(url_for('roll', index))


@route('/roll/open/(\d+)', name='roll_open')
class RollClose(LoginView):
    def get(self, index):
        index = int(index)
        if index not in Rolls:
            self.write_error(404)
        else:
            Rolls[index]['status'] = True
        self.redirect(url_for('roll', index))


@route('/roll/(\d+)', name='roll')
class Roll(View):
    def get(self, index):
        index = int(index)
        if index not in Rolls:
            self.write_error(404)
        else:
            data = Rolls[index]
            max_point = -1

            for i in data['points']:
                if i['point'] > max_point:
                    max_point = i['point']

            self.render(data=data, author=User.get_by_pk(data['host']), max_point=max_point)

    def post(self, index):
        index = int(index)
        if index not in Rolls:
            self.write_error(404)
        else:
            data = Rolls[index]
            ip = self.request.remote_ip
            
            if data['status'] == False:
                self.messages.error('投票已关闭！')
                self.redirect(url_for('roll', index))
                return
            
            if self.current_user():
                if data['host'] == self.current_user().id:
                    self.messages.error('发起人就不要ROLL了吧...')
                    self.redirect(url_for('roll', index))
                    return

            for i in data['points']:
                if ip in i['ip']:
                    self.messages.error('IP重复，不可再次参与')
                    self.redirect(url_for('roll', index))
                    return

            name = self.get_argument('name', '无名氏')
            point = random.randint(1, 999)
            data['points'].append({'name': name, 'point': point, 'ip': ip})
            self.redirect(url_for('roll', index))
