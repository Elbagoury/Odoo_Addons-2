from odoo import http

import hashlib
import hmac
import json


class SlackController(http.Controller):
    @staticmethod
    def verify_signature(timestamp, body_text, signature):
        secret = http.request.env['mail.slack.message'].get_slack_signing_secret()

        req = str.encode('v0:' + str(timestamp) + ':' + body_text)
        request_hash = 'v0=' + hmac.new(
            str.encode(secret),
            req, hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(request_hash, signature)

    @http.route('/slack/connect', type='json', auth="none", methods=['POST'], csrf=False)
    def slack_connect(self, **kwargs):
        # Gather request information
        headers = http.request.httprequest.headers
        timestamp = headers.get('X-Slack-Request-Timestamp', '')
        signature = headers.get('X-Slack-Signature', '')
        body = http.request.jsonrequest
        body_text = json.dumps(body)

        # Verify the signature matches
        # if not self.verify_signature(timestamp, body_text, signature):
        #     return {'error': 'Could not verify signature'}

        connect_type = body.get('type')
        if not connect_type:
            return {}

        if 'challenge' in body:
            return {'challenge': body['challenge']}

        # elif type == 'event_callback':
