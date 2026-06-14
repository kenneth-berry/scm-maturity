# Berrycom Supply Chain Maturity Model (SCMM) - Complete Lovable Specification

## Overview
Build a comprehensive SaaS platform that combines:
1. **SCMM Assessment Tool** - Digital maturity assessment across 6 supply chain pillars
2. **BerryPay Gateway** - Custom payment processing with hybrid checkout options
3. **Consulting Package Integration** - Seamless upsell from assessment to consulting services
4. **Corporate Billing Portal** - B2B payment terms and invoicing system

---

## Frontend Requirements (React + Tailwind)

### Core Pages & Components

#### 1. Landing Page
- **Branding**: "Berrycom Supply Chain Maturity Model (SCMM)"
- **Value Proposition**: "Assess your supply chain maturity in 15 minutes - Get actionable insights and consulting recommendations"
- **Key Features Display**:
  - 6 Pillars Assessment (Planning, Procurement, Logistics, O2C, Technology, ESG)
  - 5 Maturity Levels (Ad-Hoc → Transformational)
  - Professional PDF Reports
  - Consulting Package Recommendations
- **Call-to-Action**: "Start Free Assessment" button
- **Contact Info**: kenkaroki@gmail.com | +254 727 866057

#### 2. Authentication System
- **Sign Up**: Name, Email, Company, Role, Phone
- **Login**: Email + Password with JWT
- **Company Profile**: KYB fields for corporate billing
- **User Dashboard**: Assessment history, reports, billing

#### 3. Assessment Interface
- **Progress Tracking**: Visual progress bar (25 questions)
- **Question Categories**: Color-coded by pillar
- **Rating System**: 1-5 Likert scale with descriptive labels:
  - 1: Ad-Hoc/Reactive
  - 2: Functional/Emerging  
  - 3: Integrated/Process-Driven
  - 4: Optimized/Data-Driven
  - 5: Transformational/Digital
- **Navigation**: Previous/Next with validation
- **Auto-Save**: Progress saved in real-time

#### 4. Results Dashboard
- **Overall Maturity Score**: Large gauge chart (1-5 scale)
- **Maturity Level Badge**: Visual indicator with description
- **Category Breakdown**: Radar chart showing 6 pillars
- **Recommendations List**: Actionable improvement suggestions
- **Consulting Package Card**: Recommended package with pricing
- **Export Options**: PDF download, JSON export

#### 5. Payment Integration
- **Hybrid Checkout**: 
  - Pay Now (Cards, Mobile Money, Bank Transfer, Wallet)
  - Pay Later (Corporate Terms - Net 30/60/90)
- **Package Selection**: 
  - Free: Basic assessment results
  - Premium ($99): Full PDF report + benchmarking
  - Consulting: Diagnostic ($3K-8K), Advisory ($15K-35K), Transformation ($50K+)
- **BerryPay Gateway**: Custom payment processing
- **Corporate Portal**: B2B invoice management and credit terms

### UI/UX Requirements
- **Responsive Design**: Mobile-first approach
- **Color Scheme**: Professional blues/greens with Berrycom branding
- **Animations**: Smooth transitions and loading states
- **Accessibility**: WCAG 2.1 AA compliance
- **Loading States**: Skeleton screens and progress indicators

---

## Backend Requirements (Node.js + Express + PostgreSQL)

### Database Schema

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    company VARCHAR(255),
    role VARCHAR(100),
    phone VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Companies table (for KYB)
CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    company_name VARCHAR(255) NOT NULL,
    registration_number VARCHAR(100),
    tax_id VARCHAR(100),
    address TEXT,
    credit_limit DECIMAL(12,2) DEFAULT 0,
    outstanding_balance DECIMAL(12,2) DEFAULT 0,
    payment_terms INTEGER DEFAULT 30, -- Net 30/60/90
    status VARCHAR(50) DEFAULT 'pending', -- pending, approved, suspended
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Assessments table
CREATE TABLE assessments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    company_id INTEGER REFERENCES companies(id),
    assessment_data JSONB, -- Store all 25 question responses
    overall_score DECIMAL(3,2),
    maturity_level VARCHAR(50),
    category_scores JSONB, -- Store scores for each pillar
    recommendations JSONB,
    consulting_package JSONB,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Payments table (BerryPay)
CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    company_id INTEGER REFERENCES companies(id),
    assessment_id INTEGER REFERENCES assessments(id),
    transaction_ref VARCHAR(100) UNIQUE,
    amount DECIMAL(12,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    payment_method VARCHAR(50), -- card, mobile_money, bank_transfer, wallet
    status VARCHAR(50) DEFAULT 'pending', -- pending, completed, failed, refunded
    payment_gateway_response JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- Invoices table (Corporate Billing)
CREATE TABLE invoices (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id),
    user_id INTEGER REFERENCES users(id),
    invoice_number VARCHAR(100) UNIQUE,
    amount DECIMAL(12,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    due_date DATE,
    status VARCHAR(50) DEFAULT 'pending', -- pending, paid, overdue, cancelled
    po_number VARCHAR(100),
    description TEXT,
    payment_terms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    paid_at TIMESTAMP
);

-- Consulting packages table
CREATE TABLE consulting_packages (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL, -- Diagnostic, Advisory, Transformation
    description TEXT,
    min_price DECIMAL(12,2),
    max_price DECIMAL(12,2),
    duration_weeks INTEGER,
    maturity_level_min INTEGER,
    maturity_level_max INTEGER,
    features JSONB
);

-- Subscriptions table
CREATE TABLE subscriptions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    plan VARCHAR(50), -- free, premium, enterprise
    status VARCHAR(50) DEFAULT 'active',
    billing_cycle VARCHAR(20) DEFAULT 'monthly',
    next_billing_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### API Endpoints

#### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get user profile
- `PUT /api/auth/profile` - Update user profile

#### Assessment
- `GET /api/assessment/questions` - Get all 25 questions
- `POST /api/assessment/start` - Start new assessment
- `PUT /api/assessment/:id/answer` - Save individual answers
- `POST /api/assessment/:id/complete` - Complete assessment and calculate results
- `GET /api/assessment/:id/results` - Get assessment results
- `GET /api/assessment/history` - Get user's assessment history

#### Payment Gateway (BerryPay)
- `POST /api/pay/initiate` - Initiate payment (hybrid checkout)
- `GET /api/pay/methods` - Get available payment methods
- `POST /api/pay/process` - Process payment (cards, mobile money, etc.)
- `POST /api/pay/webhook` - Handle payment webhooks
- `GET /api/pay/status/:transactionRef` - Check payment status

#### Corporate Billing
- `POST /api/billing/company` - Register company for credit terms
- `POST /api/billing/invoice` - Generate invoice for corporate client
- `GET /api/billing/invoices` - Get company invoices
- `PUT /api/billing/invoice/:id/pay` - Mark invoice as paid
- `GET /api/billing/aging-report` - Get aging report for overdue invoices

#### Consulting Packages
- `GET /api/consulting/packages` - Get all consulting packages
- `POST /api/consulting/quote` - Request consulting quote
- `POST /api/consulting/purchase` - Purchase consulting package

#### Reports & Analytics
- `GET /api/reports/pdf/:assessmentId` - Generate PDF report
- `GET /api/reports/benchmark` - Get industry benchmarking data
- `GET /api/admin/analytics` - Admin analytics dashboard

### Security & Compliance

#### Authentication & Authorization
- JWT token-based authentication
- Role-based access control (user, admin, super_admin)
- Password hashing with bcrypt
- Rate limiting on API endpoints

#### Payment Security
- PCI-DSS compliant card data handling
- AES-256 encryption for sensitive data
- Tokenization for payment methods
- 2FA for high-value transactions

#### Fraud Prevention
- Device fingerprinting
- Velocity checks (unusual transaction patterns)
- IP geolocation validation
- Blacklist database for known fraudsters
- AI-based anomaly detection

#### Data Protection
- GDPR/data privacy compliance
- Audit trails for all actions
- Secure data backup and recovery
- SSL/TLS encryption for all communications

---

## Payment Gateway Implementation

### Hybrid Checkout Flow

#### Pay Now Options
1. **Credit/Debit Cards**: VISA, Mastercard, UnionPay
2. **Mobile Money**: M-Pesa, Airtel Money, TigoPesa
3. **Bank Transfers**: Direct bank integration
4. **Digital Wallets**: Berrycom Wallet, other e-wallets

#### Pay Later (Corporate Terms)
1. **Company Verification**: KYB checks, registration validation
2. **Credit Assessment**: Initial limits, payment history analysis
3. **PO Validation**: Purchase order verification
4. **Approval Workflow**: Automatic/manual approval based on risk
5. **Invoice Generation**: Professional invoice with payment terms

### Corporate Billing Portal Features
- **Invoice Management**: Create, track, and manage invoices
- **Credit Control**: Monitor credit limits and outstanding balances
- **Payment Tracking**: Real-time payment status updates
- **Aging Reports**: Overdue invoice management
- **Automated Reminders**: Email/SMS payment reminders
- **Settlement Reconciliation**: Automatic payment matching

### Risk Management
- **KYB (Know Your Business)**: Company verification and due diligence
- **Credit Scoring**: Dynamic risk assessment based on payment history
- **Exposure Monitoring**: Real-time credit limit tracking
- **Collections Workflow**: Automated dunning process
- **Escrow Options**: High-value transaction protection

---

## User Journey Mapping

### 1. Individual/SME Assessment (Hybrid Checkout)
```
Landing Page → Sign Up → Assessment (25 questions) → Results Dashboard → 
Premium Upgrade (Pay Now/Pay Later) → PDF Report → Consulting Package Upsell
```

### 2. Corporate Client (Billing Portal)
```
Corporate Portal → Company Registration (KYB) → Credit Approval → 
Assessment → Results → Invoice Generation → Payment Terms → 
Consulting Package Selection → Long-term Engagement
```

### 3. Consulting Package Purchase
```
Assessment Results → Package Recommendation → Quote Request → 
Hybrid Checkout (Instant/Terms) → Contract Generation → 
Project Initiation → Ongoing Billing
```

---

## Integration Requirements

### Third-Party APIs
- **Payment Processors**: VISA, Mastercard, Safaricom (M-Pesa)
- **Banking APIs**: Local and international bank integrations
- **Credit Bureaus**: Company credit verification (where available)
- **Company Registry**: Business registration validation
- **SMS/Email**: Transactional notifications
- **Document Storage**: Secure PDF and document management

### Webhooks & Events
- Payment success/failure notifications
- Invoice due date reminders
- Assessment completion alerts
- Fraud detection alerts
- Subscription renewal notifications

---

## Deployment & Infrastructure

### Architecture
- **Frontend**: React SPA hosted on CDN
- **Backend**: Node.js microservices on Kubernetes
- **Database**: PostgreSQL cluster with read replicas
- **Cache**: Redis for session management and fast lookups
- **File Storage**: AWS S3 or equivalent for PDF reports
- **Monitoring**: Application performance monitoring and logging

### Security Infrastructure
- **WAF**: Web Application Firewall for DDoS protection
- **SSL/TLS**: End-to-end encryption
- **VPN**: Secure admin access
- **Backup**: Automated database and file backups
- **Compliance**: SOC 2, PCI-DSS compliance monitoring

---

## Monetization Strategy

### SaaS Tiers
1. **Free**: Basic assessment and general recommendations
2. **Premium ($99/assessment)**: Full PDF report, benchmarking, priority support
3. **Enterprise (Custom)**: Unlimited assessments, white-label, API access

### Consulting Packages
1. **Diagnostic ($3K-8K)**: 4-6 weeks, basic process improvement
2. **Advisory ($15K-35K)**: 6-12 weeks, integrated systems and S&OP
3. **Transformation ($50K+)**: 6-12 months, digital transformation

### Payment Gateway Revenue
- **Transaction Fees**: 2.9% + $0.30 per transaction
- **Subscription Billing**: $29/month per merchant
- **Corporate Billing**: $199/month + 1% of invoice value
- **White-label Licensing**: $999/month per partner

---

## Success Metrics & KPIs

### User Engagement
- Assessment completion rate (target: >85%)
- Time to complete assessment (target: <15 minutes)
- User retention rate (target: >60% return within 90 days)
- Premium conversion rate (target: >15%)

### Revenue Metrics
- Monthly Recurring Revenue (MRR)
- Customer Acquisition Cost (CAC)
- Customer Lifetime Value (CLV)
- Consulting package conversion rate (target: >25%)

### Payment Gateway Performance
- Transaction success rate (target: >99%)
- Payment processing time (target: <3 seconds)
- Fraud detection accuracy (target: >95% with <1% false positives)
- Settlement time (target: T+1 for most transactions)

---

## Development Phases

### Phase 1: MVP (8-12 weeks)
- Basic assessment tool with 25 questions
- Simple payment processing (cards + mobile money)
- PDF report generation
- User authentication and basic dashboard

### Phase 2: Payment Gateway (6-8 weeks)
- Hybrid checkout implementation
- Corporate billing portal
- Invoice management system
- Basic fraud prevention

### Phase 3: Advanced Features (8-10 weeks)
- Consulting package integration
- Advanced analytics and benchmarking
- White-label capabilities
- Mobile app development

### Phase 4: Scale & Optimize (Ongoing)
- AI-powered insights and predictions
- Regional expansion and localization
- Advanced fraud detection
- Enterprise integrations and APIs

---

## Lovable Implementation Prompt

```
Build a comprehensive Supply Chain Maturity Assessment SaaS platform called "Berrycom SCMM" with the following specifications:

Frontend (React + Tailwind):
- Landing page with professional branding and clear value proposition
- User authentication system with company profile management
- Multi-step assessment interface with 25 questions across 6 categories
- Results dashboard with radar charts, maturity level visualization, and recommendations
- Hybrid checkout system (Pay Now/Pay Later options)
- Corporate billing portal for B2B clients
- PDF report generation and export functionality
- Mobile-responsive design with smooth animations

Backend (Node.js + Express + PostgreSQL):
- RESTful API with JWT authentication
- Assessment engine calculating maturity levels 1-5 across 6 pillars
- Custom payment gateway with multiple payment methods
- Corporate invoicing and credit management system
- Fraud prevention with KYB verification and risk scoring
- Automated email/SMS notifications
- Comprehensive audit trails and analytics

Key Features:
- 25 structured questions evaluating Planning, Procurement, Logistics, Order-to-Cash, Technology, and ESG
- 5-level maturity framework (Ad-Hoc, Functional, Integrated, Optimized, Transformational)
- Consulting package recommendations (Diagnostic, Advisory, Transformation)
- Hybrid payment options supporting instant pay and corporate terms
- Professional PDF reports with personalized recommendations
- Real-time fraud detection and prevention
- Multi-currency support and international payment methods

Security & Compliance:
- PCI-DSS compliant payment processing
- AES-256 encryption for sensitive data
- GDPR compliance and data protection
- Advanced fraud detection with AI-powered risk scoring

Monetization:
- Freemium SaaS model with premium features
- Consulting package upsells
- Payment gateway transaction fees
- Enterprise white-label licensing

Deploy as containerized microservices with PostgreSQL database, Redis caching, and comprehensive monitoring. Ensure production-ready security, scalability, and performance optimization.
```

This specification provides a complete blueprint for building the Berrycom Supply Chain Maturity Model platform with integrated payment gateway and consulting services.