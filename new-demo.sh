#!/bin/bash
# Usage: ./new-demo.sh "Sharma Dental Clinic" "sharma-dental"
# Creates a new demo branch ready for Railway deployment

BUSINESS_NAME="$1"
BRANCH_NAME="$2"

if [ -z "$BUSINESS_NAME" ] || [ -z "$BRANCH_NAME" ]; then
  echo "Usage: ./new-demo.sh \"Business Name\" \"branch-name\""
  exit 1
fi

echo "Creating demo for: $BUSINESS_NAME"
echo "Branch: demo/$BRANCH_NAME"

# Create new branch
git checkout -b "demo/$BRANCH_NAME"

# Update config.json with business name placeholder
python3 -c "
import json
with open('config.json') as f:
    config = json.load(f)
config['business_name'] = '$BUSINESS_NAME'
config['greeting'] = f\"Hi! I'm the $BUSINESS_NAME assistant. How can I help?\"
with open('config.json', 'w') as f:
    json.dump(config, f, indent=2)
"

echo ""
echo "✅ Branch demo/$BRANCH_NAME created!"
echo ""
echo "Next steps:"
echo "1. Edit config.json with business details"
echo "2. Update SYSTEM_PROMPT in main.py if needed"
echo "3. git add . && git commit -m 'demo: $BUSINESS_NAME'"
echo "4. git push origin demo/$BRANCH_NAME"
echo "5. Connect branch in Railway → auto-deploys"
echo "6. Send demo URL to client!"
