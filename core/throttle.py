from rest_framework.throttling import UserRateThrottle

class SensitiveActionThrottle(UserRateThrottle):
  rate = '5/min'