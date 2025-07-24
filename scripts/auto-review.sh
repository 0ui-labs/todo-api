#!/bin/bash
# Auto Review Script - Runs zen:review and saves output to issues folder

# Get current date and next ID
DATE=$(date +%Y-%m-%d)
REVIEW_DIR="PRPs/code-reviews/issues"

# Ensure directory exists
mkdir -p "$REVIEW_DIR"

# Get next ID
if ls "$REVIEW_DIR"/*.md 2>/dev/null | grep -q .; then
    LAST_ID=$(ls "$REVIEW_DIR"/*.md | sed 's/.*\/\([0-9]\{3\}\)-.*/\1/' | sort -n | tail -1)
    NEXT_ID=$(printf "%03d" $((10#$LAST_ID + 1)))
else
    NEXT_ID="001"
fi

# Generate filename
FILENAME="${NEXT_ID}-code-review-${DATE}-comprehensive-todo-api.md"
FILEPATH="$REVIEW_DIR/$FILENAME"

echo "Starting code review..."
echo "Review will be saved to: $FILEPATH"

# Note: The actual zen:review command would need to be integrated here
# This is a placeholder for the concept
echo "Please run /zen:review and then save the output to $FILEPATH"