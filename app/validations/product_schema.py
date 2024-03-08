# Mendefinisikan validasi mengunakan ciberus schema
product_schema = {
    'name': {
        'type': 'string',
        'required': True
    },
    'price': {
        'type': 'integer',
        'min': 1,
        'required': True
    },
    'description': {
        'type': 'string',
        'minlength': 5,
        'required': True
    }
}