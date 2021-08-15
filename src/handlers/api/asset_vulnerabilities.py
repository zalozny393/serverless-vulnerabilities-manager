from src.models.user_model import UserModel
from src.services.asset_vulnerability_service import AssetVulnerabilityService
from src.utils.debugger import init_debug_mode
from src.utils.http import response
from src.utils.request import request

init_debug_mode()


@request
def get_asset_vulnerabilities(user: UserModel, event):
    try:
        status = int(event['pathParameters'].get('status'))
        group_name = event['queryStringParameters'].get('group')
        asset = event['queryStringParameters'].get('asset')
    except AttributeError:
        return response('group name or status is missing', status=400)

    asset_vulnerability_service = AssetVulnerabilityService()
    asset_vulnerabilities = asset_vulnerability_service.get_asset_vulnerabilities(group_name, status, asset)

    converted_av = list(map(lambda av: {
            'name': av.name,
            'description': av.description,
            'asset_ip': av.ip,
            'severity': av.severity,
            'status': av.status,
            'vulnerability_id': av.vulnerability_id
        }, asset_vulnerabilities))

    return response({'count': len(converted_av), 'records': converted_av})
