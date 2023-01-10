from versify.paths.v2_journeys_journey_id.get import ApiForget
from versify.paths.v2_journeys_journey_id.put import ApiForput
from versify.paths.v2_journeys_journey_id.delete import ApiFordelete


class V2JourneysJourneyId(
    ApiForget,
    ApiForput,
    ApiFordelete,
):
    pass
