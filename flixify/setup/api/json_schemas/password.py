change_password = {
    "type": "object",
    "properties": {
        "current_password": {"type": "string"},
        "new_password": {"type": "string"},
        "confirm_password": {"type": "string"}
    },
    "required": ["current_password", "new_password", "confirm_password"]
}
