from rest_framework.throttling import UserRateThrottle

class ReviewParticularThrottle(UserRateThrottle):
    scope = 'review-specific'

class ReviewListThrottle(UserRateThrottle):
    scope = 'review-detail'