"""
Integration Gateway Request Argument Parsers

Developed by Selman Tabet @ https://selman.io/
------------------------------------------------
This file contains the definitions for the parsers and their respective arguments
that would be used in the main Flask server script.
"""

from flask_restful import reqparse

tenant_get_args = reqparse.RequestParser()
tenant_get_args.add_argument(
    "company_id", type=str, help="Company ID", required=True, location='form')


tenant_post_args = reqparse.RequestParser()
tenant_post_args.add_argument(
    "merchant_url", type=str, help="Merchant Host URL (https://merchant_name.shop.com/)", required=True, location='form')
tenant_post_args.add_argument(
    "shop_token", type=str, help="Shop Access Token", required=True, location='form')
tenant_post_args.add_argument(
    "shop_api_secret", type=str, help="Shop API Secret", required=True, location='form')
tenant_post_args.add_argument(
    "company_id", type=str, help="Company ID", required=True, location='form')

tenant_delete_args = reqparse.RequestParser()
tenant_delete_args.add_argument(
    "merchant_url", type=str, help="Merchant Host URL (https://merchant_name.shop.com/)", required=True, location='form')
tenant_delete_args.add_argument(
    "shop_token", type=str, help="Shop Access Token", required=True, location='form')
tenant_delete_args.add_argument(
    "webhook_id", type=str, help="Shop Webhook ID", required=True, location='form')
tenant_delete_args.add_argument(
    "company_id", type=str, help="Company ID", required=True, location='form')
tenant_delete_args.add_argument(
    "callback_id", type=str, help="Fleet Callback ID", required=True, location='form')
