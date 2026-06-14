/**
 * BerryPay Integration Module for SCMA Assessment
 * 
 * This module integrates the SCMA assessment with BerryPay gateway
 * and handles payment flows, webhooks, and subscription management.
 */

class SCMAPaymentManager {
    constructor() {
        this.berryPay = new BerryPayAPI({
            environment: 'sandbox', // Change to 'production' when ready
            timeout: 30000
        });
        this.initializeEventListeners();
    }

    /**
     * Initialize payment-related event listeners
     */
    initializeEventListeners() {
        // Listen for payment completion events
        window.addEventListener('berrypay-payment-success', this.handlePaymentSuccess.bind(this));
        window.addEventListener('berrypay-payment-cancelled', this.handlePaymentCancelled.bind(this));
        window.addEventListener('berrypay-payment-error', this.handlePaymentError.bind(this));
    }

    /**
     * Process premium report payment
     */
    async processPremiumPayment(userData) {
        try {
            // Show loading state
            this.showPaymentLoading('Initiating secure payment...');

            const paymentData = {
                email: userData.email,
                company: userData.company,
                assessmentId: userData.assessmentId,
                companySize: userData.companySize,
                industry: userData.industry
            };

            // Create payment session with BerryPay
            const session = await this.berryPay.initiatePremiumPayment(paymentData);
            
            if (session.success) {
                // Store session info for later verification
                localStorage.setItem('berrypay_session', JSON.stringify({
                    sessionId: session.session_id,
                    assessmentId: userData.assessmentId,
                    timestamp: Date.now()
                }));

                // Redirect to BerryPay checkout
                window.location.href = session.checkout_url;
            } else {
                throw new Error(session.error || 'Failed to create payment session');
            }

        } catch (error) {
            console.error('Premium payment failed:', error);
            this.showPaymentError(error.message);
        } finally {
            this.hidePaymentLoading();
        }
    }

    /**
     * Process consulting package quote request
     */
    async processConsultingQuote(consultingData) {
        try {
            // Show loading state
            this.showPaymentLoading('Preparing quote request...');

            const quoteData = {
                email: consultingData.email,
                company: consultingData.company,
                assessmentId: consultingData.assessmentId,
                packageType: consultingData.packageType,
                maturityLevel: consultingData.maturityLevel,
                packageDescription: consultingData.packageDescription,
                priceRange: consultingData.priceRange,
                paymentMode: consultingData.paymentMode || 'hybrid'
            };

            // Create quote session with BerryPay
            const session = await this.berryPay.requestConsultingQuote(quoteData);
            
            if (session.success) {
                // Store session info for later verification
                localStorage.setItem('berrypay_quote_session', JSON.stringify({
                    sessionId: session.session_id,
                    assessmentId: consultingData.assessmentId,
                    packageType: consultingData.packageType,
                    timestamp: Date.now()
                }));

                // Redirect to BerryPay quote portal
                window.location.href = session.quote_url;
            } else {
                throw new Error(session.error || 'Failed to create quote session');
            }

        } catch (error) {
            console.error('Consulting quote failed:', error);
            this.showPaymentError(error.message);
        } finally {
            this.hidePaymentLoading();
        }
    }

    /**
     * Verify payment after redirect back from BerryPay
     */
    async verifyPaymentOnReturn() {
        const urlParams = new URLSearchParams(window.location.search);
        const sessionId = urlParams.get('session_id');
        
        if (sessionId) {
            try {
                const paymentStatus = await this.berryPay.verifyPayment(sessionId);
                
                if (paymentStatus.status === 'completed') {
                    this.handlePaymentSuccess(paymentStatus);
                } else {
                    this.handlePaymentCancelled(paymentStatus);
                }
            } catch (error) {
                this.handlePaymentError(error);
            }
        }
    }

    /**
     * Handle successful payment
     */
    handlePaymentSuccess(paymentData) {
        // Update UI to show success
        this.showPaymentSuccess();
        
        // Unlock premium features
        this.unlockPremiumFeatures(paymentData);
        
        // Track analytics event
        this.trackPaymentEvent('payment_success', paymentData);
        
        // Clear temporary session data
        localStorage.removeItem('berrypay_session');
    }

    /**
     * Handle cancelled payment
     */
    handlePaymentCancelled(paymentData) {
        this.showPaymentCancelled();
        this.trackPaymentEvent('payment_cancelled', paymentData);
    }

    /**
     * Handle payment error
     */
    handlePaymentError(error) {
        this.showPaymentError(error.message || 'Payment processing failed');
        this.trackPaymentEvent('payment_error', { error: error.message });
    }

    /**
     * Unlock premium features for the user
     */
    unlockPremiumFeatures(paymentData) {
        // Set premium user flag
        localStorage.setItem('scma_premium_user', JSON.stringify({
            active: true,
            assessmentId: paymentData.assessment_id,
            purchaseDate: new Date().toISOString(),
            features: ['advanced_benchmarking', 'detailed_reports', 'industry_insights']
        }));

        // Refresh the results display with premium features
        if (window.lastResults) {
            displayResults(window.lastResults, true); // true = premium mode
        }
    }

    /**
     * Check if user has premium access
     */
    hasPremiumAccess(assessmentId = null) {
        const premiumData = localStorage.getItem('scma_premium_user');
        if (!premiumData) return false;

        const premium = JSON.parse(premiumData);
        if (!premium.active) return false;

        // Check if assessment-specific (optional)
        if (assessmentId && premium.assessmentId !== assessmentId) {
            return false;
        }

        return true;
    }

    /**
     * Show payment loading state
     */
    showPaymentLoading(message) {
        // Create or show loading modal
        const loadingModal = document.getElementById('payment-loading') || this.createLoadingModal();
        loadingModal.querySelector('.loading-message').textContent = message;
        loadingModal.style.display = 'flex';
    }

    /**
     * Hide payment loading state
     */
    hidePaymentLoading() {
        const loadingModal = document.getElementById('payment-loading');
        if (loadingModal) {
            loadingModal.style.display = 'none';
        }
    }

    /**
     * Show payment success message
     */
    showPaymentSuccess() {
        alert('🎉 Payment successful! Premium features are now unlocked.');
    }

    /**
     * Show payment cancelled message
     */
    showPaymentCancelled() {
        alert('⚠️ Payment was cancelled. You can try again anytime.');
    }

    /**
     * Show payment error message
     */
    showPaymentError(message) {
        alert(`❌ Payment failed: ${message}\n\nPlease try again or contact support.`);
    }

    /**
     * Create loading modal for payment processes
     */
    createLoadingModal() {
        const modal = document.createElement('div');
        modal.id = 'payment-loading';
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.7);
            display: none;
            justify-content: center;
            align-items: center;
            z-index: 10000;
        `;
        
        modal.innerHTML = `
            <div style="background: white; padding: 40px; border-radius: 10px; text-align: center; max-width: 400px;">
                <div class="spinner" style="width: 40px; height: 40px; border: 4px solid #f3f3f3; border-top: 4px solid #27ae60; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 20px;"></div>
                <h3>Processing Payment</h3>
                <p class="loading-message">Initiating secure payment...</p>
                <small>Please do not close this window</small>
            </div>
            <style>
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
            </style>
        `;
        
        document.body.appendChild(modal);
        return modal;
    }

    /**
     * Track payment analytics events
     */
    trackPaymentEvent(eventName, data) {
        // Integration with analytics (Google Analytics, etc.)
        if (typeof gtag !== 'undefined') {
            gtag('event', eventName, {
                event_category: 'payment',
                event_label: 'berrypay',
                value: data.amount || 0
            });
        }
        
        console.log('Payment Event:', eventName, data);
    }
}

// Initialize payment manager when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    window.scmaPaymentManager = new SCMAPaymentManager();
    
    // Check for payment return on page load
    if (window.location.search.includes('session_id')) {
        window.scmaPaymentManager.verifyPaymentOnReturn();
    }
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SCMAPaymentManager;
}