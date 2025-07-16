# Data Dictionary - Customer Engagement Analytics

## 📊 Data Sources

### Primary Systems
- **CRM System:** 18,000+ physician profiles (real-time updates)
- **Email Platform:** Campaign metrics, open/click rates (daily batch)
- **Event System:** Webinar/event registration and attendance (real-time)
- **Social Media:** Engagement metrics, reach data (daily batch)
- **Website Analytics:** Session data, conversions (real-time)

## 🗂️ Core Tables

### physician_master
Master physician database

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| physician_id | VARCHAR(10) | Unique physician identifier | PHY0001234 |
| first_name | VARCHAR(50) | Physician first name | John |
| last_name | VARCHAR(50) | Physician last name | Smith |
| specialty_code | VARCHAR(10) | Medical specialty | CARD001 |
| practice_type | VARCHAR(20) | Practice classification | Private/Hospital/Academic |
| region_code | VARCHAR(5) | Geographic region | NE001 |
| email_address | VARCHAR(100) | Primary email | john.smith@example.com |
| practice_size | INTEGER | Number of physicians | 5 |
| is_active | BOOLEAN | Active status | TRUE/FALSE |

### engagement_interactions
All physician interactions across channels

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| interaction_id | VARCHAR(15) | Unique interaction ID | INT202201150001 |
| physician_id | VARCHAR(10) | Physician reference | PHY0001234 |
| channel_type | VARCHAR(20) | Interaction channel | Email/Event/Social/Website |
| interaction_type | VARCHAR(30) | Specific action | Open/Click/Register/Attend |
| interaction_date | TIMESTAMP | When interaction occurred | 2022-01-15 09:45:22 |
| campaign_id | VARCHAR(15) | Associated campaign | CAMP2022Q1001 |
| engagement_score | DECIMAL(5,3) | Individual score | 0.750 |
| session_duration | INTEGER | Time spent (seconds) | 240 |
| conversion_flag | BOOLEAN | Conversion indicator | TRUE/FALSE |

### engagement_scores_daily
Daily aggregated engagement metrics

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| score_date | DATE | Calculation date | 2022-01-15 |
| physician_id | VARCHAR(10) | Physician reference | PHY0001234 |
| overall_score | DECIMAL(5,3) | Total engagement score | 0.685 |
| recency_score | DECIMAL(5,3) | Recency component | 0.800 |
| frequency_score | DECIMAL(5,3) | Frequency component | 0.650 |
| depth_score | DECIMAL(5,3) | Depth component | 0.720 |
| diversity_score | DECIMAL(5,3) | Channel diversity | 0.550 |
| segment_classification | VARCHAR(20) | Current segment | Watch_List/Alert/Potential |
| interaction_count_30d | INTEGER | 30-day interaction count | 12 |
| alert_flag | BOOLEAN | Alert trigger | TRUE/FALSE |

## 📊 Calculated Metrics

### Engagement Score Formula
```
Overall Score = 0.3×Recency + 0.25×Frequency + 0.25×Depth + 0.2×Diversity
```

### Component Calculations
- **Recency:** `EXP(-0.1 × days_since_last_interaction)`
- **Frequency:** `interaction_count_30d / peer_group_median`
- **Depth:** `avg_session_duration / benchmark_duration`
- **Diversity:** `unique_channels_used / total_available_channels`

### Segmentation Rules
```sql
CASE 
    WHEN overall_score >= 0.7 AND consistent_activity = TRUE THEN 'Watch_List'
    WHEN overall_score < 0.3 OR declining_trend = TRUE THEN 'Alert'
    ELSE 'Potential'
END
```

## 📈 Key Performance Indicators

### Business Metrics
- **Conversion Rate:** Physicians advancing to next funnel stage
- **Engagement Quality:** Average session duration and interaction depth
- **Campaign ROI:** Revenue attributed to marketing activities
- **Lead Velocity:** Rate of new high-potential physician identification

### Data Quality Metrics
- **Completeness:** Percentage of required fields populated
- **Accuracy:** Data validation against external sources
- **Timeliness:** Lag between interaction and data availability
- **Consistency:** Cross-system data validation results

## 🔍 Data Governance

### Privacy and Security
- Physician data anonymized for analytics
- HIPAA compliance protocols
- Role-based access controls
- Audit trail for all data access

### Data Quality Standards
- 95% completeness for critical fields
- Daily data validation reports
- Automated anomaly detection
- Monthly data quality assessments

### Update Frequencies
- **Real-time:** Website interactions, event registrations
- **Hourly:** Email engagement updates
- **Daily:** Engagement score calculations, segmentation updates
- **Weekly:** Comprehensive data validation and reporting
