from django.apps import AppConfig
import os


class ShopifyAppConfig(AppConfig):
    name = 'shopify_app'
    # Replace the API Key and Shared Secret with the one given for your
    # App by Shopify.
    #
    # To create an application, or find the API Key and Secret, visit:
    # - for private Apps:
    #     https://${YOUR_SHOP_NAME}.myshopify.com/admin/api
    # - for partner Apps:
    #     https://www.shopify.com/services/partners/api_clients
    #
    # You can ignore this file in git using the following command:
    #   git update-index --assume-unchanged shopify_settings.py
    SHOPIFY_API_KEY = "65cdfeaa66aba266d5f37b2ecf831fb3"
    SHOPIFY_API_SECRET = "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"

    # API_VERSION specifies which api version that the app will communicate with
    SHOPIFY_API_VERSION = os.environ.get('SHOPIFY_API_VERSION', 'unstable')

    # See http://api.shopify.com/authentication.html for available scopes
    # to determine the permisssions your app will need.
    SHOPIFY_API_SCOPE = os.environ.get('SHOPIFY_API_SCOPE', 'read_products,read_orders').split(',')
