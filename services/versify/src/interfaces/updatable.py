class UpdateableResource:

    def __init__(self) -> None:
        pass

    def update(
        self,
        body: dict,
        filter: dict,
        expand_list=[]
    ) -> dict:

        # Get document matching filter
        data = self.get(filter)

        # Update data with payload
        body['updated'] = int(time.time())
        data.update(body)

        # Update document in DB
        data = self.collection.find_one_and_update(
            filter,
            {'$set': self.Model(**data).to_bson()},
            return_document=ReturnDocument.AFTER,
        )

        # Convert to JSON and expand fields
        data = self.Model(**data).to_json()
        return self.expand(data, expand_list)  # type: ignore
