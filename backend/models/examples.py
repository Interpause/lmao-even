# Few-shot examples per category (curate these carefully)
FEW_SHOT_EXAMPLES = [
    # requires_response
    {"text": "Order 10234 shipping question: Hi, could you confirm when my order 10234 will be shipped to Tampines?", "label": "requires_response"},
    {"text": "Wrong item received: I ordered the Hydrating Toner but received the Brightening Serum instead.", "label": "requires_response"},
    {"text": "Change delivery address: Can I update the delivery address for order 10240 to my office instead?", "label": "requires_response"},
    {"text": "Subscription cancellation: Please cancel my monthly skincare subscription after this month's box.", "label": "requires_response"},
    {"text": "Allergic reaction concern: After using your night cream I had redness, can you advise and possibly refund?", "label": "requires_response"},
    {"text": "Bulk corporate order: Customer wants 120 gift sets for corporate event, asks about bulk discount.", "label": "requires_response"},
    {"text": "UGC deadline: What is the latest date we need the UGC clips for the March sale?", "label": "requires_response"},
    {"text": "Damaged shipment: One carton from supplier arrived with 12 bottles leaking, need instructions.", "label": "requires_response"},
    
    # requires_decision  
    {"text": "Overtime approval: Can I approve 2 hours overtime for the warehouse team to clear the backlog?", "label": "requires_decision"},
    {"text": "Request for new pallet jack: The current pallet jack is failing, requesting approval to purchase a new one.", "label": "requires_decision"},
    {"text": "Escalated VIP ticket: VIP customer with lifetime value above 3k is requesting exception on return window.", "label": "requires_decision"},
    {"text": "Macro for refund policy: Can we update the refund macro to mention digital gift cards as non refundable?", "label": "requires_decision"},
    {"text": "Shift scheduling: We may need to open a Saturday morning shift if orders continue at this pace.", "label": "requires_decision"},
    {"text": "Invoice approval: Need approval for courier invoice INV-5521 before Friday cut off.", "label": "requires_decision"},
    {"text": "COD orders: Two COD orders from Malaysia failed delivery twice, requesting instructions.", "label": "requires_decision"},
    {"text": "Updated quote for mailer boxes: Attached is the revised quotation for 2k and 5k units of custom mailer boxes.", "label": "requires_decision"},
    
    # requires_review
    {"text": "Deck for investor call: I've updated the investor deck with the latest MRR and CAC numbers, please review.", "label": "requires_review"},
    {"text": "Q1 marketing roadmap: Sharing our proposal for Q1 campaigns and content calendar for AuroraSkin.", "label": "requires_review"},
    {"text": "Influencer shortlist: Shortlisted 5 nano influencers for the acne care bundle, see the Notion link.", "label": "requires_review"},
    {"text": "Partnership proposal: We specialise in scaling DTC beauty brands with creative testing and performance ads.", "label": "requires_review"},
    {"text": "Investor intro: I can introduce you to my friend who invests in DTC beauty brands next week.", "label": "requires_review"},
    {"text": "Monthly metrics: We should finalise MRR, CAC and LTV numbers before the investor call.", "label": "requires_review"},
    {"text": "Feedback on new FAQ page: Several customers still ask about shipping despite the updated FAQ.", "label": "requires_review"},
    {"text": "VIP customer follow-up: I've replied to the VIP customer asking for an exception on the refund window.", "label": "requires_review"},
    
    # financial_action
    {"text": "Chargeback opened: A dispute has been opened for transaction TXN-99201 for 59.90 SGD.", "label": "financial_action"},
    {"text": "GST filing: Reminder that quarterly GST filing is due on the 15th, need final sales figures.", "label": "financial_action"},
    {"text": "GST filing preparation: I've updated the GST working file with January's marketplace sales.", "label": "financial_action"},
    {"text": "Bank reconciliation reminder: You have 37 unreconciled bank statement lines pending in Xero.", "label": "financial_action"},
    {"text": "Account balance threshold alert: Your business account ending 1023 fell below the configured threshold today.", "label": "financial_action"},
    {"text": "App billing notice: Your subscription for Upsell Plus will renew in 3 days for 29 USD.", "label": "financial_action"},
    {"text": "Invoice overdue: Invoice INV-4420 is 7 days past due, please process payment.", "label": "financial_action"},
    {"text": "Tax deadline reminder: Corporate tax filing deadline is March 15, documents needed by March 10.", "label": "financial_action"},
    
    # alert
    {"text": "Low stock alert: SKU SKN-VC-30 is below threshold, current on hand 18 units.", "label": "alert"},
    {"text": "Shipment delay notice: Shipments to Australia may experience a 1 to 2 day delay due to customs congestion.", "label": "alert"},
    {"text": "Cart abandonment spike: Cart abandonment increased to 78 percent in the last 24 hours on mobile devices.", "label": "alert"},
    {"text": "Zendesk downtime: Zendesk is running slowly, some tickets are not loading for agents.", "label": "alert"},
    {"text": "Order packing backlog: We are 20 orders behind on packing, mainly yesterday night's flash sale.", "label": "alert"},
    {"text": "Keyword limited by budget: Several high performing keywords are limited by daily budget in SG market.", "label": "alert"},
    {"text": "New rating received: You received a 3 star rating on Lazada for Brightening Serum, comment mentions slow delivery.", "label": "alert"},
    {"text": "New racking installed: New racking for small parcels is in place, picking path can be optimised.", "label": "alert"},
    
    # notification
    {"text": "New order #10234: You have received a new order from Jenna Lee totaling 89.90 SGD.", "label": "notification"},
    {"text": "Payout initiated: Your weekly Stripe payout of 4,239.12 SGD has been initiated to your bank account.", "label": "notification"},
    {"text": "ROAS daily summary: Yesterday's Meta ads achieved ROAS 3.1, top campaign was Vitamin C launch ad set.", "label": "notification"},
    {"text": "Flow performance summary: Your welcome flow generated 3,129 SGD in the last 7 days, top email is Step 3.", "label": "notification"},
    {"text": "List growth report: Your main newsletter list grew by 217 subscribers in January.", "label": "notification"},
    {"text": "Theme update available: A new version of your Dawn theme is available with performance improvements.", "label": "notification"},
    {"text": "Email subject line test: Variant B with urgency wording has 6 percent higher open rate so far.", "label": "notification"},
    {"text": "Campaign invitation: You are invited to join the upcoming Beauty Super Brand Day campaign.", "label": "notification"},
    
    # personal
    {"text": "Dinner on Sunday: Are you free for family dinner this Sunday evening?", "label": "personal"},
    {"text": "Short trip to Bangkok: Thinking of a quick weekend trip, you keen to join?", "label": "personal"},
    {"text": "Membership renewal reminder: Your monthly membership will renew on 5 February, cancel 3 days before to avoid charges.", "label": "personal"},
    {"text": "Birthday party: Hey, my birthday is next Saturday, hope you can make it!", "label": "personal"},
    {"text": "Lunch plans: Want to grab lunch tomorrow? That new ramen place opened.", "label": "personal"},
    {"text": "Doctor appointment reminder: Your dental checkup is scheduled for Thursday 3pm.", "label": "personal"},
    {"text": "Package delivered: Your Amazon order was delivered to your front door.", "label": "personal"},
    {"text": "Gym class booking: Your yoga class is confirmed for tomorrow 7am.", "label": "personal"},
]