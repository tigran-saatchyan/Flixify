from flask_restx import Api

api = Api(
    authorizations={
        "Bearer": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization"
        }
    },
    title="Project Flixify",
    doc="/",
    description="This API provides information "
                "about movies and their details.",
    contact='Tigran O. Saatchyan @Pythonistic',
    contact_email='mr.saatchyan@yandex.com',
    contact_url='https://github.com/tigran-saatchyan'
)
