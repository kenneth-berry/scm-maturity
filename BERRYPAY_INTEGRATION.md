# BerryPay Gateway Integration Guide

## Overview
This document outlines how to connect the SCMA Assessment tool with your separate BerryPay gateway application.

## Architecture

```
SCMA Assessment App  <--> BerryPay Gateway API  <--> Payment Processors
     (Frontend)              (Your App)              (Stripe, etc.)
```

## API Endpoints Your BerryPay App Should Implement

### 1. Create Payment Session
**Endpoint:** `POST /v1/payments/sessions`

**Request:**
```json
{
  "product_type": "premium_report",
  "amount": 9900,
  "currency": "USD",
  "customer": {
    "email": "user@company.com",
    "company": "Company Name",
    "assessment_id": "scma_20241014_abc123"
  },
  "metadata": {
    "assessment_id": "scma_20241014_abc123",
    "company_size": "medium",
    "industry": "manufacturing",
    "source": "scma_assessment"
  },
  "success_url": "https://scma.berrycom.co.ke/payment-success?session_id={CHECKOUT_SESSION_ID}",
  "cancel_url": "https://scma.berrycom.co.ke/payment-cancelled",
  "webhook_url": "https://scma.berrycom.co.ke/webhooks/berrypay"
}
```

**Response:**
```json
{
  "success": true,
  "session_id": "bp_session_1234567890",
  "checkout_url": "https://checkout.berrypay.com/session/bp_session_1234567890",
  "expires_at": "2024-10-14T22:30:00Z"
}
```

### 2. Create Consulting Quote
**Endpoint:** `POST /v1/quotes/sessions`

**Request:**
```json
{
  "product_type": "consulting_package",
  "package_type": "advisory",
  "amount": 2500000,
  "currency": "USD",
  "customer": {
    "email": "user@company.com",
    "company": "Company Name",
    "assessment_id": "scma_20241014_abc123"
  },
  "metadata": {
    "assessment_id": "scma_20241014_abc123",
    "maturity_level": 3,
    "package_description": "Advisory Package for Level 3 organizations",
    "price_range": "$15,000 - $35,000",
    "source": "scma_consulting"
  },
  "payment_mode": "hybrid",
  "success_url": "https://scma.berrycom.co.ke/quote-success?session_id={CHECKOUT_SESSION_ID}",
  "cancel_url": "https://scma.berrycom.co.ke/quote-cancelled",
  "webhook_url": "https://scma.berrycom.co.ke/webhooks/berrypay"
}
```

**Response:**
```json
{
  "success": true,
  "session_id": "bp_quote_1234567890",
  "quote_url": "https://quotes.berrypay.com/session/bp_quote_1234567890",
  "expires_at": "2024-10-14T22:30:00Z"
}
```

### 3. Verify Payment Status
**Endpoint:** `GET /v1/payments/sessions/{session_id}`

**Response:**
```json
{
  "session_id": "bp_session_1234567890",
  "status": "completed",
  "payment_status": "paid",
  "amount": 9900,
  "currency": "USD",
  "customer": {
    "email": "user@company.com",
    "company": "Company Name"
  },
  "metadata": {
    "assessment_id": "scma_20241014_abc123"
  },
  "created_at": "2024-10-14T21:00:00Z",
  "completed_at": "2024-10-14T21:05:00Z"
}
```

### 4. Get Subscription Status
**Endpoint:** `GET /v1/subscriptions/customer/{customer_id}`

**Response:**
```json
{
  "customer_id": "user@company.com",
  "subscriptions": [
    {
      "id": "sub_1234567890",
      "status": "active",
      "product": "premium_reports",
      "current_period_start": "2024-10-01T00:00:00Z",
      "current_period_end": "2024-11-01T00:00:00Z"
    }
  ]
}
```

## Webhook Events

Your BerryPay app should send webhooks to the SCMA app for these events:

### Payment Completed
```json
{
  "event": "payment.completed",
  "data": {
    "session_id": "bp_session_1234567890",
    "customer_email": "user@company.com",
    "amount": 9900,
    "assessment_id": "scma_20241014_abc123",
    "timestamp": "2024-10-14T21:05:00Z"
  }
}
```

### Payment Failed
```json
{
  "event": "payment.failed",
  "data": {
    "session_id": "bp_session_1234567890",
    "customer_email": "user@company.com",
    "reason": "card_declined",
    "timestamp": "2024-10-14T21:05:00Z"
  }
}
```

### Quote Accepted
```json
{
  "event": "quote.accepted",
  "data": {
    "session_id": "bp_quote_1234567890",
    "customer_email": "user@company.com",
    "package_type": "advisory",
    "amount": 2500000,
    "assessment_id": "scma_20241014_abc123",
    "timestamp": "2024-10-14T21:05:00Z"
  }
}
```

## Integration Steps

### 1. Update SCMA HTML File
Add the API integration scripts to your index.html:

```html
<!-- Add before closing </body> tag -->
<script src="berrypay_api.js"></script>
<script src="payment_integration.js"></script>
```

### 2. Configure API Endpoints
Update the base URLs in `berrypay_api.js`:

```javascript
const BerryPayConfig = {
    sandbox: {
        baseURL: 'https://sandbox-api.berrypay.com/v1', // Your sandbox URL
        environment: 'sandbox'
    },
    production: {
        baseURL: 'https://api.berrypay.com/v1', // Your production URL
        environment: 'production'
    }
};
```

### 3. Set API Key
Configure your API key (server-side or environment variable):

```javascript
// Option 1: Environment variable (recommended)
process.env.BERRYPAY_API_KEY = 'bp_live_your_api_key_here';

// Option 2: Direct configuration (for testing only)
const berryPay = new BerryPayAPI({
    apiKey: 'bp_test_your_test_key_here',
    environment: 'sandbox'
});
```

### 4. Update Payment Buttons
Replace the existing alert-based payment buttons with actual API calls:

```javascript
// Replace in your existing upgradeToPremium function
async function upgradeToPremium() {
    if (window.scmaPaymentManager) {
        const userData = JSON.parse(localStorage.getItem('scma_user_profile') || '{}');
        userData.assessmentId = window.lastResults?.assessmentId;
        
        await window.scmaPaymentManager.processPremiumPayment(userData);
    }
}

// Replace in your existing requestConsultingQuote function
async function requestConsultingQuote(packageType) {
    if (window.scmaPaymentManager) {
        const consultingData = {
            ...JSON.parse(localStorage.getItem('scma_user_profile') || '{}'),
            assessmentId: window.lastResults?.assessmentId,
            packageType: packageType.toLowerCase(),
            maturityLevel: window.lastResults?.maturityLevel,
            packageDescription: window.lastResults?.consultingPackage?.description,
            priceRange: window.lastResults?.consultingPackage?.priceRange
        };
        
        await window.scmaPaymentManager.processConsultingQuote(consultingData);
    }
}
```

## Environment Configuration

### Development
```javascript
// In berrypay_api.js, use sandbox configuration
const berryPay = new BerryPayAPI(BerryPayConfig.sandbox);
```

### Production
```javascript
// In berrypay_api.js, use production configuration
const berryPay = new BerryPayAPI(BerryPayConfig.production);
```

## Security Considerations

1. **API Keys**: Never expose production API keys in client-side code
2. **Webhook Verification**: Implement signature verification for webhooks
3. **HTTPS**: Ensure all communication uses HTTPS
4. **Input Validation**: Validate all data before sending to BerryPay API
5. **Rate Limiting**: Implement rate limiting on your API endpoints

## Testing

### 1. Sandbox Mode
Use sandbox credentials for testing:
- API Key: `bp_test_your_sandbox_key`
- Base URL: `https://sandbox-api.berrypay.com/v1`

### 2. Test Cards
Implement test card processing in your BerryPay app:
- Success: `4242424242424242`
- Decline: `4000000000000002`
- Error: `4000000000000119`

### 3. Webhook Testing
Use tools like ngrok to test webhooks locally:
```bash
ngrok http 8000
# Use the ngrok URL for webhook_url in API calls
```

## Error Handling

The integration includes comprehensive error handling:
- Network timeouts (30 seconds)
- API errors with detailed messages
- User-friendly error displays
- Retry mechanisms for failed requests

## Support

For integration support:
- Email: kenneth@berrycom.co.ke
- Documentation: This file and inline code comments
- Test Environment: Available for integration testing