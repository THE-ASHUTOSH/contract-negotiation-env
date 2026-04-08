import json
import difflib
from typing import List, Optional


def grade_conflict_identification(predicted_ids: List[str], ground_truth_ids: List[str]) -> float:
    """Grade conflict identification using F1 score."""
    if not predicted_ids and not ground_truth_ids:
        return 1.0
    if not predicted_ids:
        return 0.0
    if not ground_truth_ids:
        return 0.0

    predicted_set = set(predicted_ids)
    truth_set = set(ground_truth_ids)
    overlap = predicted_set & truth_set

    precision = len(overlap) / len(predicted_set)
    recall = len(overlap) / len(truth_set)

    if precision + recall == 0:
        return 0.0

    f1 = 2 * precision * recall / (precision + recall)
    return max(0.0, min(1.0, f1))


def grade_compromise(
    clause_id: str,
    proposed_text: str,
    vendor_text: str,
    client_text: str,
    llm_client,
    model: str,
) -> float:
    """Grade a proposed compromise clause using LLM-as-judge."""
    prompt = f"""You are a contract law expert. Score this proposed compromise clause from 0.0 to 1.0.

Vendor clause: {vendor_text}
Client clause: {client_text}
Proposed compromise: {proposed_text}

Score based on:
1. Addresses both parties' core interests (0.4 weight)
2. Legally clear and unambiguous language (0.3 weight)
3. Is a genuine compromise, not a verbatim copy of either side (0.3 weight)

Respond with ONLY valid JSON: {{"score": <float 0.0-1.0>, "reason": "<one sentence>"}}"""

    try:
        response = llm_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.1,
        )
        text = response.choices[0].message.content.strip()
        # Try to extract JSON from the response
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()
        result = json.loads(text)
        score = float(result.get("score", 0.5))
        return max(0.0, min(1.0, score))
    except Exception:
        return 0.5


def grade_final_contract(
    final_text: str,
    fixture: dict,
    llm_client,
    model: str,
) -> float:
    """Grade the final merged contract with composite scoring."""
    ground_truth = fixture["ground_truth_conflicts"]
    non_negotiable = fixture.get("non_negotiable_clauses", [])

    # --- Completeness (weight 0.30) ---
    matched_clauses = 0
    total_clauses = len(ground_truth)
    for conflict in ground_truth:
        clause_name = conflict["clause_name"].lower()
        # Check if keywords from clause_name appear in final text
        keywords = clause_name.split()
        if any(kw.lower() in final_text.lower() for kw in keywords):
            matched_clauses += 1
    completeness = matched_clauses / total_clauses if total_clauses > 0 else 1.0

    # --- Conflict resolution (weight 0.30) ---
    resolved_count = 0
    for conflict in ground_truth:
        try:
            prompt = f"""Does this final contract text contain a resolution for the "{conflict['clause_name']}" clause that is different from both the original vendor and client versions?
Vendor: {conflict['vendor_text']}
Client: {conflict['client_text']}
Final contract excerpt: {final_text[:3000]}
Respond ONLY with JSON: {{"resolved": true|false}}"""
            response = llm_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.1,
            )
            text = response.choices[0].message.content.strip()
            if "```" in text:
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
                text = text.strip()
            result = json.loads(text)
            if result.get("resolved", False):
                resolved_count += 1
        except Exception:
            pass
    conflict_resolution = resolved_count / len(ground_truth) if ground_truth else 1.0

    # --- Non-negotiable respect (weight 0.20) ---
    if not non_negotiable:
        non_negotiable_score = 1.0
    else:
        matched_nn = 0
        # Build a map of clause_id -> vendor_text from ground_truth
        vendor_texts = {}
        for conflict in ground_truth:
            vendor_texts[conflict["clause_id"]] = conflict["vendor_text"]

        for clause_id in non_negotiable:
            original_text = vendor_texts.get(clause_id, "")
            if original_text and final_text:
                ratio = difflib.SequenceMatcher(None, original_text.lower(), final_text.lower()).ratio()
                # Check substring match or high similarity
                if original_text.lower() in final_text.lower() or ratio > 0.85:
                    matched_nn += 1
                else:
                    # Check if key phrases from the original appear
                    words = original_text.lower().split()[:10]
                    match_count = sum(1 for w in words if w in final_text.lower())
                    if match_count / max(len(words), 1) > 0.7:
                        matched_nn += 1
        non_negotiable_score = matched_nn / len(non_negotiable)

    # --- Coherence (weight 0.20) ---
    try:
        prompt = f"""Rate the professional quality of this contract document from 0.0 to 1.0.
Consider: logical structure, complete sentences, professional legal tone, no contradictions.
Contract: {final_text[:2000]}
Respond ONLY with JSON: {{"score": <float 0.0-1.0>}}"""
        response = llm_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.1,
        )
        text = response.choices[0].message.content.strip()
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()
        result = json.loads(text)
        coherence = float(result.get("score", 0.5))
        coherence = max(0.0, min(1.0, coherence))
    except Exception:
        coherence = 0.5

    # --- Final composite score ---
    final_score = (
        0.30 * completeness
        + 0.30 * conflict_resolution
        + 0.20 * non_negotiable_score
        + 0.20 * coherence
    )
    return max(0.0, min(1.0, final_score))
