def build_prompt(event_type, guest_count, services, budget, total_cost):
    return f"""
You are an AI assistant helping users reduce event costs.

Event Details:
- Type: {event_type}
- Guest Count: {guest_count}
- Services: {', '.join(services)}
- Budget: ₹{budget}
- Estimated Cost: ₹{total_cost}

Suggest 2–3 smart and practical ways to reduce the overall cost and bring it within budget.
Use simple, polite, and professional language.
Respond in markdown bullet points.
"""



def build_estimation_prompt(event_type, guest_count, services, total_cost):
    return f"""
You are an expert event planner.

An event has the following details:
- Type: {event_type}
- Guest Count: {guest_count}
- Services: {', '.join(services)}

The system has calculated an estimated cost of ₹{total_cost} using internal pricing logic.

Your task:
- Briefly explain this estimated cost in 2–3 lines
- Mention where the cost is likely being spent
- Respond professionally and clearly
"""
