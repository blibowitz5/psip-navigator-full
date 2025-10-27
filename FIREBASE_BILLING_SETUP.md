# 💳 Firebase Billing Setup Required

## **Why Billing is Needed**

Firebase Functions requires the **Blaze (pay-as-you-go) plan** to deploy, even for free tier usage. This is a Google requirement for Cloud Functions.

## **Good News: It's Still Free!**

- **Free Tier**: 2M function invocations/month
- **Free Tier**: 400,000 GB-seconds of compute time
- **Free Tier**: 1GB of storage
- **Your Usage**: Will likely stay within free limits

## **Step 1: Upgrade to Blaze Plan**

1. **Go to**: https://console.firebase.google.com/project/psip-navigator/usage/details
2. **Click**: "Upgrade to Blaze"
3. **Select**: "Pay as you go"
4. **Add Payment Method**: Credit card (required but won't be charged for free tier)
5. **Confirm**: Upgrade

## **Step 2: Deploy Functions**

After upgrading, run:
```bash
firebase deploy --only functions
```

## **Step 3: Monitor Usage**

- **Firebase Console** → **Functions** → **Usage**
- **Set Budget Alerts** (optional but recommended)
- **Monitor** your usage to stay within free limits

## **Cost Estimation for Your App**

### **Expected Monthly Usage:**
- **Function Calls**: ~1,000-10,000 (well under 2M free)
- **Compute Time**: ~100-1,000 GB-seconds (well under 400K free)
- **Storage**: ~100MB (well under 1GB free)
- **Estimated Cost**: $0/month

### **If You Exceed Free Tier:**
- **Function Calls**: $0.40 per 1M calls
- **Compute Time**: $0.0000025 per GB-second
- **Storage**: $0.026 per GB per month

## **Alternative: Use Firebase Hosting Only**

If you prefer not to add billing, you can:

1. **Deploy just the frontend** to Firebase Hosting
2. **Use your existing Railway backend** (keep it running)
3. **Update frontend** to point to Railway instead of Firebase Functions

## **Step 4: Deploy Frontend to Netlify (No Billing Required)**

If you want to avoid Firebase billing entirely:

```bash
# Deploy frontend to Netlify
cd psip-plan-pal
netlify deploy --create-site --prod

# Set environment variable in Netlify:
# VITE_FIREBASE_FUNCTIONS_URL=https://your-railway-backend.railway.app
```

## **Recommendation**

**Upgrade to Blaze** - it's free for your usage level and gives you:
- ✅ Better performance
- ✅ Global CDN
- ✅ Integrated services
- ✅ No server management
- ✅ Auto-scaling

The free tier is very generous and you're unlikely to exceed it.
