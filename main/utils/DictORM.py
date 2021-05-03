from datetime import datetime

import logging

logger = logging.getLogger(__name__)

class DictORM:
    kwargs_max_size = 3
    order_max_size = 3

    def __init__(self):
        self.kwargs = {}
        self.query_dict = {}
        self.order_list = []

    def _where(self):
        for key in self.query_dict['where']:
            if not hasattr(self.kwargs, key + 'where') or len(self.kwargs[key + 'where']) < self.kwargs_max_size:
                field = self.query_dict['where'][key]
                if field:
                    self.kwargs[key + '__contains'] = field

    def _in(self):
        for key in self.query_dict['in']:
            if not hasattr(self.kwargs, key + '__in') or len(self.kwargs[key + '__in']) < self.kwargs_max_size:
                value = self.query_dict['in'][key]
                if value:
                    self.kwargs[key + '__in'] = value

    def _less_than(self):
        for key in self.query_dict['less_than']:
            if not hasattr(self.kwargs, key + '__lte') or len(self.kwargs[key + '__lte']) < self.kwargs_max_size:
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
        for key in self.query_dict['more_than']:
            if not hasattr(self.kwargs, key + '__gte') or len(self.kwargs[key + '__gte']) < self.kwargs_max_size:
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
        for key in self.query_dict['order']:
            if not self.order_list or len(self.order_list) < self.order_max_size:
                if self.query_dict['order'][key] == '-':
                    value = '-' + key
                else:
                    value = key

                if value:
                    self.order_list.append(value)

    def make(self, query_dict):
        self.query_dict = query_dict

        for key in self.query_dict:
            if hasattr(self, '_' + key):
                operation = getattr(self, '_' + key)
                if callable(operation):
                    operation()

        return self

