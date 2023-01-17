from versify.paths.v2_events_event_id.get import ApiForget
from versify.paths.v2_events_event_id.put import ApiForput
from versify.paths.v2_events_event_id.delete import ApiFordelete


class V2EventsEventId(
    ApiForget,
    ApiForput,
    ApiFordelete,
):
    pass
