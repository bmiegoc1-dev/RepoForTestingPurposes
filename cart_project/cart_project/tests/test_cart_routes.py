import pytest


class TestAddToCart:

    def test_success(self, client, seed_data):
        resp = client.post('/add', json={
            'user_id': seed_data['user_id'],
            'product_id': seed_data['product_id'],
            'quantity': 2,
        })
        assert resp.status_code == 201
        assert 'Cola' in resp.get_json()['message']

    def test_product_not_found(self, client, seed_data):
        resp = client.post('/add', json={
            'user_id': seed_data['user_id'],
            'product_id': 9999,
            'quantity': 1,
        })
        assert resp.status_code == 404

    def test_no_body_returns_400(self, client):
        resp = client.post('/add')
        assert resp.status_code == 400

    def test_missing_fields_returns_400(self, client):
        resp = client.post('/add', json={'user_id': 1})
        assert resp.status_code == 400

    def test_invalid_types_returns_400(self, client):
        resp = client.post('/add', json={
            'user_id': 'not_a_number',
            'product_id': 1,
            'quantity': 1,
        })
        assert resp.status_code == 400

    def test_zero_quantity_returns_400(self, client, seed_data):
        resp = client.post('/add', json={
            'user_id': seed_data['user_id'],
            'product_id': seed_data['product_id'],
            'quantity': 0,
        })
        assert resp.status_code == 400

    def test_negative_quantity_returns_400(self, client, seed_data):
        resp = client.post('/add', json={
            'user_id': seed_data['user_id'],
            'product_id': seed_data['product_id'],
            'quantity': -3,
        })
        assert resp.status_code == 400


class TestRemoveFromCart:

    def test_success(self, client, seed_data):
        client.post('/add', json={
            'user_id': seed_data['user_id'],
            'product_id': seed_data['product_id'],
            'quantity': 3,
        })
        resp = client.delete('/remove', json={
            'user_id': seed_data['user_id'],
            'product_id': seed_data['product_id'],
            'quantity': 1,
        })
        assert resp.status_code == 200
        assert 'Cola' in resp.get_json()['message']

    def test_product_not_in_cart_returns_404(self, client, seed_data):
        resp = client.delete('/remove', json={
            'user_id': seed_data['user_id'],
            'product_id': seed_data['product_id'],
            'quantity': 1,
        })
        assert resp.status_code == 404

    def test_no_body_returns_400(self, client):
        resp = client.delete('/remove')
        assert resp.status_code == 400


class TestGetTotal:

    def test_success(self, client, seed_data):
        client.post('/add', json={
            'user_id': seed_data['user_id'],
            'product_id': seed_data['product_id'],
            'quantity': 2,
        })
        resp = client.get(f'/total/{seed_data["user_id"]}')
        assert resp.status_code == 200
        assert resp.get_json()['current_cart_value'] == pytest.approx(5.00)

    def test_user_not_found_returns_404(self, client):
        resp = client.get('/total/9999')
        assert resp.status_code == 404


class TestGetCart:

    def test_success(self, client, seed_data):
        client.post('/add', json={
            'user_id': seed_data['user_id'],
            'product_id': seed_data['product_id'],
            'quantity': 2,
        })
        resp = client.get(f'/get_cart/{seed_data["user_id"]}')
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['cart_owner'] == 'alice'
        assert len(data['items']) == 1
        assert data['total_value'] == pytest.approx(5.00)

    def test_empty_cart_returns_200(self, client, seed_data):
        resp = client.get(f'/get_cart/{seed_data["user_id"]}')
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['items'] == []
        assert data['total_value'] == 0

    def test_user_not_found_returns_404(self, client):
        resp = client.get('/get_cart/9999')
        assert resp.status_code == 404
