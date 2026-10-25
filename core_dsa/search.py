"""
Manual Search Algorithms: Linear Search vs Binary Search with Step Tracing
==========================================================================
Academic Context:
1. Linear Search:
   - Sequentially inspects each router record from index 0 to n-1.
   - Does NOT require data to be sorted.
   - Best Case Time: O(1) [item at index 0]
   - Worst Case Time: O(n) [item at last index or absent]
   - Average Case Time: O(n)
   - Space Complexity: O(1)

2. Binary Search:
   - Divide-and-conquer algorithm that repeatedly halves the search space.
   - PREREQUISITE: The array MUST be sorted by the search key (Router ID).
   - In each iteration, compares the target key with the middle element:
     * If target == mid: record found.
     * If target < mid: discard right half (high = mid - 1).
     * If target > mid: discard left half (low = mid + 1).
   - Best Case Time: O(1) [item at middle on first try]
   - Worst Case Time: O(log n)
   - Average Case Time: O(log n)
   - Space Complexity: O(1) iterative

Academic Note:
For small router datasets (e.g., 6 to 30 routers), CPU cycle differences are sub-millisecond
and subject to system timing noise. The NUMBER OF COMPARISONS is the pure, deterministic
theoretical metric for demonstrating algorithmic efficiency.
"""

import time
from typing import List, Dict, Any, Optional, Tuple


def linear_search_routers(
    routers: List[Dict[str, Any]],
    target_id: str
) -> Dict[str, Any]:
    """
    Perform manual Linear Search on a list of router dictionaries.
    Counts exact comparisons and logs step-by-step trace.
    """
    start_time = time.perf_counter()
    comparisons = 0
    steps: List[Dict[str, Any]] = []
    found = False
    found_record: Optional[Dict[str, Any]] = None
    target_clean = target_id.strip().upper()

    for idx, router in enumerate(routers):
        comparisons += 1
        curr_id = router.get("id", "").strip().upper()
        is_match = (curr_id == target_clean)

        steps.append({
            "step": idx + 1,
            "index": idx,
            "current_id": router.get("id"),
            "target_id": target_id,
            "is_match": is_match,
            "comparisons_so_far": comparisons,
            "message": f"Step {idx + 1}: Inspected index {idx} ('{router.get('id')}'). "
                       f"{'MATCH FOUND!' if is_match else 'No match, advancing to next index.'}"
        })

        if is_match:
            found = True
            found_record = router
            break

    elapsed_ms = round((time.perf_counter() - start_time) * 1000, 4)

    return {
        "algorithm": "Linear Search",
        "target_id": target_id,
        "found": found,
        "record": found_record,
        "comparisons": comparisons,
        "total_elements": len(routers),
        "execution_time_ms": elapsed_ms,
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "steps": steps,
        "dsa_justification": (
            f"Linear Search scanned {comparisons} element(s) sequentially. "
            f"Requires no sorting, but time grows linearly O(n) with network size."
        )
    }


def binary_search_routers(
    routers: List[Dict[str, Any]],
    target_id: str
) -> Dict[str, Any]:
    """
    Perform manual Binary Search on a list of router dictionaries.
    Guarantees sorted order by router ID before starting.
    Logs low, high, mid pointers and comparisons at each step.
    """
    start_time = time.perf_counter()

    # Manual sorting by router ID (natural alphanumeric sort)
    def router_sort_key(r: Dict[str, Any]) -> str:
        # Pad digits for natural ordering e.g. R1, R2, ... R10
        r_id = r.get("id", "")
        if r_id.startswith("R") and r_id[1:].isdigit():
            return f"R{int(r_id[1:]):06d}"
        return r_id.upper()

    sorted_routers = sorted(routers, key=router_sort_key)
    target_clean = target_id.strip().upper()

    comparisons = 0
    steps: List[Dict[str, Any]] = []
    found = False
    found_record: Optional[Dict[str, Any]] = None

    low = 0
    high = len(sorted_routers) - 1
    step_num = 1

    while low <= high:
        mid = (low + high) // 2
        mid_id = sorted_routers[mid].get("id", "").strip().upper()

        comparisons += 1
        curr_step: Dict[str, Any] = {
            "step": step_num,
            "low": low,
            "high": high,
            "mid": mid,
            "mid_id": sorted_routers[mid].get("id"),
            "target_id": target_id,
            "comparisons_so_far": comparisons,
        }

        # Compare keys
        # We also use the normalized key comparison for natural ordering
        mid_key = router_sort_key(sorted_routers[mid])
        target_dummy = {"id": target_clean}
        target_key = router_sort_key(target_dummy)

        if mid_key == target_key:
            found = True
            found_record = sorted_routers[mid]
            curr_step["is_match"] = True
            curr_step["message"] = (
                f"Step {step_num}: mid={mid} ('{sorted_routers[mid].get('id')}') matches target '{target_id}'! "
                f"Binary Search succeeded in {comparisons} comparison(s)."
            )
            steps.append(curr_step)
            break
        elif target_key < mid_key:
            curr_step["is_match"] = False
            curr_step["message"] = (
                f"Step {step_num}: target '{target_id}' < mid '{sorted_routers[mid].get('id')}'. "
                f"Discarding right sub-array [{mid}..{high}]. Setting high = {mid - 1}."
            )
            steps.append(curr_step)
            high = mid - 1
        else:
            curr_step["is_match"] = False
            curr_step["message"] = (
                f"Step {step_num}: target '{target_id}' > mid '{sorted_routers[mid].get('id')}'. "
                f"Discarding left sub-array [{low}..{mid}]. Setting low = {mid + 1}."
            )
            steps.append(curr_step)
            low = mid + 1

        step_num += 1

    elapsed_ms = round((time.perf_counter() - start_time) * 1000, 4)

    return {
        "algorithm": "Binary Search",
        "target_id": target_id,
        "found": found,
        "record": found_record,
        "comparisons": comparisons,
        "total_elements": len(sorted_routers),
        "sorted_keys": [r.get("id") for r in sorted_routers],
        "execution_time_ms": elapsed_ms,
        "time_complexity": "O(log n)",
        "space_complexity": "O(1)",
        "steps": steps,
        "dsa_justification": (
            f"Binary Search required only {comparisons} comparison(s) across {len(sorted_routers)} elements. "
            f"By halving the search space each step, it achieves logarithmic O(log n) efficiency."
        )
    }


if __name__ == "__main__":
    print("=" * 65)
    print("ROUTER SEARCH ALGORITHMS: LINEAR SEARCH vs BINARY SEARCH")
    print("=" * 65)

    sample_routers = [
        {"id": "R1", "name": "Gateway Router", "ip": "192.168.1.1"},
        {"id": "R2", "name": "Core Router North", "ip": "192.168.1.2"},
        {"id": "R3", "name": "Core Router South", "ip": "192.168.1.3"},
        {"id": "R4", "name": "Aggregation Switch East", "ip": "192.168.1.4"},
        {"id": "R5", "name": "Aggregation Switch West", "ip": "192.168.1.5"},
        {"id": "R6", "name": "Border Gateway Egress", "ip": "192.168.1.6"},
    ]

    target = "R6"
    print(f"\nSearching for Target: '{target}' across {len(sample_routers)} routers\n")

    # Linear Search
    lin_res = linear_search_routers(sample_routers, target)
    print("--- [1] LINEAR SEARCH (O(n)) ---")
    print(f"  - Found: {lin_res['found']}")
    print(f"  - Key Comparisons: {lin_res['comparisons']}")
    print(f"  - Time Complexity: {lin_res['time_complexity']}")
    for step in lin_res['steps']:
        print(f"    * {step['message']}")

    # Binary Search
    bin_res = binary_search_routers(sample_routers, target)
    print("\n--- [2] BINARY SEARCH (O(log n)) ---")
    print(f"  - Found: {bin_res['found']}")
    print(f"  - Key Comparisons: {bin_res['comparisons']}")
    print(f"  - Time Complexity: {bin_res['time_complexity']}")
    for step in bin_res['steps']:
        print(f"    * {step['message']}")

    print("\n" + "=" * 65)
    print(f"SUMMARY: Binary Search saved {lin_res['comparisons'] - bin_res['comparisons']} comparison(s) vs Linear Search!")
    print("=" * 65)

