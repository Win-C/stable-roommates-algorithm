# stable-roommates-algorithm

Stable pairing means no pair will run off:
        - x cannot have a better partner than y
        - y cannot have a worse partner than x

Target: time complexity O(n^2)
Objective: determine if stable pairings are possible and return pairs

Algorithm:
    Step 0: Get ranked input from users for preferences. Need even # users
            TODO: add function to insert dummy variable for odd # users

    *Phase 1*
        Step 1: Make proposals.

                To be able to determine if table is stable, everyone needs
                - to send a proposal
                - receive a proposal and accept a proposal*
                *can reject accepted proposal if better offer received

        Step 2: Is this a stable table? Return True or False.

        Step 2: Eliminate all preference pairs after accepted proposal
                in preference list (successors will be worse than current
                offer).

        Step 3: Is length of participants' preference list equal to 1?
                - Yes, stable matches found and return pairs
                - No, proceed to phase 2

    *Phase 2*
        Step 1: Start with first participant with preference list of at
                least 2.

                Create 'p' and 'q' lists
                p: [participant   ],[last item of q0],[last item of q1]...
                q: [2nd item of p0],[2nd item of p1 ],[2nd item of p2 ]...

                Continue process until a pattern repeats in p. This is a
                cycle to eliminate

        Step 2: Put pairs into a cycle list [(q0, p1), (q1, p2), ...]
                to generate pairs to eliminate.

                Eliminate pairs symmetrically.

        Step 3: Continue process until everyone's preference list is
                equal or less than 1
                - If all preference lists equal one then stable pair found
                    and return
                - If any preference list is empty, no stable table and
                    return UnstableTableError