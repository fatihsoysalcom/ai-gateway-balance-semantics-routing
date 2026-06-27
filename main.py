import time
import random

# --- Simulated AI Providers ---
# Each provider has different characteristics that influence routing decisions.
AI_PROVIDERS = [
    {
        "id": "provider_A",
        "name": "Reliable AI Corp",
        "cost_per_token": 0.002,  # USD
        "avg_latency_ms": 150,
        "reliability_score": 0.95, # Higher is better, represents strategic preference or quality
        "current_load": 0 # Simulated load counter for load balancing
    },
    {
        "id": "provider_B",
        "name": "Budget AI Solutions",
        "cost_per_token": 0.0015, # Cheaper option
        "avg_latency_ms": 200,
        "reliability_score": 0.80, # Lower reliability/preference
        "current_load": 0
    },
    {
        "id": "provider_C",
        "name": "Fast AI Services",
        "cost_per_token": 0.0025, # More expensive
        "avg_latency_ms": 100, # Faster option
        "reliability_score": 0.90,
        "current_load": 0
    }
]

# --- Simulated AI Call ---
def simulate_ai_call(provider_id, prompt_tokens):
    """Simulates an API call to an AI provider, including latency and cost."""
    provider = next((p for p in AI_PROVIDERS if p["id"] == provider_id), None)
    if not provider:
        raise ValueError(f"Provider {provider_id} not found.")

    # Simulate latency with some variance
    latency_ms = provider["avg_latency_ms"] + random.randint(-50, 50)
    time.sleep(latency_ms / 1000)

    # Calculate cost
    cost = prompt_tokens * provider["cost_per_token"]

    # Simulate token generation (simple output)
    response_tokens = prompt_tokens * random.uniform(0.8, 1.2)
    
    # Update simulated load for the chosen provider
    provider["current_load"] += 1

    return {
        "provider_name": provider["name"],
        "cost": cost,
        "latency_ms": latency_ms,
        "response_tokens": int(response_tokens),
        "status": "success"
    }

# --- AI Token Gateway Logic ---
def ai_token_gateway(prompt, expected_tokens):
    """
    Routes the AI request to the most suitable provider based on a balanced semantic approach.
    Considers cost, latency, reliability, and current load, not just the cheapest or fastest.
    """
    best_provider = None
    min_score = float('inf')

    print(f"\n--- Routing request for '{prompt[:30]}...' ({expected_tokens} tokens) ---")

    for provider in AI_PROVIDERS:
        # Calculate estimated cost and latency for this specific request
        estimated_cost = expected_tokens * provider["cost_per_token"]
        estimated_latency_s = provider["avg_latency_ms"] / 1000.0

        # --- Balance Semantics: Combine multiple factors into a weighted score ---
        # The goal is to minimize this score. Weights can be tuned based on strategic priorities.
        # Cost: Directly proportional (higher cost is worse)
        # Latency: Directly proportional (higher latency is worse)
        # Reliability: Inversely proportional (higher reliability_score is better, so subtract)
        # Load: Directly proportional (higher current_load is worse, encouraging load balancing)
        
        WEIGHT_COST = 1000      # Scale cost up as it's a small number
        WEIGHT_LATENCY = 1      # Latency in seconds
        WEIGHT_RELIABILITY = 50 # Reliability score (0-1), higher is better
        WEIGHT_LOAD = 0.1       # Current load (number of active requests)

        score = (estimated_cost * WEIGHT_COST) + \
                (estimated_latency_s * WEIGHT_LATENCY) - \
                (provider["reliability_score"] * WEIGHT_RELIABILITY) + \
                (provider["current_load"] * WEIGHT_LOAD) 

        print(f"  {provider['name']}: Cost=${estimated_cost:.4f}, Latency={estimated_latency_s:.2f}s, Reliability={provider['reliability_score']:.2f}, Load={provider['current_load']} -> Score={score:.2f}")

        if score < min_score:
            min_score = score
            best_provider = provider

    if best_provider:
        print(f"  Selected Provider: {best_provider['name']} (Score: {min_score:.2f})")
        result = simulate_ai_call(best_provider["id"], expected_tokens)
        print(f"  Result from {result['provider_name']}: Cost=${result['cost']:.4f}, Latency={result['latency_ms']}ms, Response Tokens={result['response_tokens']}")
        return result
    else:
        print("  No suitable provider found.")
        return {"status": "error", "message": "No providers available."}

# --- Example Usage ---
if __name__ == "__main__":
    prompts = [
        "Generate a short story about a space explorer.",
        "Explain the concept of quantum entanglement.",
        "Write a Python function for quicksort.",
        "Translate 'hello world' to French.",
        "Summarize the latest news on AI.",
        "Draft an email to a client about project status.",
        "Generate a list of 5 healthy breakfast ideas.",
        "Describe the history of the internet.",
        "Create a simple haiku about autumn.",
        "Provide a recipe for chocolate chip cookies."
    ]

    # Simulate multiple requests to demonstrate load balancing and balanced routing
    for i in range(10):
        prompt = random.choice(prompts)
        expected_tokens = random.randint(50, 200) # Simulate varying request sizes
        ai_token_gateway(prompt, expected_tokens)
        time.sleep(0.1) # Small delay between requests
    
    print("\n--- Final Provider Loads ---")
    for provider in AI_PROVIDERS:
        print(f"{provider['name']}: {provider['current_load']} requests handled.")
