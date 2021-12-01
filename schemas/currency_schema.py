class CurrencySchema(object):

    @staticmethod
    def success_schema():
        return {
            "required": ["success", "timestamp", "base", "date", "rates"],
            "type": "object",
            "properties": {
                "success": {"type": "boolean"},
                "timestamp": {"type": "integer"},
                "base": {"type": "string"},
                "date": {"type": "string"},
                "rates": {
                    "type": "object",
                    "properties": {"": {"type": "number"}
                                   }
                }
            }
        }

    @staticmethod
    def invalid_currency_code_schema():
        return {
            "type": "object",
            "properties": {
                "error": {
                    "type": "object",
                    "properties": {"code": {"type": "string"},
                                   "message": {"type": "string"}
                                   }
                }
            }
        }
