# Time complexity O(n^2)

# Step 0: Get ranked input from users for preferences into an ADT

{
    A: [C, B, D],  # PS: C, PR: B
    B: [A, C, D],  # PS: A, PR: D
    C: [D, B, A],  # PS: D, PR: A
    D: [B, A, C],  # PS: B, PR: C
}

proposal_record = {
    A: [C, B],
    B: [A, D],
    C: [D, A],
    D: [B, C]
}

# Phase 1
#   Step 1: Is this a stable table?
#           - Everyone needs to send a proposal
#           - Everyone needs to receive a proposal and accept a proposal
#           Participants can reject a proposal accepted if a better offer comes
#           along
#   Step 2: Yes, stable table. Then eliminate all preference pairs after
#           accepted proposal in preference list. Else, can't have stable table
#   Step 3: Does everyone only have one item in list? Stable match and done.
#           Else, proceed to phase 2

# Phase 2 - If participants have at least 2 in preference list
#   Step 1: Start with first participant and create 'p' and 'q' lists
#           p: [participant],     [last item of q0], [last item of q1]...
#           q: [2nd item of p0],  [2nd item of p1],  [2nd item of p2]...
#           Continue process until a pattern repeats = cycle
#   Step 2: Connect pairs into [(q0, p1), (q1, p2), ...] for pattern 
#           and to find pairs to eliminate
#   Step 3: Continue process until only left with one preference in each list
#           or no stable table

# Edge case: odd cohort #, what would you do? Use a dummy variable for "solo"
# But what if everyone wants to be "solo", force a stable match?

# Forcing function if recently paired, weighting to move it down
# Pull pairing info from enrollment table
# Adjustment done before stable roommate algorithm process
