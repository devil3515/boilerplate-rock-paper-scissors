import random
def player(prev_opponent_play, opponent_history=[], my_history=[], 
           pattern_length=3, strategy_tracker={}):
    
    # Initialize variables on first run
    if not prev_opponent_play:
        prev_opponent_play = 'R'
        opponent_history.clear()
        my_history.clear()
        strategy_tracker.clear()
    
    opponent_history.append(prev_opponent_play)
    
    # Define the strategies we'll use against specific bots
    strategies = {
        'counter_quincy': counter_quincy,
        'counter_mrugesh': counter_mrugesh,
        'counter_kris': counter_kris,
        'counter_abbey': counter_abbey,
        'pattern_matcher': pattern_matcher
    }
    
    # If we don't have enough history, play randomly
    if len(opponent_history) < 5:
        return random.choice(['R', 'P', 'S'])
    
    # Try to detect which bot we're playing against
    detected_bot = detect_bot(opponent_history, my_history)
    
    # If we've detected a specific bot, use its counter strategy
    if detected_bot in strategies:
        return strategies[detected_bot](opponent_history, my_history)
    
    # Default to pattern matching if we can't detect the bot
    return pattern_matcher(opponent_history, my_history, pattern_length)

def detect_bot(opponent_history, my_history):
    """Try to detect which bot we're playing against based on its play patterns."""
    if len(opponent_history) < 10:
        return None
    
    # Check for Quincy's pattern (R, R, P, P, S repeating)
    quincy_pattern = ['R', 'R', 'P', 'P', 'S']
    matches = 0
    for i in range(len(opponent_history)):
        expected = quincy_pattern[i % 5]
        if opponent_history[i] == expected:
            matches += 1
    if matches / len(opponent_history) > 0.9:
        return 'counter_quincy'
    
    # Check for Kris (always plays to counter our last move)
    # If we can predict their move based on our last move with high accuracy
    if len(my_history) > 10:
        correct = 0
        for i in range(1, len(my_history)):
            predicted = counter_move(my_history[i-1])
            if predicted == opponent_history[i]:
                correct += 1
        if correct / (len(my_history)-1) > 0.9:
            return 'counter_kris'
    
    # Check for Mrugesh (plays counter to most frequent in last 10)
    # Harder to detect, but we'll try pattern matching first
    
    # Check for Abbey (looks at last two moves)
    # Also harder to detect, pattern matching works well
    
    return None

def counter_move(move):
    """Return the move that would counter the given move."""
    return {'R': 'P', 'P': 'S', 'S': 'R'}.get(move, 'R')

def counter_quincy(opponent_history, my_history):
    """Counter Quincy's fixed pattern."""
    # Quincy's pattern is R, R, P, P, S repeating
    pattern = ['R', 'R', 'P', 'P', 'S']
    next_in_pattern = pattern[len(opponent_history) % 5]
    return counter_move(next_in_pattern)

def counter_mrugesh(opponent_history, my_history):
    """Counter Mrugesh's most-frequent strategy."""
    last_ten = opponent_history[-10:] if len(opponent_history) >= 10 else opponent_history
    if not last_ten:
        return 'P'
    most_frequent = max(set(last_ten), key=last_ten.count)
    return counter_move(most_frequent)

def counter_kris(opponent_history, my_history):
    """Counter Kris who counters our last move."""
    if not my_history:
        return 'P'
    # Kris will counter our last move, so we counter what they would play
    their_predicted_move = counter_move(my_history[-1])
    return counter_move(their_predicted_move)

def counter_abbey(opponent_history, my_history):
    """Counter Abbey's pattern recognition strategy."""
    if len(opponent_history) < 2:
        return 'P'
    
    # Abbey looks at the last two moves to predict our next move
    # We'll use a similar approach but try to stay one step ahead
    last_two = "".join(opponent_history[-2:])
    potential_plays = [last_two + "R", last_two + "P", last_two + "S"]
    
    # Count occurrences of each potential play in history
    counts = {'R': 0, 'P': 0, 'S': 0}
    for i in range(len(opponent_history) - 2):
        seq = "".join(opponent_history[i:i+2])
        next_move = opponent_history[i+2] if i+2 < len(opponent_history) else 'R'
        if seq == last_two:
            counts[next_move] += 1
    
    # Predict Abbey's prediction (she'll pick the most frequent)
    prediction = max(counts, key=counts.get)
    
    # Abbey will counter her prediction, so we counter that
    abbey_move = counter_move(prediction)
    return counter_move(abbey_move)

def pattern_matcher(opponent_history, my_history, pattern_length=3):
    """Generic pattern matcher for unknown opponents."""
    if len(opponent_history) < pattern_length + 1:
        return random.choice(['R', 'P', 'S'])
    
    # Look for patterns of the given length
    last_pattern = "".join(opponent_history[-pattern_length:])
    
    # Find all occurrences of this pattern in history
    next_moves = []
    for i in range(len(opponent_history) - pattern_length):
        current_pattern = "".join(opponent_history[i:i+pattern_length])
        if current_pattern == last_pattern and i+pattern_length < len(opponent_history):
            next_moves.append(opponent_history[i+pattern_length])
    
    # If we found patterns, predict the most common next move
    if next_moves:
        predicted = max(set(next_moves), key=next_moves.count)
        return counter_move(predicted)
    
    # If no pattern found, fall back to countering their most frequent move
    return counter_mrugesh(opponent_history, my_history)