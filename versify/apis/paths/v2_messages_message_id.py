from versify.paths.v2_messages_message_id.get import ApiForget
from versify.paths.v2_messages_message_id.put import ApiForput
from versify.paths.v2_messages_message_id.delete import ApiFordelete


class V2MessagesMessageId(
    ApiForget,
    ApiForput,
    ApiFordelete,
):
    pass
