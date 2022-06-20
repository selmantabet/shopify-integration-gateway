import json


payload = {
    'transportTypeId': 1, 'amountToBeCollected': 0.0, 'taskItems': [{'name': 'Test Product 1', 'quantity': 1, 'price': '100.00'}],
    'pickupByUtc': '2022-06-19T20:19:01.278745', 'deliverByUtc': '2022-06-19T21:19:01.278745', 'pickup': {'Address': '12282 King Abdulaziz Road, Al Mouroj \n ', 'Name': '12282 King Abdulaziz Road, Al Mouroj', 'PhoneNumber': '+97433693992', 'Latitude': '25.3138126', 'Longitude': '51.4408446'},
    'delivery': {
        'Address': 'Building 41, Street 312, Zone 69 \n Apartment C-208, AlAsmakh Residency', 'Name': 'Selmane Tabet', 'PhoneNumber': '974-3369-3992', 'Latitude': 25.2676538, 'Longitude': 51.5357698},
    'priority': 5, 'canGroupTask': True, 'pickupLocationTypeId': 2, 'deliveryLocationTypeId': 2, 'userMetaDataDtos': [{'key': 'order_id', 'value': 4782091829501}, {'key': 'fulfillment_id', 'value': 4298889232637},
                                                                                                                      {'key': 'merchant_url', 'value': 'https://chaoscodes.myshopify.com'}], 'clientGeneratedId': 4782091829501}
print(json.dumps(payload))
