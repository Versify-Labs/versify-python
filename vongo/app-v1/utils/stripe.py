import stripe

from ..config import StripeConfig

stripe.api_key = StripeConfig.STRIPE_SECRET_KEY
