import os
import tweepy
import pandas as pd
import numpy as np
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import joblib
from sklearn.preprocessing import StandardScaler
import logging

logger = logging.getLogger(__name__)

class TwitterUserView(APIView):
    def post(self, request):
        username = request.data.get('username')
        if not username:
            return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Check if bearer token exists
            bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
            if not bearer_token:
                logger.error("Twitter Bearer Token not found in environment variables")
                return Response(
                    {'error': 'Twitter API credentials not configured'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Initialize Twitter API client
            client = tweepy.Client(
                bearer_token=bearer_token,
                wait_on_rate_limit=True
            )

            # Get user data
            user = client.get_user(username=username, user_fields=[
                'created_at', 'description', 'public_metrics', 'verified'
            ])

            if not user.data:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            # Extract features
            user_data = user.data
            created_at = user_data.created_at
            account_age_days = (datetime.now(created_at.tzinfo) - created_at).days

            features = {
                'verified': int(user_data.verified),
                'followers_count': user_data.public_metrics['followers_count'],
                'following_count': user_data.public_metrics['following_count'],
                'tweet_count': user_data.public_metrics['tweet_count'],
                'listed_count': user_data.public_metrics['listed_count'],
                'account_age_days': account_age_days,
                'description_len': len(user_data.description or ''),
                'username_len': len(username),
                'followers_per_day': user_data.public_metrics['followers_count'] / (account_age_days + 1),
                'follower_following_ratio': user_data.public_metrics['followers_count'] / (user_data.public_metrics['following_count'] + 1),
                'tweets_per_day': user_data.public_metrics['tweet_count'] / (account_age_days + 1),
                'followers_to_tweets': user_data.public_metrics['followers_count'] / (user_data.public_metrics['tweet_count'] + 1),
                'follow_to_following': user_data.public_metrics['following_count'] / (user_data.public_metrics['followers_count'] + 1),
                'listed_per_follower': user_data.public_metrics['listed_count'] / (user_data.public_metrics['followers_count'] + 1),
                'description_density': len(user_data.description or '') / (account_age_days + 1)
            }

            try:
                # Load model and scaler
                model_path = os.path.join(settings.BASE_DIR, 'models', 'xgb_model.pkl')
                scaler_path = os.path.join(settings.BASE_DIR, 'models', 'feature_scaler.pkl')
                
                if not os.path.exists(model_path):
                    logger.error(f"Model file not found at {model_path}")
                    return Response(
                        {'error': 'Model file not found'}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                
                if not os.path.exists(scaler_path):
                    logger.error(f"Scaler file not found at {scaler_path}")
                    return Response(
                        {'error': 'Scaler file not found'}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

                model = joblib.load(model_path)
                scaler = joblib.load(scaler_path)

                # Prepare features for prediction
                feature_names = [
                    'verified', 'followers_count', 'following_count', 'tweet_count', 'listed_count',
                    'account_age_days', 'description_len', 'username_len',
                    'followers_per_day', 'follower_following_ratio', 'tweets_per_day',
                    'followers_to_tweets', 'follow_to_following', 'listed_per_follower',
                    'description_density'
                ]
                
                X = pd.DataFrame([features])[feature_names]
                X_scaled = scaler.transform(X)
                
                # Make prediction
                prediction = model.predict(X_scaled)[0]
                probability = model.predict_proba(X_scaled)[0][1]

                return Response({
                    'username': username,
                    'is_bot': bool(prediction),
                    'bot_probability': float(probability),
                    'features': features
                })

            except Exception as e:
                logger.error(f"Error during model prediction: {str(e)}")
                return Response(
                    {'error': f'Error during prediction: {str(e)}'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        except tweepy.TweepyException as e:
            logger.error(f"Twitter API error: {str(e)}")
            return Response(
                {'error': f'Twitter API error: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response(
                {'error': f'Unexpected error: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 