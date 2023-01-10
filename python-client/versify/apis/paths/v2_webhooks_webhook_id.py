from versify.paths.v2_webhooks_webhook_id.get import ApiForget
from versify.paths.v2_webhooks_webhook_id.put import ApiForput
from versify.paths.v2_webhooks_webhook_id.delete import ApiFordelete


class V2WebhooksWebhookId(
    ApiForget,
    ApiForput,
    ApiFordelete,
):
    pass
