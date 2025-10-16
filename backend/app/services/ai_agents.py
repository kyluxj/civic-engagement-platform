"""AI Agent services using OpenAI."""
import os
from openai import OpenAI
from datetime import datetime

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY', ''))


class NarrativeArchitect:
    """
    Narrative Architect AI Agent
    Analyzes public discourse and suggests narrative frameworks.
    """
    
    @staticmethod
    def generate_recommendations(campaign_data):
        """
        Generate narrative recommendations for a campaign.
        
        Args:
            campaign_data: Dict containing campaign objectives, target audience, etc.
        
        Returns:
            Dict containing narrative recommendations
        """
        prompt = f"""
You are an ethical Narrative Architect AI for civic engagement. Your role is to analyze public discourse and suggest EDUCATIONAL narrative frameworks only.

Campaign Context:
- Name: {campaign_data.get('name', 'N/A')}
- Type: {campaign_data.get('campaign_type', 'N/A')}
- Objectives: {campaign_data.get('objectives', 'N/A')}
- Target Audience: {campaign_data.get('target_audience', 'N/A')}

Task: Provide 3-5 ethical narrative frameworks that:
1. Focus on education and civic participation
2. Are based on factual information
3. Avoid manipulation or deception
4. Promote democratic values
5. Are transparent about sources

For each narrative framework, provide:
- Title (brief, descriptive)
- Description (2-3 sentences)
- Key messaging points (3-5 bullet points)
- Emotional tone (educational, inspiring, informative, etc.)
- Risk assessment (potential concerns or sensitivities)
- Supporting data sources

Format as JSON with this structure:
{{
  "narratives": [
    {{
      "title": "...",
      "description": "...",
      "key_points": ["...", "..."],
      "emotional_tone": "...",
      "risk_assessment": "...",
      "sources": ["..."]
    }}
  ],
  "safety_notes": "...",
  "compliance_check": "..."
}}
"""
        
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are an ethical AI assistant for civic engagement. You prioritize transparency, education, and democratic values."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
            return {
                'success': True,
                'agent_type': 'narrative_architect',
                'recommendations': result,
                'generated_at': datetime.utcnow().isoformat(),
                'model_used': 'gpt-4.1-mini'
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'agent_type': 'narrative_architect'
            }


class ContentSynthesizer:
    """
    Content Synthesizer AI Agent
    Generates educational explainer content.
    """
    
    @staticmethod
    def generate_content(content_request):
        """
        Generate educational content based on approved narrative.
        
        Args:
            content_request: Dict containing content type, topic, narrative, etc.
        
        Returns:
            Dict containing generated content
        """
        content_type = content_request.get('content_type', 'post')
        topic = content_request.get('topic', '')
        narrative = content_request.get('narrative', '')
        platform = content_request.get('platform', 'general')
        
        prompt = f"""
You are an ethical Content Synthesizer AI for civic engagement. Create EDUCATIONAL content only.

Content Request:
- Type: {content_type}
- Topic: {topic}
- Narrative Framework: {narrative}
- Target Platform: {platform}

Requirements:
1. Educational and informative (NOT persuasive advertising)
2. Fact-based with credible sources
3. Clear AI-generated labeling
4. Transparent about limitations
5. Accessible language (8th-grade reading level)
6. Include call-to-action for civic participation (voting, learning, engagement)

Generate content with:
- Title/Headline
- Main body (appropriate length for platform)
- Key facts with sources
- Call-to-action
- Hashtags (if applicable)
- Image/visual suggestions
- Provenance metadata (mark as AI-generated)

Format as JSON:
{{
  "title": "...",
  "body": "...",
  "key_facts": [
    {{"fact": "...", "source": "..."}}
  ],
  "call_to_action": "...",
  "hashtags": ["...", "..."],
  "visual_suggestions": ["...", "..."],
  "provenance": {{
    "ai_generated": true,
    "model": "gpt-4.1-mini",
    "generated_at": "...",
    "human_review_required": true
  }},
  "compliance_notes": "..."
}}
"""
        
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are an ethical AI content creator for civic education. You create transparent, factual, educational content."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
            # Add provenance metadata
            result['provenance']['generated_at'] = datetime.utcnow().isoformat()
            result['provenance']['agent_type'] = 'content_synthesizer'
            
            return {
                'success': True,
                'agent_type': 'content_synthesizer',
                'content': result,
                'generated_at': datetime.utcnow().isoformat(),
                'model_used': 'gpt-4.1-mini'
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'agent_type': 'content_synthesizer'
            }


class DistributionOptimizer:
    """
    Distribution Optimizer AI Agent
    Recommends optimal posting times and channels (advisory only).
    """
    
    @staticmethod
    def generate_recommendations(distribution_request):
        """
        Generate distribution recommendations.
        
        Args:
            distribution_request: Dict containing content, target audience, platforms, etc.
        
        Returns:
            Dict containing distribution recommendations
        """
        content_summary = distribution_request.get('content_summary', '')
        target_audience = distribution_request.get('target_audience', '')
        platforms = distribution_request.get('platforms', ['facebook', 'twitter', 'instagram'])
        budget = distribution_request.get('budget', 'N/A')
        
        prompt = f"""
You are an ethical Distribution Optimizer AI for civic engagement. Provide ADVISORY recommendations only (no automated posting).

Distribution Request:
- Content Summary: {content_summary}
- Target Audience: {target_audience}
- Platforms: {', '.join(platforms)}
- Budget: {budget}

Provide recommendations for:
1. Optimal posting times (based on audience engagement patterns)
2. Platform-specific strategies
3. Budget allocation suggestions
4. Estimated reach and engagement
5. A/B testing suggestions
6. Compliance considerations for each platform

Important: All recommendations require human approval before implementation.

Format as JSON:
{{
  "posting_schedule": [
    {{
      "platform": "...",
      "recommended_times": ["...", "..."],
      "reasoning": "...",
      "estimated_reach": "..."
    }}
  ],
  "platform_strategies": [
    {{
      "platform": "...",
      "strategy": "...",
      "content_adaptations": ["...", "..."]
    }}
  ],
  "budget_allocation": [
    {{
      "platform": "...",
      "percentage": "...",
      "estimated_cost": "...",
      "expected_roi": "..."
    }}
  ],
  "ab_testing_suggestions": ["...", "..."],
  "compliance_notes": {{
    "platform_policies": ["...", "..."],
    "required_disclosures": ["...", "..."]
  }},
  "human_approval_required": true
}}
"""
        
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are an ethical AI distribution advisor. You provide recommendations only - never automated posting."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=1500
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
            return {
                'success': True,
                'agent_type': 'distribution_optimizer',
                'recommendations': result,
                'generated_at': datetime.utcnow().isoformat(),
                'model_used': 'gpt-4.1-mini'
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'agent_type': 'distribution_optimizer'
            }


class FeedbackIntelligence:
    """
    Feedback Intelligence AI Agent
    Analyzes engagement data and flags misinformation.
    """
    
    @staticmethod
    def analyze_feedback(feedback_data):
        """
        Analyze engagement feedback and detect issues.
        
        Args:
            feedback_data: Dict containing engagement metrics, comments, mentions, etc.
        
        Returns:
            Dict containing analysis and insights
        """
        engagement_metrics = feedback_data.get('engagement_metrics', {})
        sample_comments = feedback_data.get('sample_comments', [])
        mentions = feedback_data.get('mentions', [])
        
        prompt = f"""
You are an ethical Feedback Intelligence AI for civic engagement. Analyze engagement data and flag potential issues.

Engagement Data:
- Metrics: {engagement_metrics}
- Sample Comments: {sample_comments[:10]}  # Limit to 10 for analysis
- Mentions: {mentions[:10]}

Analyze and provide:
1. Sentiment analysis (positive, neutral, negative percentages)
2. Key themes in feedback
3. Misinformation detection (flag suspicious patterns)
4. Engagement quality assessment
5. Recommendations for improvement
6. Transparency report data

Format as JSON:
{{
  "sentiment_analysis": {{
    "positive": "...",
    "neutral": "...",
    "negative": "...",
    "overall_sentiment": "..."
  }},
  "key_themes": [
    {{
      "theme": "...",
      "frequency": "...",
      "sentiment": "..."
    }}
  ],
  "misinformation_alerts": [
    {{
      "type": "...",
      "description": "...",
      "severity": "low|medium|high",
      "recommended_action": "..."
    }}
  ],
  "engagement_quality": {{
    "score": "...",
    "assessment": "...",
    "areas_for_improvement": ["...", "..."]
  }},
  "recommendations": ["...", "..."],
  "transparency_metrics": {{
    "total_interactions": "...",
    "flagged_content": "...",
    "response_rate": "..."
  }}
}}
"""
        
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are an ethical AI analyst for civic engagement. You provide transparent, accountable analysis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=1500
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
            return {
                'success': True,
                'agent_type': 'feedback_intelligence',
                'analysis': result,
                'generated_at': datetime.utcnow().isoformat(),
                'model_used': 'gpt-4.1-mini'
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'agent_type': 'feedback_intelligence'
            }


# Factory function to get appropriate agent
def get_ai_agent(agent_type):
    """Get AI agent by type."""
    agents = {
        'narrative_architect': NarrativeArchitect,
        'content_synthesizer': ContentSynthesizer,
        'distribution_optimizer': DistributionOptimizer,
        'feedback_intelligence': FeedbackIntelligence
    }
    
    return agents.get(agent_type)

