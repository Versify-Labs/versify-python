# from aws_lambda_powertools import Logger, Tracer
# from aws_lambda_powertools.utilities.data_classes import (EventBridgeEvent,
#                                                           event_source)
# from versify.utilities.model import response

# from .service import WalletService

# tracer = Tracer()
# logger = Logger()


# @event_source(data_class=EventBridgeEvent)
# @logger.inject_lambda_context(log_event=True)
# @tracer.capture_lambda_handler
# def on_merchant_order(event, context):
#     merchant_order = event.detail
#     email = merchant_order['email']
#     items = merchant_order['items']
#     merchant = merchant_order['merchant_details']

#     # Iniit service with customers email
#     service = WalletService(email)

#     # Create order
#     order = service.create_order(merchant_order)

#     # Create an asset for each item in order
#     for item in items:
#         product = item['product_details']
#         service.create_asset(
#             attributes=product['attributes'],
#             collection={'id': product['collection']},
#             description=product['description'],
#             image=product['images'][0],
#             merchant={'id': merchant_order['merchant'], **merchant},
#             name=product['name'],
#             order={'id': order.id},
#             product={'id': product['id']},
#             quantity=item['quantity']
#         )

#     return response('create', order.to_dict())
