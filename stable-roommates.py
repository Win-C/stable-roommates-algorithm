import random  # Used in illustrative text case


class UnstableTableError(Exception):
    """ Error for unstable table when no stable pairings are possible. """


def make_proposals(preferences):
    """ Takes in a dictionary with key equal to a participant and
        value equal to a list of that participant's preferences.

        Function iterates over each participant in order to find and return
        a record of the proposals in the form of a dictionary.

        Each participant proposes in turn using its preference list and
        receives a proposal, accepting only the highest preferred
        proposal using its preference list and rejecting all others.

        Function returns when there are no longer any participants in the
        priority queue (participants left needing to propose) or there are
        no more participants to propose to.

        For example:

        Inputs of
            preferences = {
                'A': ['B', 'D', 'C'],
                'B': ['D', 'C', 'A'],
                'C': ['A', 'D', 'B'],
                'D': ['A', 'B', 'C'],
            }
        Outputs =>
            proposal_record = {
                'A': ['D', 'D'],
                'B': ['C', 'C'],
                'C': ['B', 'B'],
                'D': ['A', 'A'],
            }
    """
    proposal_record = {}
    proposers = []  # using non-optimal list here to represent priority queue

    # Create list of proposers and empty proposal_record for each
    for participant in preferences:
        proposers.append(participant)
        proposal_record[participant] = ["", ""]

    # breakpoint()
    # to show proposers and empty proposal_record

    while proposers:
        current_proposer = proposers.pop(0)

        # Get current proposer's preference list of proposees
        current_proposer_prefs = preferences[current_proposer][:]

        # Propose to each proposee in order until accepted
        for proposee in current_proposer_prefs:
            proposee_prefs = preferences[proposee]
            current_proposer_ranking = proposee_prefs.index(current_proposer)

            # get proposal_record for proposee and proposer
            proposee_proposal_to, proposee_proposal_from = proposal_record[proposee]
            proposer_proposal_to, proposer_proposal_from = proposal_record[current_proposer]

            # breakpoint()

            # if proposee has not accepted a proposal yet
            if not proposee_proposal_from:
                proposal_record[proposee][1] = current_proposer
                proposal_record[current_proposer][0] = proposee
                break

            # if current proposal is better than accepted proposal
            elif proposee_prefs.index(proposee_proposal_from) > current_proposer_ranking:
                proposal_record[proposee][1] = current_proposer
                proposal_record[current_proposer][0] = proposee

                # Reject previously accepted proposal symmetrically
                # Step 1: reset rejected participant's proposal record
                proposal_record[proposee_proposal_from][0] = ""
                # Step 2: put rejected participant at front of priority queue
                proposers.insert(0, proposee_proposal_from)
                # Step 3: remove rejected pairing symmetrically from the preference list
                preferences[proposee].remove(proposee_proposal_from)
                preferences[proposee_proposal_from].remove(proposee)
                break

            # Otherwise, proposee prefers previously accepted proposal
            else:
                # Update preference lists for rejected proposal
                preferences[proposee].remove(current_proposer)
                preferences[current_proposer].remove(proposee)

    return proposal_record


def is_stable_table(proposal_record):
    """ Function checks if a stable table exists.
        Takes in dictionary of lists and iterates over each list.
        Checks each list item is not equal to an empty string and
        each list pair is unique.
        Returns True, if not empty and is unique; otherwise returns False

        Examples Below:

        Stable table:
            Inputs of
                proposal_record =>
                {
                    'A': ['C', 'B'],
                    'B': ['A', 'D'],
                    'C': ['D', 'A'],
                    'D': ['B', 'C']
                }
            Outputs => True

        Unstable table:
            Inputs of
                proposal_record =>
                {
                    'A': ['D', 'D'],
                    'B': ['D', 'A'],
                    'C': ['', ''],
                    'D': ['A', 'A']
                }
            Outputs => False
    """
    proposers = set()
    proposees = set()
    for (proposee, proposer) in proposal_record.values():
        if not proposee or not proposer:
            return False
        if (proposer in proposers) or (proposee in proposees):
            return False

        proposers.add(proposer)
        proposees.add(proposee)

    return True


def remove_trailing_prefs(proposal_record, preferences):
    """ Function trims each preference list by eliminating possibilities indexed
        after accepted proposal
        Takes in two dictionaries: proposal_record and preference_lists
        Returns updated preference_lists

        For example:
        Inputs of
            proposal_record = {
                'A': ['C', 'B'], - proposed to C and accepted proposal from B
                'B': ['A', 'D'], - proposed to A and accepted proposal from D
                'C': ['D', 'A'], - proposed to D and accepted proposal from A
                'D': ['B', 'C'], - proposed to B and accepted proposal from C
            }
            preferences = {
                'A': ['C', 'B', 'D'], - remove all prefs that rank lower than B
                'B': ['A', 'C', 'D'],
                'C': ['D', 'B', 'A'],
                'D': ['B', 'A', 'C'], - remove 'A' since 'D' is removed from A's list
            }

        Outputs =>
            preferences = {
                'A': ['C', 'B'],
                'B': ['A', 'C', 'D'],
                'C': ['D', 'B', 'A'],
                'D': ['B', 'C'],
            }
    """
    for proposer in proposal_record:
        proposee = proposal_record[proposer][0]
        proposee_prefs = preferences[proposee]
        proposer_ranking = proposee_prefs.index(proposer)

        successors = proposee_prefs[proposer_ranking+1:]

        # Updated proposee's preferences, removing successors
        preferences[proposee] = proposee_prefs[:proposer_ranking+1]

        # Iterate over successors, deleting proposee from own preference list
        for successor in successors:
            if proposee in preferences[successor]:
                preferences[successor].remove(proposee)

    return preferences


def get_stable_match(preferences):
    """ Function takes in dictionary of each participant's preferences and
        finds stable pairings if it exists by iterating through
        participants while preference lists are greater than 1.
        Identifies cycles and removes cycle pairs to reduce participant's
        preference lists.

        Process is repeated until stable matches are found and preference
        lists are length of 1, returning stable pairings
        Or, returns UnstableTableError if stable matches are not possible.

        Identify cycles by
        - Creating two lists (p and q) until cycle is found in p
            p: [participant   ],[last item of q0],[last item of q1]...
            q: [2nd item of p0],[2nd item of p1 ],[2nd item of p2 ]...
        - Creates cycle list to then determine pairs and removes

        For example
        Input of
            preferences = {
                'A': ['C', 'B'],
                'B': ['A', 'C', 'D'],
                'C': ['D', 'B', 'A'],
                'D': ['B', 'C']
            }

        Identifies cycle:
            Starting with 'A'
                p = ['A', 'D', 'A']
                q = ['B', 'C',]
            Cycle found in p (p[0] == p[2])
            Cycle list = [('D', 'B'), ('A', 'C')]
            Pairs removed: ('B', 'C'), ('B', 'D') and ('C', 'A')
            Process repeats

        Output =>
            preferences = {'A': ['B'], 'B': ['A'], 'C': ['D'], 'D': ['C']}
    """

    for participant in preferences:
        p = [participant, ]
        q = []

        while len(preferences[participant]) > 1:
            def find_cycle():
                new_q = preferences[p[-1]][1]
                q.append(new_q)
                q_pref_list = preferences[new_q]
                new_p = q_pref_list[-1]

                if new_p in p:
                    p.append(new_p)
                    return

                p.append(new_p)
                find_cycle()

            find_cycle()

            # start at beginning of found cycle, create list representing cycle path
            start = p.index(p[-1])
            cycle = [(p[i + 1], q[i]) for i in range(start, len(p) - 1)]
            # breakpoint()

            # from cycle path, find pairs to remove
            elimination_pairs = find_pairs_to_remove(cycle, preferences)

            try:
                preferences = remove_pairs(elimination_pairs, preferences)
            except UnstableTableError:
                return UnstableTableError

            # reset p and q for next iteration
            p = [participant, ]
            q = []

    return preferences


def find_pairs_to_remove(cycle, preferences):
    """ Find all cycle pairs to remove from each participant's preference lists.
        Takes in a list of tuples representing a cycle path found and
        dictionary containing each participant's preferences.
        Returns list of tuples representing pairs to remove.

        For example:
        Input of
            cycle = [('D', 'B'), ('A', 'C')]
            preferences = {
                'A': ['C', 'B'],
                'B': ['A', 'C', 'D'],
                'C': ['D', 'B', 'A'],
                'D': ['B', 'C']
            }

        where participant = 'B'
            participant_prefs = ['A', 'C', 'D']
            first_pref = 'A'
            successors = ['C', 'D']

        Output =>
            pairs = [('B', 'C'), ('B', 'D'), ('C', 'A')]
    """
    pairs = []
    for i, (_, participant) in enumerate(cycle):
        # grab the preference list for participant
        participant_prefs = preferences[participant]
        # first_pref is a pointer for where to start successors list
        first_pref = cycle[(i - 1) % len(cycle)][0]
        # successors is the tail of the cycle which needs to be removed
        successors = participant_prefs[participant_prefs.index(first_pref) + 1:]
        # breakpoint()

        for successor in successors:
            pair = (participant, successor)
            if pair not in pairs and pair[::-1] not in pairs:
                pairs.append((participant, successor))
    return pairs


def remove_pairs(pairs, preferences):
    """ Takes in list of tuples representing pairs to remove
        and dictionary of each participant's preferences.
        Returns updated preferences.

        For example:
        Input of
            pairs = [('B', 'C'), ('B', 'D'), ('C', 'A')]
            preferences = {
                'A': ['C', 'B'],
                'B': ['A', 'C', 'D'],
                'C': ['D', 'B', 'A'],
                'D': ['B', 'C']
            }

        Output =>
            preferences = {
                'A': ['B'],
                'B': ['A'],
                'C': ['D'],
                'D': ['C']
            }
    """

    for (left, right) in pairs:
        preferences[left].remove(right)
        preferences[right].remove(left)
        if not preferences[left] or not preferences[right]:
            raise UnstableTableError

    return preferences


def find_stable_pairings(preferences):
    """ Takes in a dictionary with key equal to a participant and
        value equal to a list of preferences

        Returns stable pairing for each participant

        For example:
        Input of
        preferences = {
            "A": ["C", "B", "D"],
            "B": ["A", "C", "D"],
            "C": ["D", "B", "A"],
            "D": ["B", "A", "C"],
        }
        Output =>
        preferences_list = {
            'A': ['B'],
            'B': ['A'],
            'C': ['D'],
            'D': ['C']
        }
    """
    proposal_record = make_proposals(preferences)

    if not is_stable_table(proposal_record):
        return UnstableTableError("No stable pairings possible")

    updated_preferences = remove_trailing_prefs(
        proposal_record,
        preferences
    )

    try:
        return get_stable_match(updated_preferences)
    except UnstableTableError:
        return UnstableTableError("No stable pairings possible")


# -------------------------- Illustrative Test Cases --------------------------

unstable = {
    "A": ["B", "C", "D"],  # Proposal Sent: B, Proposal Received: C
    "B": ["C", "A", "D"],  # Proposal Sent: C, Proposal Received: A
    "C": ["A", "B", "D"],  # Proposal Sent: A, Proposal Received: B
    "D": ["B", "A", "C"],  # Proposal Sent: X, Proposal Received: X
}

stable_phase1 = {
    "A": ["B", "C", "D"],  # Proposal Sent: B, Proposal Received: B
    "B": ["A", "C", "D"],  # Proposal Sent: A, Proposal Received: A
    "C": ["D", "B", "A"],  # Proposal Sent: D, Proposal Received: D
    "D": ["C", "B", "A"],  # Proposal Sent: C, Proposal Received: C
}

stable_phase2 = {
    "A": ["C", "B", "D"],  # Proposal Sent: C, Proposal Received: B
    "B": ["A", "C", "D"],  # Proposal Sent: A, Proposal Received: D
    "C": ["D", "B", "A"],  # Proposal Sent: D, Proposal Received: A
    "D": ["B", "A", "C"],  # Proposal Sent: B, Proposal Received: C
}

medium = {
    "A": ["C", "D", "B", "F", "E"],  # PS: D, PR: F
    "B": ["F", "E", "D", "A", "C"],  # PS: F, PR: C
    "C": ["B", "D", "E", "A", "F"],  # PS: B, PR: E
    "D": ["E", "B", "C", "F", "A"],  # PS: E, PR: A
    "E": ["C", "A", "B", "D", "F"],  # PS: C, PR: D
    "F": ["E", "A", "C", "D", "B"],  # PS: A, PR: B
}

large = {
        1: [8, 2, 9, 3, 6, 4, 5, 7, 10],
        2: [4, 3, 8, 9, 5, 1, 10, 6, 7],
        3: [5, 6, 8, 2, 1, 7, 10, 4, 9],
        4: [10, 7, 9, 3, 1, 6, 2, 5, 8],
        5: [7, 4, 10, 8, 2, 6, 3, 1, 9],
        6: [2, 8, 7, 3, 4, 10, 1, 5, 9],
        7: [2, 1, 8, 3, 5, 10, 4, 6, 9],
        8: [10, 4, 2, 5, 6, 7, 1, 3, 9],
        9: [6, 7, 2, 5, 10, 3, 4, 8, 1],
        10: [3, 1, 6, 5, 2, 9, 8, 4, 7],
}

students = {
    "Charlie": ["Peter", "Paul", "Sam", "Kelly", "Elise"],
    "Peter": ["Kelly", "Elise", "Sam", "Paul", "Charlie"],
    "Elise": ["Peter", "Sam", "Kelly", "Charlie", "Paul"],
    "Paul": ["Elise", "Charlie", "Sam", "Peter", "Kelly"],
    "Kelly": ["Peter", "Charlie", "Sam", "Elise", "Paul"],
    "Sam": ["Charlie", "Paul", "Kelly", "Elise", "Peter"],
}

# student_stable_pairings = {
#     'Charlie': ['Sam'],
#     'Peter': ['Kelly'],
#     'Elise': ['Paul'],
#     'Paul': ['Elise'],
#     'Kelly': ['Peter'],
#     'Sam': ['Charlie']
# }

rithm = {}

# Create a Rithm School student cohort size of 20
for i in range(1, 21):
    temp = []
    while len(temp) != 19:
        num = random.randint(1, 20)
        if num not in temp and num != i:
            temp.append(num)
    rithm[i] = temp


# Unstable table
proposal_record1 = make_proposals(unstable)
# print(proposal_record1)
# print(is_stable_table(proposal_record1))

# Phase 1 - stable table
# proposal_record2 = make_proposals(stable_phase1)
# print(proposal_record2)
# print(is_stable_table(proposal_record2))
# updated_prefs2 = remove_trailing_prefs(proposal_record2, stable_phase1)
# print(updated_prefs2)

# Phase 2 - stable table
# proposal_record3 = make_proposals(stable_phase2)
# updated_prefs3 = remove_trailing_prefs(proposal_record3, stable_phase2)
# print(updated_prefs3)
# stable_pairings = get_stable_match(updated_prefs3)
# print(stable_pairings)

# Full algorithm runs for ALL test cases
# print(find_stable_pairings(unstable))
# print(find_stable_pairings(stable_phase1))
# print(find_stable_pairings(stable_phase2))
# print(find_stable_pairings(medium))
# print(find_stable_pairings(large))
# print(find_stable_pairings(students))
# print(find_stable_pairings(rithm))


# ------------------------ Illustrative Test Cases Solutions ------------------

# unstable table
# No stable pairings possible

# stable_phase1_stable_pairings = {
#     'A': ['B'],
#     'B': ['A'],
#     'C': ['D'],
#     'D': ['C']
# }

# stable_phase2_stable_pairings = {
#     'A': ['B'],
#     'B': ['A'],
#     'C': ['D'],
#     'D': ['C']
# }

# medium_stable_pairings = {
#     'A': ['F'],
#     'B': ['D'],
#     'C': ['E'],
#     'D': ['B'],
#     'E': ['C'],
#     'F': ['A']
# }

# large_stable_pairings = {
#     1: [7],
#     2: [8],
#     3: [6],
#     4: [9],
#     5: [10],
#     6: [3],
#     7: [1],
#     8: [2],
#     9: [4],
#     10: [5]
# }


