import re

CUSTOMER_PATTERN = '(?P<field>tags|email)(?P<operator>:|<|>|~)(?P<value>\".*?\")'


class Pipeline:

    @staticmethod
    def count_stage():
        stage = {
            '$count': "count"
        }
        return stage

    @staticmethod
    def vql_stage(vql='', org=None):
        q = {}

        # Limit the results for the organization
        if org:
            q['organization'] = org

        # Convert VQL to match conditions
        clauses = vql.split(' ')
        for clause in clauses:
            print(clause)

            if not clause or clause == '':
                continue

            # Find the field, operator, and value
            print(CUSTOMER_PATTERN)
            matches = re.match(CUSTOMER_PATTERN, clause)
            print(matches)

            field = matches.group('field')
            operator = matches.group('operator')
            value = matches.group('value')[1:-1]
            print('Field: ' + field)
            print('Operator: ' + operator)
            print('Value: ' + value)

            if operator == ':':
                q[field] = value

            elif operator == '~' and field == 'tags':
                q[field] = {'$in': [value]}

            elif operator == '~':
                q[field] = {'$regex': value}

            elif operator == '<':
                q[field] = {'$lt': int(value)}

            elif operator == '>':
                q[field] = {'$gt': int(value)}

        print(q)
        return {"$match": q}

    @staticmethod
    def match_stage(conditions='', match='all', org=None):
        q = {}

        # Inject $or if match is any
        # if match == 'any':

        # Limit the results for the organization
        if org:
            q['organization'] = org

        # Gather the filter conditions
        condition_map = {}
        conditions = conditions.split(',')
        for condition in conditions:
            if condition == '' or condition.count('-') != 2:
                continue
            field, op, val = condition.split('-')
            if op == '$in':
                vals = [v for v in val[1:-1].split('|')]
                condition_map[field] = {op: vals}

        if match == 'any':
            q['$or'] = []
            for k, v in condition_map.items():
                q['$or'].append({k: v})

        if match == 'all':
            for k, v in condition_map.items():
                q[k] = v

        return {"$match": q}

    @staticmethod
    def search_stage(index, query):
        stage = {
            '$search': {
                'index': index,
                'text': {
                    'query': query,
                    'path': {
                        'wildcard': '*'
                    }
                }
            }
        }
        return stage

    @staticmethod
    def unwind_stage(path):
        stage = {
            '$unwind': {
                'path': path,
                'preserveNullAndEmptyArrays': False
            }
        }
        return stage


if __name__ == '__main__':
    v = 'tag:"Customer"'
    Pipeline.vql_stage(v)
