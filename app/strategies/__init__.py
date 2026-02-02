from typing import Dict
from app.strategies.base import InputSourceStrategy
from app.strategies.whatsapp_strategy import WhatsAppStrategy


AVAILABLE_INPUT_TYPES = ("whatsapp",)


def get_strategy(input_type: str) -> InputSourceStrategy:
    """
    Return an instance of a strategy for the given input_type.
    Currently supported: 'whatsapp'
    """
    strategies: Dict[str, InputSourceStrategy] = {
        "whatsapp": WhatsAppStrategy(),
    }
    try:
        return strategies[input_type.lower()]
    except KeyError:
        raise ValueError(f"Unsupported input_type '{input_type}'. Supported types: {', '.join(AVAILABLE_INPUT_TYPES)}")