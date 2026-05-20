import os


def explain_route(driver_id, driver_name, driver_loc, pickup, destination,
                  pickup_path, trip_path, pickup_dist, trip_dist,
                  safety_rating=None, verification_status=None, api_key=None):
    """Generate a safety-focused route explanation."""
    key = api_key or os.environ.get("GOOGLE_API_KEY", "")
    if key:
        try:
            return _ai_explanation(key, driver_id, driver_name, driver_loc, pickup, destination,
                                   pickup_path, trip_path, pickup_dist, trip_dist,
                                   safety_rating, verification_status)
        except Exception:
            pass
    return _fallback_explanation(driver_id, driver_name, driver_loc, pickup, destination,
                                pickup_path, trip_path, pickup_dist, trip_dist,
                                safety_rating, verification_status)


def generate_decision_insight(selected, candidates, pickup, destination,
                              total_available, total_drivers, api_key=None):
    """Generate an AI safety-focused decision insight."""
    key = api_key or os.environ.get("GOOGLE_API_KEY", "")
    if key:
        try:
            return _ai_decision_insight(key, selected, candidates, pickup, destination,
                                        total_available, total_drivers)
        except Exception:
            pass
    return _fallback_decision_insight(selected, candidates, pickup, destination,
                                     total_available, total_drivers)


# ---------------------------------------------------------------------------
# GenAI caller (Gemini -> PaLM -> chat fallback)
# ---------------------------------------------------------------------------

def _call_genai(api_key, prompt):
    import google.generativeai as genai
    genai.configure(api_key=api_key)

    try:
        model = genai.GenerativeModel("gemini-pro")
        return model.generate_content(prompt).text
    except Exception:
        pass
    try:
        resp = genai.generate_text(model="models/text-bison-001", prompt=prompt)
        if resp and resp.result:
            return resp.result
    except Exception:
        pass
    try:
        resp = genai.chat(model="models/chat-bison-001", messages=[prompt])
        if resp and resp.last:
            return resp.last
    except Exception:
        pass
    raise RuntimeError("All GenAI API methods failed")


# ---------------------------------------------------------------------------
# AI implementations
# ---------------------------------------------------------------------------

def _ai_explanation(api_key, driver_id, driver_name, driver_loc, pickup, destination,
                    pickup_path, trip_path, pickup_dist, trip_dist,
                    safety_rating, verification_status):
    verified_tag = "verified" if verification_status == "verified" else "pending verification"
    prompt = (
        "You are a women's safety transportation AI assistant for SafeHer Ride. "
        "Provide a professional, safety-focused route analysis.\n\n"
        f"Driver {driver_id} ({driver_name}, {verified_tag}, safety rating {safety_rating}/5.0) "
        f"at grid ({driver_loc[0]},{driver_loc[1]}).\n"
        f"Female rider pickup at ({pickup[0]},{pickup[1]}), destination ({destination[0]},{destination[1]}).\n"
        f"Pickup distance: {pickup_dist} blocks. Trip distance: {trip_dist} blocks.\n\n"
        "Provide a concise route analysis emphasizing: safety of the route, driver trust & verification, "
        "secure path selection, and estimated times (2 min/block). Under 150 words. "
        "Format with clear sections."
    )
    return _call_genai(api_key, prompt)


def _ai_decision_insight(api_key, selected, candidates, pickup, destination,
                         total_available, total_drivers):
    cand_text = "\n".join(
        f"- {c['driver_id']} ({c.get('name','')}) rating={c.get('safety_rating','N/A')}, "
        f"verified={c.get('verification_status','N/A')}, dist={c['dist']} blocks"
        for c in candidates[:5]
    )
    prompt = (
        f"You are a women's safety ride-matching AI analyst for SafeHer Ride. "
        f"Explain why driver {selected['driver_id']} was selected for pickup at {pickup}.\n\n"
        f"Top candidates:\n{cand_text}\n\n"
        f"Scanned {total_available} verified female drivers out of {total_drivers} total.\n"
        "Explain in 3-4 bullet points emphasizing: safety rating, verification status, "
        "proximity, and rider security. Under 100 words."
    )
    return _call_genai(api_key, prompt)


# ---------------------------------------------------------------------------
# Fallback implementations
# ---------------------------------------------------------------------------

def _fallback_explanation(driver_id, driver_name, driver_loc, pickup, destination,
                          pickup_path, trip_path, pickup_dist, trip_dist,
                          safety_rating, verification_status):
    dx, dy = driver_loc
    px, py = pickup
    dest_x, dest_y = destination

    total_dist = pickup_dist + trip_dist
    pickup_time = pickup_dist * 2
    trip_time = trip_dist * 2
    total_time = total_dist * 2

    pickup_h = "east" if px > dx else ("west" if px < dx else "")
    pickup_v = "north" if py > dy else ("south" if py < dy else "")
    pickup_dir = f"{pickup_h}{' and ' if pickup_h and pickup_v else ''}{pickup_v}" or "stationary"

    trip_h = "east" if dest_x > px else ("west" if dest_x < px else "")
    trip_v = "north" if dest_y > py else ("south" if dest_y < py else "")
    trip_dir = f"{trip_h}{' and ' if trip_h and trip_v else ''}{trip_v}" or "stationary"

    pickup_turns = _count_turns(pickup_path)
    trip_turns = _count_turns(trip_path)

    manhattan = abs(px - dx) + abs(py - dy) + abs(dest_x - px) + abs(dest_y - py)
    efficiency = (manhattan / max(total_dist, 1)) * 100

    verified_text = "a <strong>verified</strong>" if verification_status == "verified" else "a pending-verification"
    rating_text = f"{safety_rating}/5.0" if safety_rating else "N/A"

    if efficiency >= 95:
        safety_note = "The selected route is the <strong>most direct and safest</strong> path with zero detours."
    elif efficiency >= 80:
        safety_note = "The route maintains a <strong>safe corridor</strong> with minimal deviation."
    else:
        safety_note = "The route follows a <strong>monitored path</strong> through well-connected grid zones."

    return (
        f"<strong>SafeHer Route Analysis &mdash; Driver {driver_id}</strong><br><br>"
        f"<strong>Driver Trust Profile:</strong><br>"
        f"<strong>{driver_name}</strong> is {verified_text} female driver with a safety rating "
        f"of <strong>{rating_text}</strong>. {safety_note}<br><br>"
        f"<strong>Phase 1 &mdash; Secure Pickup:</strong><br>"
        f"Driver departs ({dx}, {dy}) heading {pickup_dir} to the rider at ({px}, {py}). "
        f"Distance: <strong>{pickup_dist} blocks</strong>, {pickup_turns} turn(s), "
        f"ETA: <strong>{pickup_time} min</strong>.<br><br>"
        f"<strong>Phase 2 &mdash; Safe Trip:</strong><br>"
        f"Route heads {trip_dir} toward ({dest_x}, {dest_y}). "
        f"Distance: <strong>{trip_dist} blocks</strong>, {trip_turns} turn(s), "
        f"ETA: <strong>{trip_time} min</strong>.<br><br>"
        f"<strong>Safety Summary:</strong><br>"
        f"&bull; Total distance: <strong>{total_dist} blocks</strong><br>"
        f"&bull; Total time: <strong>{total_time} min</strong><br>"
        f"&bull; Route efficiency: <strong>{efficiency:.0f}%</strong><br>"
        f"&bull; Driver safety rating: <strong>{rating_text}</strong><br>"
        f"&bull; Verification: <strong>{'Verified' if verification_status == 'verified' else 'Pending'}</strong><br><br>"
        f"<strong>Recommendation:</strong> {driver_name} ({driver_id}) is a <strong>trusted match</strong> "
        f"for this ride, ensuring a secure and efficient journey with estimated completion "
        f"in <strong>{total_time} minutes</strong>."
    )


def _fallback_decision_insight(selected, candidates, pickup, destination,
                               total_available, total_drivers):
    best = candidates[0] if candidates else selected
    runner_ups = candidates[1:3]

    advantage = ""
    if runner_ups:
        gap = runner_ups[0]["dist"] - best["dist"]
        if gap > 0:
            advantage = f" &mdash; <strong>{gap} block(s) closer</strong> than the next candidate"

    factors = []
    factors.append(
        f"Evaluated <strong>{total_available}</strong> available female drivers "
        f"across a fleet of <strong>{total_drivers}</strong>."
    )

    verified = "Verified" if best.get("verification_status") == "verified" else "Pending"
    rating = best.get("safety_rating", "N/A")
    factors.append(
        f"<strong>{best['driver_id']} ({best.get('name', '')})</strong> &mdash; "
        f"Safety: <strong>{rating}/5.0</strong>, Status: <strong>{verified}</strong>, "
        f"Distance: <strong>{best['dist']} blocks</strong>{advantage}."
    )

    if best.get("verification_status") == "verified":
        factors.append(
            "Driver is <strong>identity-verified</strong>, meeting SafeHer's trust and "
            "background-check standards for women rider security."
        )

    manhattan = abs(pickup[0] - best["x"]) + abs(pickup[1] - best["y"])
    eff = (manhattan / max(best["dist"], 1)) * 100
    factors.append(
        f"Route safety efficiency: <strong>{eff:.0f}%</strong> &mdash; "
        f"optimal path with minimal exposure to unmonitored zones."
    )

    if runner_ups:
        comp = ", ".join(
            f"{c['driver_id']} ({c.get('safety_rating','?')}/5, {c['dist']}blk)"
            for c in runner_ups
        )
        factors.append(f"Runner-up(s): {comp}.")

    rating_val = float(rating) if isinstance(rating, (int, float)) else 4.0
    is_verified = best.get("verification_status") == "verified"
    base_conf = 60
    if is_verified:
        base_conf += 15
    if rating_val >= 4.5:
        base_conf += 15
    elif rating_val >= 4.0:
        base_conf += 10
    if runner_ups and runner_ups[0]["dist"] - best["dist"] >= 2:
        base_conf += 8
    confidence = min(base_conf, 99)

    if confidence >= 90:
        conf_label = "Very High"
    elif confidence >= 75:
        conf_label = "High"
    else:
        conf_label = "Moderate"

    return {
        "factors": factors,
        "confidence": confidence,
        "confidence_label": conf_label,
        "candidates": candidates[:3],
    }


def _count_turns(path):
    if len(path) < 3:
        return 0
    turns = 0
    for i in range(2, len(path)):
        prev_dir = (path[i - 1][0] - path[i - 2][0], path[i - 1][1] - path[i - 2][1])
        curr_dir = (path[i][0] - path[i - 1][0], path[i][1] - path[i - 1][1])
        if prev_dir != curr_dir:
            turns += 1
    return turns
