"""
Single-backend sync bundle: bootstrap + profile + district user export in one response.

Used when the API and MSSQL live in one Django deployment (no separate upstream proxy).
"""

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from operations.api.mobile_export_views import MobileUserExportView
from operations.api.permissions import IsRider
from operations.api.rider_views import RiderBootstrapView, RiderProfileView


class RiderSyncBundleView(APIView):
    """
    GET /api/rider/sync-bundle/

    Returns bootstrap, profile, and mobile-user-export payloads for the authenticated rider.
    Same permissions and district rules as GET /api/rider/mobile-user-export/.
    """

    permission_classes = [IsAuthenticated, IsRider]

    def get(self, request):
        br = RiderBootstrapView().get(request)
        if br.status_code != 200:
            return br
        pr = RiderProfileView().get(request)
        if pr.status_code != 200:
            return pr
        ur = MobileUserExportView().get(request)
        if ur.status_code != 200:
            return ur
        bootstrap = br.data
        profile = pr.data
        users = ur.data.get("users", [])
        district_id = ur.data.get("district_id") or bootstrap.get("district_id")
        return Response(
            {
                "bootstrap": bootstrap,
                "profile": profile,
                "district_id": district_id,
                "users": users,
            },
            status=status.HTTP_200_OK,
        )
