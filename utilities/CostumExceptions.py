# Exception to signal a dead lock/ dead end in the graph
# Only used to pattern match
class DeadLock(Exception):
    pass


# Exception to signal a maximal trace length exceeded
# Only used to pattern match
class TraceLengthExceeded(Exception):
    pass