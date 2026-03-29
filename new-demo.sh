#!/bin/bash
# Usage: ./new-demo.sh "Business Name" "branch-name" "pet-grooming"
# Creates a new demo branch ready for Railway deployment

BUSINESS_NAME="$1"
BRANCH_NAME="$2"
TEMPLATE="${3:-pet-grooming}"

if [ -z "$BUSINESS_NAME" ] || [ -z "$BRANCH_NAME" ]; then
  echo "Usage: ./new-demo.sh \"Business Name\" \"branch-name\" [pet-grooming]"
  exit 1
fi

echo "Creating demo for: $BUSINESS_NAME"
echo "Branch: demo/$BRANCH_NAME"
echo "Template: $TEMPLATE"

# Create new branch
git checkout -b "demo/$BRANCH_NAME" 2>/dev/null || git checkout "demo/$BRANCH_NAME"

if [ "$TEMPLATE" = "pet-grooming" ]; then
  # Generate pet grooming config
  python3 -c "
import json

config = {
    'business_name': '$BUSINESS_NAME',
    'business_type': 'Pet Grooming Salon',
    'greeting': \"Hi there! I'm the virtual receptionist at $BUSINESS_NAME. How can I help you and your pup today? 🐾\",
    'hours': 'Mon-Sat 9AM-6PM',
    'location': 'USA',
    'phone': '',
    'website': '',
    'owner_name': '',
    'services': [],
    'faq': [],
    'escalation': 'Great question! Let me have the team get back to you on that. You can also call us directly for immediate help.',
    'provider': 'cerebras'
}

with open('config.json', 'w') as f:
    json.dump(config, f, indent=2)

print('✅ Pet grooming config template created')
print('📝 Edit config.json with business-specific details')
"
else
  # Update business name in existing config
  python3 -c "
import json
with open('config.json') as f:
    config = json.load(f)
config['business_name'] = '$BUSINESS_NAME'
config['greeting'] = 'Hi! I am the $BUSINESS_NAME assistant. How can I help?'
with open('config.json', 'w') as f:
    json.dump(config, f, indent=2)
"
fi

echo ""
echo "✅ Branch demo/$BRANCH_NAME created!"
echo ""
echo "Next steps:"
echo "1. Edit config.json with business details"
echo "2. git add . && git commit -m 'demo: $BUSINESS_NAME'"
echo "3. git push origin demo/$BRANCH_NAME"
echo "4. Connect branch in Railway → auto-deploys"
echo "5. Send demo URL to client!"
