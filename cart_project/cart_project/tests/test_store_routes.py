class TestAddStore:

    def test_success(self, client):
        resp = client.post('/add_store', json={
            'name': 'Water',
            'price': 1.00,
            'quantity': 50,
        })
        assert resp.status_code == 201
        assert 'Water' in resp.get_json()['message']

    def test_no_body_returns_400(self, client):
        resp = client.post('/add_store')
        assert resp.status_code == 400

    def test_invalid_price_type_returns_400(self, client):
        resp = client.post('/add_store', json={
            'name': 'Water',
            'price': 'not_a_number',
            'quantity': 10,
        })
        assert resp.status_code == 400

    def test_zero_quantity_returns_400(self, client):
        resp = client.post('/add_store', json={
            'name': 'Water',
            'price': 1.00,
            'quantity': 0,
        })
        assert resp.status_code == 400

    def test_negative_price_returns_400(self, client):
        resp = client.post('/add_store', json={
            'name': 'Water',
            'price': -1.00,
            'quantity': 10,
        })
        assert resp.status_code == 400


class TestGetCatalog:

    def test_returns_all_products(self, client, seed_data):
        resp = client.get('/catalog')
        assert resp.status_code == 200
        catalog = resp.get_json()['catalog']
        assert isinstance(catalog, list)
        assert len(catalog) == 1
        assert catalog[0]['name'] == 'Cola'
