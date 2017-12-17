from app import create_app
import unittest
from mongoengine import connect
import mongomock
from Models.Utils import Config

class FlaskBookshelfTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # creates a test client
        # connect(host='mongomock://localhost')
        id = mongomock.MongoClient().db.Config.insert({ "config_id" : "initials", "SECRET_KEY" : "yolo leme trele mou", "ACTIVATION_SECRET_KEY" : "oti na nai dn tn palevoume", "DEBUG" : True, "MAIL_SERVER" : "smtp.zoho.eu", "MAIL_PORT" : 465, "MAIL_USE_SSL" : True, "MAIL_USE_TLS" : False, "MAIL_USERNAME" : "info@taxicab.me", "MAIL_PASSWORD" : "21132113" })

        # print(Config.objects.get(config_id='initials'))
        print(id)
        self.app = create_app(
            # MONGODB_SETTINGS={
            #     'host': 'mongomock://localhost' #, 'db': 'testdb'
            # },

            testing=True,
            TESTING=True
        ).test_client()
        print('asdfasdfasdfas')

        # propagate the exceptions to the test client
        # self.app.testing = True

    def tearDown(self):
        pass

    def test_home_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        print('asdfasdfasdfas')
        result = self.app.get('/')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_home_data(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/')

        # assert the response data
        self.assertEqual(result.data, "Hello World!!!")

if __name__ == '__main__':
    unittest.main()
