/**
 * BerryPay Webhook Handler for SCMA Assessment
 * 
 * This Node.js/Express handler processes webhooks from BerryPay gateway
 * and updates the SCMA assessment with payment confirmations.
 */

const express = require('express');
const crypto = require('crypto');
const fs = require('fs').promises;
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(express.raw({ type: 'application/json' }));
app.use(express.json());

// Webhook secret for signature verification
const WEBHOOK_SECRET = process.env.BERRYPAY_WEBHOOK_SECRET || 'your_webhook_secret_here';

/**
 * Verify webhook signature
 */
function verifyWebhookSignature(payload, signature, secret) {
    const expectedSignature = crypto
        .createHmac('sha256', secret)
        .update(payload, 'utf8')
        .digest('hex');
    
    return crypto.timingSafeEqual(
        Buffer.from(signature, 'hex'),
        Buffer.from(expectedSignature, 'hex')
    );
}

/**
 * Update assessment database with payment confirmation
 */
async function updateAssessmentPaymentStatus(assessmentId, paymentData) {
    try {
        // Path to assessment database (adjust based on your setup)
        const dbPath = path.join(__dirname, 'assessment_payments.json');
        
        // Read existing data
        let payments = [];
        try {
            const data = await fs.readFile(dbPath, 'utf8');
            payments = JSON.parse(data);
        } catch (error) {
            // File doesn't exist, start with empty array
            console.log('Creating new payments database');
        }
        
        // Add new payment record
        const paymentRecord = {
            assessment_id: assessmentId,
            payment_status: paymentData.status,
            amount: paymentData.amount,
            currency: paymentData.currency,
            customer_email: paymentData.customer?.email,
            session_id: paymentData.session_id,
            timestamp: new Date().toISOString(),
            product_type: paymentData.product_type || 'premium_report'
        };
        
        payments.push(paymentRecord);
        
        // Save updated data
        await fs.writeFile(dbPath, JSON.stringify(payments, null, 2));
        
        console.log('Payment record saved:', paymentRecord);
        return paymentRecord;
        
    } catch (error) {
        console.error('Error updating payment status:', error);
        throw error;
    }
}

/**
 * Send notification email (integrate with your email service)
 */
async function sendPaymentConfirmation(customerEmail, paymentData) {
    // TODO: Integrate with your email service (SendGrid, AWS SES, etc.)
    console.log(`Would send payment confirmation to ${customerEmail}:`, paymentData);
    
    // Example: Integration with email service
    /*
    const emailData = {
        to: customerEmail,
        subject: 'Premium SCMA Report - Payment Confirmed',
        template: 'payment_confirmation',
        data: {
            assessment_id: paymentData.assessment_id,
            amount: paymentData.amount / 100, // Convert cents to dollars
            access_url: `https://scma.berrycom.co.ke/premium-access?id=${paymentData.assessment_id}`
        }
    };
    
    await emailService.send(emailData);
    */
}

/**
 * Main webhook endpoint
 */
app.post('/webhooks/berrypay', async (req, res) => {
    try {
        const signature = req.headers['berrypay-signature'];
        const payload = req.body;
        
        // Verify webhook signature
        if (!verifyWebhookSignature(payload, signature, WEBHOOK_SECRET)) {
            console.error('Invalid webhook signature');
            return res.status(401).json({ error: 'Invalid signature' });
        }
        
        const event = JSON.parse(payload);
        console.log('Received webhook event:', event.event);
        
        switch (event.event) {
            case 'payment.completed':
                await handlePaymentCompleted(event.data);
                break;
                
            case 'payment.failed':
                await handlePaymentFailed(event.data);
                break;
                
            case 'quote.accepted':
                await handleQuoteAccepted(event.data);
                break;
                
            case 'subscription.created':
                await handleSubscriptionCreated(event.data);
                break;
                
            default:
                console.log('Unhandled webhook event:', event.event);
        }
        
        res.status(200).json({ received: true });
        
    } catch (error) {
        console.error('Webhook processing error:', error);
        res.status(500).json({ error: 'Webhook processing failed' });
    }
});

/**
 * Handle successful payment
 */
async function handlePaymentCompleted(data) {
    console.log('Processing completed payment:', data);
    
    try {
        // Update assessment database
        await updateAssessmentPaymentStatus(data.assessment_id, {
            ...data,
            status: 'completed'
        });
        
        // Send confirmation email
        if (data.customer_email) {
            await sendPaymentConfirmation(data.customer_email, data);
        }
        
        // Log for analytics
        console.log(`Payment completed: ${data.assessment_id} - $${data.amount / 100}`);
        
    } catch (error) {
        console.error('Error handling payment completion:', error);
    }
}

/**
 * Handle failed payment
 */
async function handlePaymentFailed(data) {
    console.log('Processing failed payment:', data);
    
    try {
        // Update assessment database
        await updateAssessmentPaymentStatus(data.assessment_id || 'unknown', {
            ...data,
            status: 'failed'
        });
        
        // Log for follow-up
        console.log(`Payment failed: ${data.session_id} - ${data.reason}`);
        
    } catch (error) {
        console.error('Error handling payment failure:', error);
    }
}

/**
 * Handle accepted consulting quote
 */
async function handleQuoteAccepted(data) {
    console.log('Processing accepted quote:', data);
    
    try {
        // Update assessment database
        await updateAssessmentPaymentStatus(data.assessment_id, {
            ...data,
            status: 'quote_accepted',
            product_type: 'consulting_package'
        });
        
        // Notify sales team
        console.log(`Quote accepted: ${data.package_type} - $${data.amount / 100}`);
        
        // TODO: Send notification to sales team
        // TODO: Create CRM entry
        
    } catch (error) {
        console.error('Error handling quote acceptance:', error);
    }
}

/**
 * Handle subscription creation
 */
async function handleSubscriptionCreated(data) {
    console.log('Processing subscription creation:', data);
    
    try {
        // Update customer subscription status
        console.log(`Subscription created: ${data.customer_id} - ${data.plan}`);
        
        // TODO: Update customer database
        // TODO: Send welcome email
        
    } catch (error) {
        console.error('Error handling subscription creation:', error);
    }
}

/**
 * Health check endpoint
 */
app.get('/health', (req, res) => {
    res.json({ 
        status: 'healthy', 
        service: 'SCMA Webhook Handler',
        timestamp: new Date().toISOString()
    });
});

/**
 * Get payment status endpoint (for frontend to check)
 */
app.get('/api/payment-status/:assessmentId', async (req, res) => {
    try {
        const { assessmentId } = req.params;
        const dbPath = path.join(__dirname, 'assessment_payments.json');
        
        const data = await fs.readFile(dbPath, 'utf8');
        const payments = JSON.parse(data);
        
        const payment = payments.find(p => p.assessment_id === assessmentId);
        
        if (payment) {
            res.json({
                found: true,
                status: payment.payment_status,
                timestamp: payment.timestamp
            });
        } else {
            res.json({ found: false });
        }
        
    } catch (error) {
        console.error('Error checking payment status:', error);
        res.status(500).json({ error: 'Failed to check payment status' });
    }
});

// Start server
app.listen(PORT, () => {
    console.log(`SCMA Webhook Handler running on port ${PORT}`);
    console.log(`Webhook endpoint: http://localhost:${PORT}/webhooks/berrypay`);
    console.log(`Health check: http://localhost:${PORT}/health`);
});

module.exports = app;