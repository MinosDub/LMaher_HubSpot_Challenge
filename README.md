# Hubspot Integration Django Project

This Django project provides integration with the HubSpot API to perform various tasks such as authentication, making API requests and retrieving contacts.

## Features

- Authenticates with the HubSpot API using OAuth 2.0
- Handles authorization callbacks
- Makes API requests to retrieve contact data
- Caches access tokens for improved performance
- Handles token refresh for expired access tokens

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/MinosDub/LMaher_HubSpot_Challenge.git

2. Install dependencies

```bash
    cd lmaher_hs_oauth
    pip install -r requirements.txt
```

3. Setup environment variables

Setup env file in root directory and create below vars 

```bash
CLIENT_ID=your_hubspot_client_id
CLIENT_SECRET=your_hubspot_client_secret
AUTH_URI=https://app.hubspot.com/oauth/authorize
TOKEN_URI=https://api.hubapi.com/oauth/v1/token
REDIRECT_URI=http://localhost:8000/hub/hubspot-callback/
SCOPES=oauth, crm.objects.contacts.read
```

4. Apply migrations

```bash
python manage.py migrate
```

5. Access application at http://localhost:8000/hub/hubspot-integration/

**Usage**

Navigate to the Hubspot integration page at http://localhost:8000/hub/hubspot-integration/ to start the integration process.

Follow the authentication flow to authorize the application with HubSpot.

Once authenticated, you can access the https://api.hubapi.com/contacts/v1/lists/all/contacts/all HubSpot API endpoint through the application and retrieve a customer record. 

**Example Output**
```json
{"contacts": [{"vid": 12368139980, "canonical-vid": 12368139980, "merged-vids": [], "portal-id": 144648450, "is-contact": true, "properties": {"firstname": {"value": "Maria"}, "lastmodifieddate": {"value": "1715361985270"}, "company": {"value": "HubSpot"}, "lastname": {"value": "Johnson (Sample Contact)"}}, "form-submissions": [], "identity-profiles": [{"vid": 12368139980, "saved-at-timestamp": 1715361979736, "deleted-changed-timestamp": 0, "identities": [{"type": "EMAIL", "value": "emailmaria@hubspot.com", "timestamp": 1715361979661, "is-primary": true}, {"type": "LEAD_GUID", "value": "992471dc-88a8-42a3-a89a-8bf8690388ec", "timestamp": 1715361979733}]}], "merge-audits": [], "addedAt": 1715361979736}, {"vid": 12377098232, "canonical-vid": 12377098232, "merged-vids": [], "portal-id": 144648450, "is-contact": true, "properties": {"firstname": {"value": "Brian"}, "lastmodifieddate": {"value": "1715361995675"}, "company": {"value": "HubSpot"}, "lastname": {"value": "Halligan (Sample Contact)"}}, "form-submissions": [], "identity-profiles": [{"vid": 12377098232, "saved-at-timestamp": 1715361980038, "deleted-changed-timestamp": 0, "identities": [{"type": "EMAIL", "value": "bh@hubspot.com", "timestamp": 1715361979661, "is-primary": true}, {"type": "LEAD_GUID", "value": "be097f6a-4ec6-428c-8e66-a2e75dc6e1e0", "timestamp": 1715361980035}]}], "merge-audits": [], "addedAt": 1715361980038}], "has-more": false, "vid-offset": 0}
```