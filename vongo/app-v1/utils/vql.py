from pprint import pprint


def convert_clause(clause):
    field = clause["field"]
    operator = clause["operator"]
    value = clause["value"]
    if operator == "=":
        return field, value
    elif operator == "~":
        return field, {"$regex": value}
    elif operator == "<":
        return field, {"$lt": int(value)}
    elif operator == ">":
        return field, {"$gt": int(value)}
    return {}


def query_to_mongo(query: dict):
    result = {}
    operator = query["operator"]

    # Handle AND
    if operator == "AND":
        for clause in query.get("value", []):
            k, v = convert_clause(clause)
            result[k] = v

    # Handle OR
    if operator == "OR":
        result["$or"] = {}
        for clause in query.get("value", []):
            k, v = convert_clause(clause)
            result["$or"][k] = v

    return result


def test_1():
    q = {
        "operator": "AND",
        "value": [
            {
                "field": "custom_attributes.social_network",
                "operator": "=",
                "value": "facebook",
            },
            {
                "field": "custom_attributes.social_network",
                "operator": "=",
                "value": "twitter",
            },
            {
                "field": "custom_attributes.social_network",
                "operator": "=",
                "value": "instagram",
            },
        ],
    }
    test = query_to_mongo(q)
    truth = {
        "custom_attributes.social_network": "facebook",
        "custom_attributes.social_network": "twitter",
        "custom_attributes.social_network": "instagram",
    }
    try:
        assert test == truth
    except:
        pprint(test)
        pprint(truth)


def test_2():
    q = {
        "operator": "OR",
        "value": [
            {
                "field": "custom_attributes.social_network",
                "operator": "=",
                "value": "facebook",
            },
            {
                "field": "custom_attributes.social_network",
                "operator": "=",
                "value": "twitter",
            },
            {
                "field": "custom_attributes.social_network",
                "operator": "=",
                "value": "instagram",
            },
        ],
    }
    test = query_to_mongo(q)
    truth = {
        "$or": {
            "custom_attributes.social_network": "facebook",
            "custom_attributes.social_network": "twitter",
            "custom_attributes.social_network": "instagram",
        }
    }
    try:
        assert test == truth
    except:
        pprint(test)
        pprint(truth)


def test_3():
    q = {
        "operator": "OR",
        "value": [
            {"field": "created", "operator": ">", "value": 123},
            {"field": "email", "operator": "~", "value": "@gmail.com"},
        ],
    }
    test = query_to_mongo(q)
    truth = {
        "$or": {
            "created": {"$gt": 123},
            "email": {"$regex": "@gmail.com"},
        }
    }
    try:
        assert test == truth
    except:
        pprint(test)
        pprint(truth)


if __name__ == "__main__":
    test_1()
    test_2()
    test_3()
