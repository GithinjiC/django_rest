from django.test import TestCase
from django.utils.http import urlencode
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from drones.models import DroneCategory
from drones import views


class DroneCategoryTests(APITestCase):
    def post_drone_category(self, name):
        url = reverse(views.DroneCategoryList.name)
        data = {'name': name}
        response = self.client.post(url, data, format='json')
        return response

    def test_post_and_get_drone_category(self):
        new_drone_category_name = 'Hexacopter'
        response = self.post_drone_category(new_drone_category_name)
        print("nPK {0}n".format(DroneCategory.objects.get().pk))
        assert response.status_code == status.HTTP_201_CREATED
        assert DroneCategory.objects.count() == 1
        assert DroneCategory.objects.get().name == new_drone_category_name

    def test_post_existing_drone_category_name(self):
        url = reverse(views.DroneCategoryList.name)
        new_drone_category_name = 'Duplicated Copter'
        data = {'name': new_drone_category_name}
        response1 = self.post_drone_category(new_drone_category_name)
        assert response1.status_code == status.HTTP_201_CREATED
        response2 = self.post_drone_category(new_drone_category_name)
        print(response2)
        assert response2.status_code == status.HTTP_400_BAD_REQUEST

    def test_filter_drone_category_by_name(self):
        drone_category_name1 = 'Hexacopter'
        self.post_drone_category(drone_category_name1)
        drone_category_name2 = 'Octocopter'
        self.post_drone_category(drone_category_name2)
        filter_by_name = {'name': drone_category_name1}
        url = '{0}?{1}'.format(
            reverse(views.DroneCategoryList.name),
            urlencode(filter_by_name))
        print(url)
        response = self.client.get(url, format='json')
        print(response)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['name'] == drone_category_name1

    def test_get_drone_categories_collection(self):
        new_drone_category_name = 'Super Copter'
        self.post_drone_category(new_drone_category_name)
        url = reverse(views.DroneCategoryList.name)
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['name'] == new_drone_category_name

    def test_update_drone_category(self):
        drone_category_name = 'Initial Name'
        response = self.post_drone_category(drone_category_name)
        url = reverse(views.DroneCategoryDetail.name, None, {response.data['pk']})
        updated_drone_category_name = 'Update Name'
        data = {'name': updated_drone_category_name}
        patch_response = self.client.patch(url, data, format='json')
        assert patch_response.status_code == status.HTTP_200_OK
        assert patch_response.data['name'] == updated_drone_category_name

    def test_get_drone_category(self):
        drone_category_name = 'Easy to retrieve'
        response = self.post_drone_category(drone_category_name)
        url = reverse(views.DroneCategoryDetail.name, None, {response.data['pk']})
        get_response = self.client.get(url, format='json')
        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.data['name'] == drone_category_name
