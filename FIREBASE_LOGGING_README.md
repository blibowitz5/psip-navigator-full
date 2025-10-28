# Firebase Logging Implementation

This document describes the Firebase-based user interaction logging system that replaces the previous CSV-based logging.

## Overview

The application now logs all user interactions to Firebase Firestore instead of local CSV files. This enables:
- Centralized logging across all deployments
- Real-time analytics and monitoring
- Better scalability and reliability
- Integration with Firebase ecosystem

## Implementation Details

### Firebase Collections

**Collection: `interactions`**
- Stores all user interactions (questions, answers, errors)
- Each document contains:
  - `question`: User's question
  - `answer`: System's response
  - `model`: AI model used (nelly-1.0, gpt-4, etc.)
  - `user_id`: User identifier (currently 'anonymous')
  - `timestamp`: When the interaction occurred
  - `contexts_used`: Number of context documents used (for RAG)
  - `error`: Any error messages
  - `response_time`: Time taken to generate response
  - `created_at`: Server timestamp
  - Additional fields for future use (improved_response, category, etc.)

### Files Modified

1. **`functions/index.js`**
   - Added Firebase Admin SDK initialization
   - Added `logInteractionToFirebase()` function
   - Updated all response handlers to log interactions

2. **`functions/main.py`**
   - Added Firebase Admin SDK initialization
   - Added `log_interaction_to_firebase()` function
   - Updated response handlers to log interactions

3. **`backend_api.py`**
   - Added Firebase Admin SDK initialization
   - Added `log_interaction_to_firebase()` function
   - Updated CSV logging to also log to Firebase
   - Maintains backward compatibility

4. **`functions/requirements.txt`**
   - Added `firebase-admin==6.2.0` dependency

5. **`firebase.json`**
   - Added Firestore rules configuration

6. **`firestore.rules`**
   - Security rules for the interactions collection

## Setup Instructions

### 1. Install Dependencies

```bash
# For Firebase Functions
cd functions
npm install

# For Python backend
pip install firebase-admin==6.2.0
```

### 2. Firebase Configuration

The system uses Firebase Application Default Credentials, which work automatically in:
- Firebase Functions environment
- Local development with `firebase login`
- Google Cloud environments

For custom service account:
```bash
export FIREBASE_SERVICE_ACCOUNT_PATH="/path/to/service-account-key.json"
```

### 3. Deploy Firestore Rules

```bash
firebase deploy --only firestore:rules
```

### 4. Deploy Functions

```bash
firebase deploy --only functions
```

## Testing

### Test Firebase Logging

```bash
python test_firebase_logging.py
```

### Migrate Existing CSV Data

```bash
python migrate_csv_to_firebase.py
```

## Monitoring and Analytics

### Firebase Console
- View interactions in the Firestore database
- Monitor real-time activity
- Set up alerts and monitoring

### Query Examples

```javascript
// Get all interactions from today
db.collection('interactions')
  .where('timestamp', '>=', new Date().setHours(0,0,0,0))
  .orderBy('timestamp', 'desc')
  .get()

// Get interactions by model
db.collection('interactions')
  .where('model', '==', 'nelly-1.0')
  .get()

// Get interactions with errors
db.collection('interactions')
  .where('error', '!=', null)
  .get()
```

## Security Considerations

1. **Firestore Rules**: Currently set to allow all access for development
2. **Authentication**: User identification is currently 'anonymous'
3. **Data Privacy**: Consider implementing user consent and data retention policies
4. **Access Control**: Implement proper authentication for production use

## Future Enhancements

1. **User Authentication**: Integrate with Firebase Auth
2. **Analytics Dashboard**: Create real-time analytics interface
3. **Data Export**: Add functionality to export data for analysis
4. **Retention Policies**: Implement automatic data cleanup
5. **Performance Monitoring**: Add response time and error rate tracking

## Troubleshooting

### Common Issues

1. **Firebase not initialized**
   - Check Firebase credentials
   - Verify Firebase project configuration

2. **Permission denied**
   - Check Firestore rules
   - Verify authentication

3. **Import errors**
   - Install firebase-admin: `pip install firebase-admin`
   - Check Python path configuration

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Migration from CSV

The system maintains backward compatibility with CSV logging while adding Firebase logging. To fully migrate:

1. Run the migration script: `python migrate_csv_to_firebase.py`
2. Verify data in Firebase Console
3. Test the application
4. Remove CSV logging code (optional)

## Support

For issues or questions:
1. Check Firebase Console for errors
2. Review application logs
3. Test with the provided test scripts
4. Check Firebase documentation
