from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from watchlist_app.models import StreamPlatform, WatchList, Review


# ---------------------------------------------------------------------------------------------------------------------------------
#                  StreamPlatformTestCase - TestCase - CRUD 
# ---------------------------------------------------------------------------------------------------------------------------------

# 1. Create temporary User [ This is for normal user and not admin so -> HTTP_403_FORBIDDEN]
# 2. Generate token and attach it to Header -> as users need to be autheticated to access this page
# 3. Also add single entry for StreamPlatform to perform CRUD operation on individual platform [self.stream]
# 4. Do post req.
# 5. Get the response and verify it 

# ---------------------------------------------------------------------------------------------------------------------------------  

class StreamPlatformTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="newPassword@123")
        self.token = Token.objects.get(user__username='example')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = StreamPlatform.objects.create(name="Netflix",
                                               about="#1 Platform",
                                               website="https://netflix.com")
    
    def test_streamplatform_create(self):
        data = {
            "name": "Prime",
            "about": "#1 Streaming Platform",
            "website": "https://prime.com"
        }
        
        response = self.client.post(reverse('streamplatform-list'), data)
        
        # should fail (forbidden for non-admin user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(StreamPlatform.objects.get().name, "Netflix")
        
    
    def test_streamplatform_list(self):
        response = self.client.get(reverse('streamplatform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_streamplatform_detail(self):
        response = self.client.get(reverse('streamplatform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(StreamPlatform.objects.get().name, "Netflix")
        
    def test_streamplatform_update(self):
        data = {
            "name": "Netflix Updated",
            "about": "Updated #1 Platform",
            "website": "https://netflix.com"
        }
        response = self.client.put(reverse('streamplatform-detail', args=(self.stream.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        
    def test_streamplatform_delete(self):
        response = self.client.delete(reverse('streamplatform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        


# ---------------------------------------------------------------------------------------------------------------------------------
#                  WatchListTestCase - TestCase - CRUD 
# ---------------------------------------------------------------------------------------------------------------------------------

# 1. Create temporary User [ This is for normal user and not admin so -> HTTP_403_FORBIDDEN]
# 2. Generate token and attach it to Header -> as users need to be autheticated to access this page
# 3. Also add single entry for WatchList to perform CRUD operation on individual platform [self.stream]
# 4. Do post req.
# 5. Get the response and verify it 

# ---------------------------------------------------------------------------------------------------------------------------------        



class WatchListTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="newPassword@123")
        
        self.token = Token.objects.get(user__username='example')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.stream = StreamPlatform.objects.create(
            name="Netflix",
            about="#1 Platform",
            website="https://netflix.com"
        )
        
        self.watchlist = WatchList.objects.create(
            title="Aarya",
            storyline="A woman joins a narcotics ring to protect her family after her husband is killed.",
            platform=self.stream,
            active=True
        )
        
    def test_watchlist_create(self):
        data = {
            "title": "Aarya - Part 2",
            "storyline": "A woman joins a narcotics ring to protect her family after her husband is killed.",
            "active": True,
            "platform": self.stream
        }
        response = self.client.post(reverse('movie-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_watchlist_list(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_watchlist_detail(self):
        response = self.client.get(reverse('movie-details', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Aarya')
        
    def test_watchlist_update(self):
        data = {
            "title": "Aarya Updated",
            "storyline": "Updated storyline",
            "platform": self.stream.id,
            "active": True
        }
        response = self.client.put(reverse('movie-details', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        
    def test_watchlist_delete(self):
        response = self.client.delete(reverse('movie-details', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ReviewTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="newPassword@123")
        self.token = Token.objects.get(user__username='example')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.stream = StreamPlatform.objects.create(
            name="Netflix",
            about="#1 Platform",
            website="https://netflix.com"
        )
        
        self.watchlist = WatchList.objects.create(
            title="Aarya",
            storyline="A woman joins a narcotics ring to protect her family after her husband is killed.",
            platform=self.stream,
            active=True,
            avg_rating=0,
            number_rating=0
        )
        
        self.review = Review.objects.create(
            review_user=self.user,
            rating=5,
            description="Great Movie!",
            watchlist=self.watchlist,
            active=True
        )
        
        # Update watchlist rating after review creation
        self.watchlist.number_rating = 1
        self.watchlist.avg_rating = 5.0
        self.watchlist.save()
       
        
    def test_review_create(self):
        # We're trying to create a second review for the same movie by the same user, which isn't allowed
        # First delete the review created in setUp
        self.review.delete()
        
        data = {
            "rating": 4,
            "description": "Great Movie! Must Watch!",
            "active": True
        }
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['rating'], 4)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.get().description, "Great Movie! Must Watch!")
        
        
    def test_review_create_unauth(self):
        self.client.force_authenticate(user=None)
        data = {
            "rating": 4,
            "description": "Great Movie! Must Watch!",
            "active": True
        }
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
    def test_review_update(self):
        data = {
            "rating": 4,
            "description": "Great Movie! - Updated!",
            "active": True
        }
        response = self.client.put(reverse('review-specific', args=(self.review.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], "Great Movie! - Updated!")
        
        # Verify the watchlist's average rating is updated
        self.watchlist.refresh_from_db()
        self.assertEqual(self.watchlist.avg_rating, 4.0)  # New rating should be 4
        self.assertEqual(self.watchlist.number_rating, 1)  # Should still be 1 review


    def test_review_list(self):
        response = self.client.get(reverse('review-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_review_ind(self):
        response = self.client.get(reverse('review-specific', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_review_user(self):
        response = self.client.get(reverse('user-review-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
       
        
    def test_review_delete(self):
        response = self.client.delete(reverse('review-specific', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        
    def test_review_user_limit(self):
        # Test that a user cannot review the same movie twice
        data = {
            "rating": 4,
            "description": "Great Movie! Second Review!",
            "active": True
        }
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
      
        # Verify that no new review was created
        self.assertEqual(Review.objects.count(), 1)
        # Verify the original review remains unchanged
        self.assertEqual(Review.objects.first().description, "Great Movie!")
        
        
    def test_review_invalid_rating(self):
        data = {
            "rating": 6,  # Invalid rating > 5
            "description": "Great Movie!",
            "active": True
        }
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
# ---------------------------------------------------------------------------------------------------------------------------------
#                  Review Movie Average - TestCase 
# ---------------------------------------------------------------------------------------------------------------------------------

        """
        Test that creating a second review by a different authenticated user updates
        the WatchList instance's average rating and review count correctly.
        Steps:
        1. Create a second user and obtain their authentication token.
        2. Authenticate as the second user and submit a new review (rating = 2).
        3. Assert the review creation endpoint returns HTTP 201 (Created).
        4. Refresh the WatchList instance from the database to reflect updated aggregates.
        5. Retrieve the movie detail endpoint and assert it returns HTTP 200 (OK).
        6. Verify:
            - number_rating increments to 2.
            - avg_rating is recalculated to (5 + 2) / 2 = 3.5.
        """

# ---------------------------------------------------------------------------------------------------------------------------------  
    def test_review_movie_average(self):

        # Create another user and get their token
        user2 = User.objects.create_user(username="example2", password="newPassword@123")
        token2 = Token.objects.get(user__username='example2')
        
        # Switch to user2
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token2.key)
        
        # Create second review
        data = {
            "rating": 2,
            "description": "Bad Movie!",
            "active": True
        }
        
        # Create review using the API endpoint
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Refresh watchlist from database to get updated values
        self.watchlist.refresh_from_db()
        
        # Get the movie details to check average rating
        response = self.client.get(reverse('movie-details', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify calculations
        self.assertEqual(self.watchlist.number_rating, 2)
        self.assertEqual(self.watchlist.avg_rating, 3.5)  # (5 + 2) / 2 = 3.5