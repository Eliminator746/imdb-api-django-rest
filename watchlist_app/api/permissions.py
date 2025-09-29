from rest_framework import permissions

# ---------------------------------------------------------------------------------------------------------------------------------
"""
                                            Allows access only to admin users.
                                            Check if user is Admin or not
                                            if not: readonly else: allow 
"""
# ---------------------------------------------------------------------------------------------------------------------------------
class AdminOrReadOnly(permissions.IsAdminUser):
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user and request.user.is_staff

# ---------------------------------------------------------------------------------------------------------------------------------
"""
                                            Allows write access only to ReviewUser i.e the user who has written this review.
                                            Check if logged in user is same as review_user 
                                            if not: readonly else: allow 
"""
# ---------------------------------------------------------------------------------------------------------------------------------
class ReviewUserOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.review_user == request.user
# ---------------------------------------------------------------------------------------------------------------------------------
          
        