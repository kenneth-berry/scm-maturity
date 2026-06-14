/**
 * BerryPay Gateway API Integration
 * 
 * This module handles all API interactions with the separate BerryPay gateway application.
 * It provides functions for payment processing, subscription management, and transaction status.
 */

class BerryPayAPI {
    constructor(config = {}) {
        // Configuration for BerryPay Gateway
        this.baseURL = config.baseURL || 'https://api.berrypay.com/v1';
        this.apiKey = config.apiKey || process.env.BERRYPAY_API_KEY;
        this.environment = config.environment || 'sandbox'; // 'sandbox' or 'production'
        this.timeout = config.timeout || 30000; // 30 seconds
    }

    /**
     * Initialize payment session for premium SCMA report
     * @param {Object} paymentData - Payment information
     * @returns {Promise<Object>} Payment session response
     */
    async initiatePremiumPayment(paymentData) {
        const payload = {
            product_type: 'premium_report',
            amount: 9900, // $99.00 in cents
            currency: 'USD',
            customer: {
                email: paymentData.email,
                company: paymentData.company,
                assessment_id: paymentData.assessmentId
            },
            metadata: {
                assessment_id: paymentData.assessmentId,
                company_size: paymentData.companySize,
                industry: paymentData.industry,
                source: 'scma_assessment'
            },
            success_url: `${window.location.origin}/payment-success?session_id={CHECKOUT_SESSION_ID}`,
            cancel_url: `${window.location.origin}/payment-cancelled`,
            webhook_url: `${window.location.origin}/webhooks/berrypay`
        };

        return this._makeRequest('POST', '/payments/sessions', payload);
    }

    /**
     * Request consulting package quote
     * @param {Object} quoteData - Quote request information
     * @returns {Promise<Object>} Quote session response
     */
    async requestConsultingQuote(quoteData) {
        const payload = {
            product_type: 'consulting_package',
            package_type: quoteData.packageType, // 'diagnostic', 'advisory', 'transformation'
            amount: this._getPackageAmount(quoteData.packageType),
            currency: 'USD',
            customer: {
                email: quoteData.email,
                company: quoteData.company,
                assessment_id: quoteData.assessmentId
            },
            metadata: {
                assessment_id: quoteData.assessmentId,
                maturity_level: quoteData.maturityLevel,
                package_description: quoteData.packageDescription,
                price_range: quoteData.priceRange,
                source: 'scma_consulting'
            },
            payment_mode: quoteData.paymentMode || 'hybrid', // 'instant', 'terms', 'hybrid'
            success_url: `${window.location.origin}/quote-success?session_id={CHECKOUT_SESSION_ID}`,
            cancel_url: `${window.location.origin}/quote-cancelled`,
            webhook_url: `${window.location.origin}/webhooks/berrypay`
        };

        return this._makeRequest('POST', '/quotes/sessions', payload);
    }

    /**
     * Verify payment status
     * @param {string} sessionId - Payment session ID
     * @returns {Promise<Object>} Payment status
     */
    async verifyPayment(sessionId) {
        return this._makeRequest('GET', `/payments/sessions/${sessionId}`);
    }

    /**
     * Get customer subscription status
     * @param {string} customerId - Customer ID or email
     * @returns {Promise<Object>} Subscription details
     */
    async getSubscriptionStatus(customerId) {
        return this._makeRequest('GET', `/subscriptions/customer/${encodeURIComponent(customerId)}`);
    }

    /**
     * Handle webhook verification
     * @param {Object} payload - Webhook payload
     * @param {string} signature - Webhook signature
     * @returns {boolean} Verification result
     */
    verifyWebhook(payload, signature) {
        // This would implement webhook signature verification
        // For now, return true for development
        console.log('Webhook received:', payload);
        return true;
    }

    /**
     * Get package amount based on type
     * @private
     */
    _getPackageAmount(packageType) {
        const amounts = {
            'diagnostic': 500000, // $5,000.00 in cents (average)
            'advisory': 2500000,  // $25,000.00 in cents (average)
            'transformation': 10000000 // $100,000.00 in cents (average)
        };
        return amounts[packageType] || 0;
    }

    /**
     * Make HTTP request to BerryPay API
     * @private
     */
    async _makeRequest(method, endpoint, data = null) {
        const url = `${this.baseURL}${endpoint}`;
        
        const options = {
            method,
            headers: {
                'Authorization': `Bearer ${this.apiKey}`,
                'Content-Type': 'application/json',
                'X-BerryPay-Version': '2024-10-01',
                'User-Agent': 'SCMA-Assessment/1.0'
            }
        };

        if (data) {
            options.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(url, options);
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(`BerryPay API Error: ${response.status} - ${errorData.message || response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('BerryPay API Request Failed:', error);
            throw error;
        }
    }
}

// Configuration for different environments
const BerryPayConfig = {
    sandbox: {
        baseURL: 'https://sandbox-api.berrypay.com/v1',
        environment: 'sandbox'
    },
    production: {
        baseURL: 'https://api.berrypay.com/v1',
        environment: 'production'
    }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { BerryPayAPI, BerryPayConfig };
}

// Global instance for browser usage
window.BerryPayAPI = BerryPayAPI;
window.BerryPayConfig = BerryPayConfig;