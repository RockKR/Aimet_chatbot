# schemas.py

# JSON Schema for Start_State_Agent
start_state_schema = {
    "type": "object",
    "properties": {
        "Identified Topic": {"type": "string", "enum": ["counseling", "medical"]}
    },
    "required": ["Identified Topic"]
}

# JSON Schema for Counseling_Exploration_Agent
counseling_exploration_schema = {
    "type": "object",
    "properties": {
        "Counseling Responses": {
            "type": "object",
            "properties": {
                "problems": {"type": "string"},
                "duration": {"type": "string"},
                "perception": {"type": "string"},
                "feeling": {"type": "string"},
                "behavior": {"type": "string"}
            },
            "required": ["problems", "duration", "perception", "feeling", "behavior"]
        },
        "Session Status": {"type": "string", "enum": ["Not started yet", "In progress", "Completed"]}
    },
    "required": ["Counseling Responses", "Session Status"]
}

# JSON Schema for Medical_Exploration_Agent
medical_exploration_schema = {
    "type": "object",
    "properties": {
        "Medical Responses": {
            "type": "object",
            "properties": {
                "symptom": {"type": "string"},
                "duration": {"type": "string"}
            },
            "required": ["symptom", "duration"]
        },
        "Session Status": {"type": "string", "enum": ["Not started yet", "In progress", "Completed"]}
    },
    "required": ["Medical Responses", "Session Status"]
}

# JSON Schema for Medical_Medium_Exploration_Agent
medical_medium_exploration_schema = {
    "type": "object",
    "properties": {
        "Medical Medium Responses": {
            "type": "object",
            "properties": {
                "psychiatric_history": {"type": "string"}
            },
            "required": ["psychiatric_history"]
        },
        "Session Status": {"type": "string", "enum": ["Not started yet", "In progress", "Completed"]}
    },
    "required": ["Medical Medium Responses", "Session Status"]
}

# JSON Schema for Counseling_Medium_Exploration_Agent
counseling_medium_exploration_schema = {
    "type": "object",
    "properties": {
        "Counseling Medium Responses": {
            "type": "object",
            "properties": {
                "sensation": {"type": "string"}
            },
            "required": ["sensation"]
        },
        "Session Status": {"type": "string", "enum": ["Not started yet", "In progress", "Completed"]}
    },
    "required": ["Counseling Medium Responses", "Session Status"]
}

# JSON Schema for Question_Selector_Agent
question_selector_schema = {
    "type": "object",
    "properties": {
        "Next Question": {"type": "string"}
    },
    "required": ["Next Question"]
}

# Add more schemas as needed for other agents...
