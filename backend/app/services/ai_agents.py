"""AI Agent services using Hugging Face."""
import os
import requests
from datetime import datetime
import json

# Hugging Face API configuration
HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
HF_API_KEY = os.environ.get('HUGGINGFACE_API_KEY', '')


def query_huggingface(prompt, max_tokens=2000):
    """Query Hugging Face Inference API."""
    headers = {"Authorization": f"Bearer {HF_API_KEY}"} if HF_API_KEY else {}
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_tokens,
            "temperature": 0.7,
            "return_full_text": False
        }
    }
    
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        if isinstance(result, list) and len(result) > 0:
            return result[0].get('generated_text', '')
        return str(result)
    except Exception as e:
        print(f"Hugging Face API error: {e}")
        return None


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
        
        # Always return demo data for reliable functionality
        return {
            'success': True,
            'agent_type': 'narrative_architect',
            'recommendations': {
                'narratives': [
                    {
                        'title': 'Youth Climate Action Framework',
                        'description': 'An educational narrative focusing on empowering young voters to understand climate policy and participate in democratic processes.',
                        'key_points': [
                            'Climate change affects young people\'s future most directly',
                            'Democratic participation is key to climate policy change',
                            'Education on climate science builds informed voters',
                            'Local actions can create meaningful impact'
                        ],
                        'emotional_tone': 'Educational, inspiring, empowering',
                        'risk_assessment': 'Low risk - focuses on education and democratic participation',
                        'sources': ['IPCC Reports', 'Youth Climate Movement Studies', 'Civic Engagement Research']
                    },
                    {
                        'title': 'Economic Opportunity Narrative',
                        'description': 'Connecting climate action with economic opportunities for youth, including green jobs and sustainable development.',
                        'key_points': [
                            'Green economy creates new job opportunities',
                            'Sustainable practices benefit local communities',
                            'Youth innovation drives economic growth',
                            'Education in sustainability opens career paths'
                        ],
                        'emotional_tone': 'Optimistic, practical, forward-looking',
                        'risk_assessment': 'Low risk - balanced economic and environmental focus',
                        'sources': ['Green Jobs Reports', 'Economic Development Studies', 'Youth Employment Data']
                    },
                    {
                        'title': 'Civic Participation Framework',
                        'description': 'Encouraging youth to engage in local governance and community decision-making processes.',
                        'key_points': [
                            'Local government decisions directly impact daily life',
                            'Youth voices bring fresh perspectives to policy',
                            'Civic engagement builds leadership skills',
                            'Community involvement creates lasting change'
                        ],
                        'emotional_tone': 'Empowering, community-focused, action-oriented',
                        'risk_assessment': 'Very low risk - promotes democratic values',
                        'sources': ['Civic Engagement Studies', 'Youth Leadership Research', 'Local Government Data']
                    }
                ],
                'safety_notes': 'This is DEMO DATA. All recommendations require human review and approval before use.',
                'compliance_check': 'Demo mode active - using curated educational content'
            },
            'generated_at': datetime.utcnow().isoformat(),
            'model_used': 'demo-mode',
            'demo_mode': True,
            'note': 'Using curated demo data for reliable demonstration'
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
        
        # Return demo content
        return {
            'success': True,
            'agent_type': 'content_synthesizer',
            'content': {
                'title': 'Understanding Climate Action: A Youth Guide',
                'body': 'Climate action is not just about environmental protection—it\'s about securing a sustainable future for all. Young people have a crucial role to play in shaping climate policy through democratic participation and informed voting.',
                'key_messages': [
                    'Climate change is a pressing issue that requires immediate action',
                    'Democratic processes allow citizens to influence climate policy',
                    'Education and awareness are the first steps toward change'
                ],
                'call_to_action': 'Learn more about climate policy and participate in local town halls',
                'sources': ['Climate Science Research', 'Youth Engagement Studies']
            },
            'generated_at': datetime.utcnow().isoformat(),
            'model_used': 'demo-mode',
            'demo_mode': True
        }


class DistributionOptimizer:
    """
    Distribution Optimizer AI Agent
    Recommends optimal posting times and channels.
    """
    
    @staticmethod
    def optimize_distribution(campaign_data):
        """
        Optimize content distribution strategy.
        
        Args:
            campaign_data: Dict containing campaign info and target audience
        
        Returns:
            Dict containing distribution recommendations
        """
        
        return {
            'success': True,
            'agent_type': 'distribution_optimizer',
            'recommendations': {
                'optimal_times': [
                    {'day': 'Monday', 'time': '18:00-20:00', 'reason': 'High engagement after work/school'},
                    {'day': 'Wednesday', 'time': '12:00-13:00', 'reason': 'Lunch break browsing peak'},
                    {'day': 'Saturday', 'time': '10:00-12:00', 'reason': 'Weekend leisure time'}
                ],
                'channels': [
                    {'platform': 'Instagram', 'priority': 'High', 'reason': 'Strong youth demographic presence'},
                    {'platform': 'Twitter/X', 'priority': 'Medium', 'reason': 'Good for civic discourse'},
                    {'platform': 'Community Forums', 'priority': 'High', 'reason': 'Direct local engagement'}
                ],
                'content_format': [
                    'Short videos (30-60 seconds)',
                    'Infographics with key statistics',
                    'Personal stories and testimonials'
                ]
            },
            'generated_at': datetime.utcnow().isoformat(),
            'model_used': 'demo-mode',
            'demo_mode': True
        }


class FeedbackIntelligence:
    """
    Feedback Intelligence AI Agent
    Analyzes engagement data and flags misinformation.
    """
    
    @staticmethod
    def analyze_feedback(feedback_data):
        """
        Analyze engagement and feedback data.
        
        Args:
            feedback_data: Dict containing engagement metrics and comments
        
        Returns:
            Dict containing analysis results
        """
        
        return {
            'success': True,
            'agent_type': 'feedback_intelligence',
            'analysis': {
                'sentiment': {
                    'positive': 65,
                    'neutral': 25,
                    'negative': 10
                },
                'key_themes': [
                    'Strong interest in climate education',
                    'Questions about local action opportunities',
                    'Requests for more youth-focused events'
                ],
                'engagement_metrics': {
                    'reach': 'Growing steadily',
                    'interaction_rate': 'Above average',
                    'share_rate': 'Good'
                },
                'flags': [],
                'recommendations': [
                    'Continue educational content approach',
                    'Add more local action opportunities',
                    'Consider hosting youth forums'
                ]
            },
            'generated_at': datetime.utcnow().isoformat(),
            'model_used': 'demo-mode',
            'demo_mode': True
        }
