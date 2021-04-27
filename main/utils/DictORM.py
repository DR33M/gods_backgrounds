from datetime import datetime


class DictORM:
    def __init__(self):
        self.kwargs = {}
        self.query_dict = {}
        self.order_list = []

    def validate(self):
        return True

    def _in(self):
        if 'in' in self.query_dict:
            for key in self.query_dict['in']:
                value = self.query_dict['in'][key]
                if value:
                    self.kwargs[key + '__in'] = value

    def _less_than(self):
        if 'less_than' in self.query_dict:
            for key in self.query_dict['less_than']:
                value = self.query_dict['less_than'][key]
                if value:
                    try:
                        start_date = datetime.fromisoformat(value)

                        if start_date:
                            value = start_date
                    except ValueError:
                        pass

                    self.kwargs[key + '__lte'] = value

    def _more_than(self):
        if 'more_than' in self.query_dict:
            for key in self.query_dict['more_than']:
                value = self.query_dict['more_than'][key]
                if value:
                    try:
                        end_date = datetime.fromisoformat(value)

                        if end_date:
                            value = end_date
                    except ValueError:
                        pass

                    self.kwargs[key + '__gte'] = value

    def _order(self):
        if 'order' in self.query_dict:
            for key in self.query_dict['order']:
                value = self.query_dict['order'][key] + key
                if value:
                    self.order_list.append(value)

    def make(self, query_dict):
        self.query_dict = query_dict

        if self.validate():
            for key in self.query_dict:
                operation = getattr(self, '_' + key)
                if callable(operation):
                    operation()

            return self
        return False

