from rest_framework.permissions import IsAuthenticated


class IsGroupSupportAndAuthenticated(IsAuthenticated):
    """
    Allows access only to support team users.
    """
    def has_permission(self, request, view):
        user_groups = request.user.groups.values_list('name', flat=True)
        return 'team_support' in list(user_groups)


class IsGroupSalesAndAuthenticated(IsAuthenticated):
    """
    Allows access only to sales team users.
    """
    def has_permission(self, request, view):
        user_groups = request.user.groups.values_list('name', flat=True)
        return 'team_sales' in list(user_groups)
