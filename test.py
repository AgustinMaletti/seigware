from app import create_app, db
import unittest
from time import sleep
from bot import Selenium_bot
# import HtmlTestRunner
# import threading
from flask import url_for
import requests
# from app import create_app
from bot import Selenium_bot
from flask_testing import LiveServerTestCase
import pathlib
from flask import Flask
import io
from models import Post
import sys
import json
from flask import jsonify


authors = ['Roberto', 'Mike', 'Chevy', 'Ivan', 'Cristian', 'Flavia', 'Soraia']
title = ['Life is good', 'Play with the cats', 'Jump the wall', 'Claim the reward', 'Own your destiny', 'Make good friends', 'Eat icecream']
text = ['Never give up in the life, learn to smile to difficult situations and enjoy your food',
        'Play with the cats like a cats,jump with the cats like a cats',
        'Jump the defense wall when you play basketball!',
        'The end is always the most difficult part, be patient and claim the reward.',
        'Fight for what you wont and always learn from mistakes.',
        'Make some time for rest and have fun with friends at the ends only we have our memories',
        'Experiment with different ice creams until you found one that you like']

PATH = pathlib.Path(__file__).parent
DB_PATH = PATH.joinpath('static/fake_db.db').resolve().__str__()
db_uri =  'sqlite:////' + DB_PATH

def print_in_test(hello):
    ''' Capture print statement in test
    '''
    captured_output = io.StringIO()          # Create StringIO object
    sys.stdout = captured_output                   #  and redirect stdout.
    print(hello)                                   # Call unchanged function.
    sys.stdout = sys.__stdout__                   # Reset redirect.
    print('Captured', captured_output.getvalue())


class BaseTest(LiveServerTestCase):

    def create_app(self):
        # PATH = pathlib.Path(__file__).parent
         # fake_db_path = PATH.joinpath('/static/fake_db.db').resolve()
        fake_db_path = db_uri
        app = create_app()
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        # SERVER_NAME="0.0.0.0"
        app.config.update(
                          LIVESERVER_PORT = 5000,
                          LIVESERVER_TIMEOUT = 10,
                          SQLALCHEMY_DATABASE_URI = fake_db_path
                          )
        self.app_context = app.app_context()
        self.app_context.push()
        return app  
    
    def populate_db(self):
        for a, t, tx in zip(authors, title, text):
            new_post = Post(author=a, title=t, text=tx)
            db.session.add(new_post)
            db.session.commit()


class Test_with_Selenium(BaseTest):
   
    def setUp(self):
        self.app = self.create_app()
        db.create_all()
        self.populate_db()
        self.bot = Selenium_bot()
        sleep(4)
        self.bot.driver.implicitly_wait(5)  
        self.server = self.get_server_url() 
        # self.server='http://0.0.0.0:5000'
        self.bot.driver.get(self.server)
        
        
    def tearDown(self):
        self.bot.driver.quit()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

  
    def test_like_button_0(self):
        # check how much elements of the type are    
        Q = self.bot.how_much_elements('//div[contains(@id,"post-slot")]')
        print_in_test(Q)
        check, check2, button_display = self.bot.check_click_check('//label[contains(@for, "like")]',
                                                                  '//button[contains(@class, "like")]', 0)
        self.assertEqual(int(check2), int(check) + 1)
           
    def test_like_button_6(self):
        # check how much elements of the type are    
        Q = self.bot.how_much_elements('//div[contains(@id,"post-slot")]')
        check, check2, button_display = self.bot.check_click_check('//label[contains(@for, "like")]',
                                                                  '//button[contains(@class, "like")]', 6)
        self.assertEqual(int(check2), int(check) + 1)

    def test_write_on_textarea(self):
        # check if the textarea receive the keysending
        text_test = 'Automatic text'
        text_is_there = self.bot.write_check( '//textarea[contains(@id,"text-post")]', text_test)
        self.assertEqual(text_test, text_is_there)
    

    def test_write_on_author(self):
         # check if the author input receive the keysending
        text_test = 'author text'
        text_is_there = self.bot.write_check( '//input[contains(@id,"author-post")]', text_test)
        self.assertEqual(text_test, text_is_there)
    
    def test_write_on_title(self):
        # check if the title input receive the keysending
        text_test = 'title text'
        text_is_there = self.bot.write_check( '//input[contains(@id,"title-post")]', text_test)
        self.assertEqual(text_test, text_is_there)

    def test_send_post_check_in_db(self):
        # find elementes and send a new post
        author = 'Edilverto rammirez'
        title= 'um simple titulo de teste'
        content = 'Ola sendo este outro post queri dizer algo sem importancia'
        # fill the fields
        self.bot.write( '//input[contains(@id,"author-post")]', author)
        self.bot.write( '//input[contains(@id,"title-post")]', title)
        self.bot.write( '//textarea[contains(@id,"text-post")]', content)
        self.bot.action.perform()
        self.bot.driver.find_element_by_xpath('//button[contains(@id, "button-send")]').click()
        # # query the database
        sleep(1)
        recent_post = Post.query.filter_by(author=author).first()
        # compare the records to the values
        self.assertEqual(recent_post.author , author)
        self.assertEqual(recent_post.title , title)
        self.assertEqual(recent_post.text , content)
        self.assertEqual(recent_post.likes , 0)

    def test_send_post_check_in_page(self):
        # find elementes and send a new post
        author = 'Edilverto rammirez'
        title = 'um simple titulo de teste'
        content = 'Ola sendo este outro post queri dizer algo sem importancia'
        # fill the fields
        self.bot.write( '//input[contains(@id,"author-post")]', author)
        self.bot.write( '//input[contains(@id,"title-post")]', title)
        self.bot.write( '//textarea[contains(@id,"text-post")]', content)
        self.bot.action.perform()
        self.bot.driver.find_element_by_xpath('//button[contains(@id, "button-send")]').click()
        # # query the database
        sleep(2)
        slot_post = "//div[contains(@id, 'post-slot') and position() =1]"
        # compare the records to the values
        recent_post_author = self.bot.driver.find_element_by_xpath(slot_post+"//h3").text
        recent_post_title = self.bot.driver.find_element_by_xpath(slot_post+"//h4").text
        recent_post_text = self.bot.driver.find_element_by_xpath(slot_post+"//p").text
        recent_post_label = self.bot.driver.find_element_by_xpath(slot_post+"//label").text
        self.assertEqual(recent_post_author , author)
        self.assertEqual(recent_post_title , title)
        self.assertEqual(recent_post_text , content)
        self.assertEqual(recent_post_label , '0')
    
    def test_send_empty_post_missing_data_appear(self):
        self.bot.write( '//input[contains(@id,"author-post")]', '')
        self.bot.write( '//input[contains(@id,"title-post")]', '')
        self.bot.write( '//textarea[contains(@id,"text-post")]', '')
        self.bot.action.perform()
        self.bot.driver.find_element_by_xpath('//button[contains(@id, "button-send")]').click()
        sleep(1)
        alert_message = self.bot.driver.find_element_by_xpath("//div[@id='error-alert']").text
        self.assertEqual(alert_message, 'Missing data')

class Test_FakeClient(BaseTest):
    
    def setUp(self):
        self.app = self.create_app()
        db.create_all()
        self.populate_db()
        self.client = self.app.test_client()
        self.server = self.get_server_url() 
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_server_permanentRedirect(self):
         response = self.client.get(self.server)
         print_in_test(self.server)
         self.assertEqual(response.status_code, 308)

    def test_server_indexAlive(self):
         response = self.client.get(self.server+'/')
         print_in_test(self.server)
         self.assertEqual(response.status_code, 200)

    def test__getPostRest(self):
        response = self.client.get('/get_posts')
        posts = []
        for i, (a, t, tx) in enumerate(zip(authors, title, text)):
            post = {'author':a, 'likes':'0', 'post_id': str(i +1),'text':tx, 'title':t}
            posts.append(post)
        self.assertEqual(response.json, posts)

    def test_likePost_responseOk(self):
        # fake data sending
        data = {'post_id': 2, 'total_likes': 3}
        response = self.client.post(self.server + '/like_post',
                                    content_type='application/json;charset=UTF-8',
                                    data=json.dumps(data)) 
        self.assertIn( b'Ok', response.data)
        self.assertEqual(200, response.status_code)

    def test_likePost_responseMissingData(self):
        # fake data sending
        data = {'post_id': None,'total_likes': None}
        response = self.client.post(self.server + '/like_post',
                                    content_type='application/json;charset=UTF-8',
                                    data=json.dumps(data)) 
        self.assertIn( b'Missing data', response.data)

    def test_likePost_inDb(self):
        # fake data sending
        data = {'post_id': 2, 'total_likes': 3}
        response = self.client.post(self.server + '/like_post',
                                    content_type='application/json;charset=UTF-8',
                                    data=json.dumps(data)) 
        post_with_updated_like = Post.query.filter_by(id=data['post_id']).first()
        current_likes = post_with_updated_like.likes
        self.assertEqual( data['total_likes'], current_likes)
     
    def test_PostPost_inDb(self):
            # fake data sending
        data = {'author': 'human being', 'title': 'great test', 'text':'Hello world'}
        response = self.client.post(self.server + '/new_post',
                                    content_type='application/json;charset=UTF-8',
                                    data=json.dumps(data)) 
        sleep(1)
        recent_post = Post.query.filter_by(author=data['author']).first()
        author = recent_post.author
        title = recent_post.title
        text = recent_post.text
        self.assertEqual(data['author'], author)
        self.assertEqual(data['title'], title)
        self.assertEqual(data['text'], text)
    
    def test_PostPost_withoutData(self):
            # fake data sending
        data = {'author': None, 'title': None, 'text': None}
        response = self.client.post(self.server + '/new_post',
                                    content_type='application/json;charset=UTF-8',
                                    data=json.dumps(data)) 
        sleep(1)
        self.assertIn( b'Missing data', response.data)
    
    def test_PostPost_authorTooLong(self):
            # fake data sending
        data = {'author': 'maisdevintecaracteres', 'title': 'title', 'text': 'simpletext'}
        response = self.client.post(self.server + '/new_post',
                                    content_type='application/json;charset=UTF-8',
                                    data=json.dumps(data)) 
        sleep(1)
        self.assertIn( b'Missing data', response.data)

    def test_PostPost_titleTooLong(self):
            # fake data sending
        data = {'author': 'vinti', 'title': 'titlewithmorethan50caracteres_addingmorecaractereshere', 'text': 'simpletext'}
        response = self.client.post(self.server + '/new_post',
                                    content_type='application/json;charset=UTF-8',
                                    data=json.dumps(data)) 
        sleep(1)
        self.assertIn( b'Missing data', response.data)

    def test_PostPost_textTooLong(self):
            # fake data sending
        data = {'author': 'vinte', 'title': 'title', 'text': ''.join(str(i) for i in range(140))}
        response = self.client.post(self.server + '/new_post',
                                    content_type='application/json;charset=UTF-8',
                                    data=json.dumps(data)) 
        sleep(1)
        self.assertIn( b'Missing data', response.data)

          

if __name__== '__main__':
#    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='testes'))
    unittest.main()

