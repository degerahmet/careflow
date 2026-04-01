import json
import datetime

import anthropic
from django.conf import settings

from .models import BookingSession
from .prompts import EXTRACTION_SYSTEM, EXTRACTION_USER, REPLY_SYSTEM, REPLY_USER
from .tools import create_appointment, get_available_slots, search_providers


def _llm_extract(message: str, draft: dict) -> dict:
    """Call the LLM to extract structured booking fields from the user message."""
    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    # Pass providers/slots as context so the LLM can map names/descriptions to IDs
    user_content = EXTRACTION_USER.format(
        today=datetime.date.today().isoformat(),
        draft=json.dumps({k: v for k, v in draft.items() if k not in ("providers", "slots")}),
        providers=json.dumps(draft.get("providers", [])),
        slots=json.dumps(draft.get("slots", [])),
        message=message,
    )

    try:
        response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=256,
            system=EXTRACTION_SYSTEM,
            messages=[{"role": "user", "content": user_content}],
        )
        text = response.content[0].text.strip()
        # Strip markdown code fences if the model wraps the JSON
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text)
    except Exception:
        return {}


def _llm_reply(message: str, step: str, draft: dict, data: dict) -> str:
    """Call the LLM to generate a natural language reply for the current step."""
    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    user_content = REPLY_USER.format(
        step=step,
        draft=json.dumps({k: v for k, v in draft.items() if k not in ("providers", "slots")}),
        providers=json.dumps(data.get("providers", draft.get("providers", []))),
        slots=json.dumps(data.get("slots", draft.get("slots", []))),
        appointment=json.dumps(data.get("appointment")),
        message=message,
    )

    try:
        response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=256,
            system=REPLY_SYSTEM,
            messages=[{"role": "user", "content": user_content}],
        )
        print(response)
        return response.content[0].text.strip()
    except Exception:
        return "I'm sorry, something went wrong. Please try again."


def handle_message(session: BookingSession, message: str) -> dict:
    """
    Main orchestration entry point.

    1. Extract structured fields from the user message via LLM.
    2. Apply deterministic state transitions based on extracted fields.
    3. Call backend tools as needed (search_providers, get_available_slots, create_appointment).
    4. Generate a natural language reply via LLM.
    5. Persist session state.
    6. Return a structured response for the frontend.
    """
    draft = dict(session.draft)
    data = {}

    # Step 1 — extract
    extracted = _llm_extract(message, draft)
    for key, value in extracted.items():
        if value is not None:
            draft[key] = value

    # Step 2 — state machine
    if session.step == "collecting_intent":
        if draft.get("specialty"):
            providers = search_providers(draft["specialty"])
            draft["providers"] = providers
            data["providers"] = providers
            if providers:
                session.step = "provider_selection"

    elif session.step == "provider_selection":
        selected_id = draft.get("selected_provider_id")
        if selected_id is not None:
            try:
                draft["selected_provider_id"] = int(selected_id)
            except (ValueError, TypeError):
                draft["selected_provider_id"] = None

        if draft.get("selected_provider_id"):
            slots = get_available_slots(
                draft["selected_provider_id"],
                draft.get("preferred_date"),
            )
            draft["slots"] = slots
            data["slots"] = slots
            session.step = "slot_selection"

    elif session.step == "slot_selection":
        selected_slot = draft.get("selected_slot_id")
        if selected_slot is not None:
            try:
                draft["selected_slot_id"] = int(selected_slot)
            except (ValueError, TypeError):
                draft["selected_slot_id"] = None

        if draft.get("selected_slot_id"):
            session.step = "confirmation"

    elif session.step == "confirmation":
        if extracted.get("confirmed") is True:
            try:
                appt = create_appointment(
                    member=session.member,
                    provider_id=draft["selected_provider_id"],
                    slot_id=draft["selected_slot_id"],
                    reason=draft.get("reason", ""),
                )
                data["appointment"] = appt
                session.step = "completed"
            except Exception as exc:
                data["error"] = str(exc)

    # Step 3 — reply
    reply = _llm_reply(message, session.step, draft, data)

    # Step 4 — persist
    session.messages = list(session.messages) + [
        {"role": "user",      "text": message},
        {"role": "assistant", "text": reply},
    ]
    session.draft = draft
    session.save()

    return {
        "session_id": str(session.session_id),
        "reply": reply,
        "step": session.step,
        "data": {
            "providers":   data.get("providers", []),
            "slots":       data.get("slots", []),
            "appointment": data.get("appointment"),
            "draft":       {k: v for k, v in draft.items() if k not in ("providers", "slots")},
        },
    }
