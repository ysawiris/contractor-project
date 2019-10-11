from unittest import TestCase, main as unittest_main, mock
from bson.objectid import ObjectId
from app import app

sample_inventory_id = ObjectId('5d55cffc4a3d4031f42827a2')
sample_inventory = {
    'product_team_brand': 'Golden State Warriors',
    'product_name' : 'Official NBA Jersey',
    'pic_path' : '/static/warriors_jersey.jpeg',
    'product_price' : 60
}
sample_inventory_form_data = {
    'product_team_brand': sample_inventory['product_team_brand'],
    'product_name' : sample_inventory['product_name'],
    'pic_path' : sample_inventory['pic_path'],
    'product_price' : sample_inventory['product_price']
}

sample_comment_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_comment = {
    'title': 'Test Title',
    'name': 'Test Name',
    'content': 'Test Content',
    'inventory_id' : ObjectId('5d55cffc4a3d4031f42827a2')
}
sample_form_data = {
    'title': sample_comment['title'],
    'name': sample_comment['name'],
    'content': sample_comment['content'],
    'inventory_id': sample_comment['inventory_id']
}

class ContractorTests(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
    
    def test_index(self):
        """Test the FanGear homepage."""
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Jersey', result.data)
    
    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_inventory(self, mock_find):
        mock_find.return_value = sample_inventory

        result = self.client.get(f'/inventory/{sample_inventory_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Warriors', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_edit_comment(self, mock_find):
        mock_find.return_value = sample_comment

        result = self.client.get(f'/inventory/{sample_inventory_id}/comments/{sample_comment_id}/edit')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Title', result.data)

    @mock.patch('pymongo.collection.Collection.update_one')
    def test_update_comment(self, mock_update):
        result = self.client.post(f'/inventory/{sample_inventory_id}/comments/{sample_comment_id}', data=sample_form_data)

        self.assertEqual(result.status, '302 FOUND')
        mock_update.assert_called_with({'_id': sample_comment_id}, {'$set': sample_comment})
    
if __name__ == '__main__':
    unittest_main()