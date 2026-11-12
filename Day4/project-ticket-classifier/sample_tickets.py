
# We'll deliberately include different categories and urgency levels so that we can evaluate the classifier.

# Each ticket has:
# - id
# - message
# - expected_category
# - expected_priority
# These expected values are our test labels (ground truth). The LLM must not receive them as part of the classification prompt.

SAMPLE_TICKETS = [

    # ACCOUNT TICKETS

    {
        "id": 1,
        "message": "I cannot log in to my account even after entering the correct password.",
        "expected_category": "account",
        "expected_priority": "medium"
    },
    {
        "id": 2,
        "message": "I requested a password reset email but haven't received it.",
        "expected_category": "account",
        "expected_priority": "medium"
    },
    {
        "id": 3,
        "message": "Someone accessed my account without permission. I suspect my account has been compromised.",
        "expected_category": "account",
        "expected_priority": "critical"
    },
    {
        "id": 4,
        "message": "I want to update my profile picture and display name.",
        "expected_category": "account",
        "expected_priority": "low"
    },
    {
        "id": 5,
        "message": "My account has been locked after several failed login attempts.",
        "expected_category": "account",
        "expected_priority": "high"
    },

    # BILLING TICKETS

    {
        "id": 6,
        "message": "I was charged twice for my monthly subscription. Please refund the extra payment.",
        "expected_category": "billing",
        "expected_priority": "high"
    },
    {
        "id": 7,
        "message": "My refund has been pending for two weeks. I need an update.",
        "expected_category": "billing",
        "expected_priority": "high"
    },
    {
        "id": 8,
        "message": "Can you send me a copy of last month's invoice?",
        "expected_category": "billing",
        "expected_priority": "low"
    },
    {
        "id": 9,
        "message": "The payment gateway is failing for all customers and nobody can complete purchases.",
        "expected_category": "billing",
        "expected_priority": "critical"
    },
    {
        "id": 10,
        "message": "I want to change the credit card linked to my subscription.",
        "expected_category": "billing",
        "expected_priority": "low"
    },

    # TECHNICAL TICKETS

    {
        "id": 11,
        "message": "The application crashes every time I try to open it.",
        "expected_category": "technical",
        "expected_priority": "high"
    },
    {
        "id": 12,
        "message": "The dashboard takes around 20 seconds to load.",
        "expected_category": "technical",
        "expected_priority": "medium"
    },
    {
        "id": 13,
        "message": "Our production application is completely unavailable for every user.",
        "expected_category": "technical",
        "expected_priority": "critical"
    },
    {
        "id": 14,
        "message": "The alignment of the submit button looks slightly incorrect.",
        "expected_category": "technical",
        "expected_priority": "low"
    },
    {
        "id": 15,
        "message": "Data synchronization between our application and database keeps failing.",
        "expected_category": "technical",
        "expected_priority": "high"
    },

    # GENERAL TICKETS

    {
        "id": 16,
        "message": "What are your customer support working hours?",
        "expected_category": "general",
        "expected_priority": "low"
    },
    {
        "id": 17,
        "message": "I would like to suggest adding a dark mode to your application.",
        "expected_category": "general",
        "expected_priority": "low"
    },
    {
        "id": 18,
        "message": "Where can I find tutorials to learn how to use your platform?",
        "expected_category": "general",
        "expected_priority": "low"
    },
    {
        "id": 19,
        "message": "I have a question about the services offered by your company.",
        "expected_category": "general",
        "expected_priority": "low"
    },
    {
        "id": 20,
        "message": "I have been trying to contact your support team for days but haven't received any response.",
        "expected_category": "general",
        "expected_priority": "medium"
    }
]
