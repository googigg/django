import boto3
import traceback

from boto3.dynamodb.conditions import Attr
from boto3.dynamodb.conditions import Key
class DynamodbUtil():
	dynamodb = boto3.resource('dynamodb',region_name='ap-southeast-1')

	def create(self, table_name, data, batch=False):
		"""
		data = [{
			"<key_id>" : "<key_value>",
			"<attr_1>" : "<attr_value_1>",
			"<attr_2>" : "<attr_value_2>",
			"<attr_3>" : "<attr_value_3>",
			"<attr_4>" : "<attr_value_4>",
		}]
		"""

		return_response = {}
		return_response_data = []
		success_flag = False
		try:
			table = self.dynamodb.Table(table_name)
			if not batch:
				for item in data:
					response_item = {}
					res = table.put_item(Item=item)
					if res['ResponseMetadata']['HTTPStatusCode'] == 200:
						success_flag = True
						response_item["response_code"] = '20000'
						response_item["response_desc"] = 'Success'
						response_item["response_data"] = item
						return_response_data.append(response_item)
					else:
						success_flag = False
						response_item["response_code"] = '22000'
						response_item["response_desc"] = 'HTTPStatusCode {}'.format(res['ResponseMetadata']['HTTPStatusCode'])
						return_response_data.append(response_item)
			else:
				with table.batch_writer() as batch:
					for item in data:
						batch.put_item(Item=item)

			if success_flag:
				return_response['response_code'] = '20000'
				return_response['response_desc'] = 'Success'
				return_response['response_data'] = return_response_data
				
			else:
				return_response['response_code'] = '22000'
				return_response['response_desc'] = 'Fail Create data'
				return_response['response_data'] = return_response_data

		except Exception as e:
			traceback.print_exc()
			return_response['response_code'] = '22000'
			return_response['response_desc'] = 'Exception {}'.format(e)

		return return_response

	def get_item(self, table_name, query_item):
		"""
		{'<key_id>':'<key_value>'}
		"""

		return_response_data = []
		return_response = {}

		try:
			table = self.dynamodb.Table(table_name)
			response = table.get_item(
				Key=query_item
			)
			if response['ResponseMetadata']['HTTPStatusCode'] == 200:
				return_response['response_code'] = '20000'
				return_response['response_desc'] = 'Success'
				return_response['response_data'] = return_response_data.append(response['Item'])
			else:
				return_response_data['response_code'] = '22000'
				return_response_data['response_desc'] = 'HTTPStatusCode {}'.format(res['ResponseMetadata']['HTTPStatusCode'])
		except Exception as e:
			traceback.print_exc()
			return_response['response_code'] = '22000'
			return_response['response_desc'] = 'Exception {}'.format(e)

		return return_response

	def update(self, table_name, data):
		"""
		data = {
			"data" : [{
				"key" : {
					"<key_id>" : "<key_value>"
				},
				"update_data" : {
					"<attr_1>" : "<attr_value_1>",
					"<attr_2>" : "<attr_value_2>",
					"<attr_3>" : "<attr_value_3>",
					"<attr_4>" : "<attr_value_4>",
				}
			}]
		}
		"""

		return_response = {}
		return_response_data = []
		success_flag = False

		table = self.dynamodb.Table(table_name)

		for updated_dict in data["data"]:
			key_dict = updated_dict["key"]
			update_expr = "SET "
			expression_attribute_values = {}
			for update_key in updated_dict['update_data'].keys():
				if update_expr != "SET ":
					update_expr = update_expr+", "

				expression_key = ":{}".format(update_key)
				update_expr = update_expr+ '{} = {}'.format(update_key,expression_key)

				expression_attribute_values[expression_key] = updated_dict['update_data'][update_key]

			response = table.update_item(
				Key=key_dict,
				UpdateExpression=update_expr,
				ExpressionAttributeValues=expression_attribute_values
			)

			response_item = {}

			if response['ResponseMetadata']['HTTPStatusCode'] == 200:
				success_flag = True
				response_item['response_code'] = '20000'
				response_item['response_desc'] = 'Success'
				response_item["response_data"] = updated_dict
				return_response_data.append(response_item)
			else:
				success_flag = False
				response_item['response_code'] = '22000'
				response_item['response_desc'] = 'HTTPStatusCode {}'.format(response['ResponseMetadata']['HTTPStatusCode'])
				return_response_data.append(response_item)

		if success_flag:
			return_response['response_code'] = '20000'
			return_response['response_desc'] = 'Success'
			return_response['response_data'] = return_response_data
			
		else:
			return_response['response_code'] = '22000'
			return_response['response_desc'] = 'Fail Create data'
			return_response['response_data'] = return_response_data

		return return_response

	def delete(self, table_name, item_key):
		"""
		item_key = [{
			"<key_id>" : "<key_value>"
		}]
		"""
		return_response = {}
		table = self.dynamodb.Table(table_name)
		for item_key_data in item_key:
			response = table.delete_item(
				Key=item_key_data
			)
			if response['ResponseMetadata']['HTTPStatusCode'] == 200:
				return_response['response_code'] = '20000'
				return_response['response_desc'] = 'Success'
			else:
				return_response['response_code'] = '22000'
				return_response['response_desc'] = 'HTTPStatusCode {}'.format(response['ResponseMetadata']['HTTPStatusCode'])

		return return_response


	def search(self, table_name, filter_expression, expression_attribute_values, total_items=None, start_key=None, table=None, use_scan=False, index_name=None):
		if not use_scan:
			res = self.query_item(table_name, filter_expression, expression_attribute_values, total_items=total_items, start_key=start_key, table=table, index_name=index_name)
		else:
			res = self.scan_item(table_name, filter_expression, expression_attribute_values, total_items=total_items, start_key=start_key, table=table)
		return res


	def query_item(self, table_name, filter_expression, expression_attribute_values, index_name=None, total_items=None, start_key=None, table=None):
		"""
			primary_key={
				'name':'<primary-key-name>',
				'value':'<primary-key-value>'
			}
			sort_key={
				'name':'<sort-key-name>',
				'value':'<sort-key-value>'
			}
		"""

		"""
		FilterExpression="enterprise_role_id = :enterprise_role_id_1_value1"
		ExpressionAttributeValues={":enterprise_role_id": "1"})

		"""

		return_response = {}
		if not table:
			table = self.dynamodb.Table(table_name)
		
		if not start_key:
			response = table.query(
				KeyConditionExpression=filter_expression,
				ExpressionAttributeValues=expression_attribute_values
			)
		else:
			response = table.query(
				KeyConditionExpression=filter_expression,
				ExclusiveStartKey=start_key,
				ExpressionAttributeValues=expression_attribute_values
			)

		if not total_items:
			total_items = response['Items']
		else:
			total_items.extend(response['Items'])

		if response.get('LastEvaluatedKey'):
			start_key = response['LastEvaluatedKey']
			return_items = self.query_item(
				table_name=table_name, filter_expression=filter_expression,
				expression_attribute_values=expression_attribute_values, total_items=total_items,
				start_key=start_key, table=table
			)
			return return_items
		else:
			return_response['response_code'] = '20000'
			return_response['response_desc'] = 'Success'
			return_response['response_data'] = total_items
			return return_response

	# def query_item(self, table_name, primary_key, sort_key=None, index_name=None, total_items=None, start_key=None, table=None):
	# 	"""
	# 		primary_key={
	# 			'name':'<primary-key-name>',
	# 			'value':'<primary-key-value>'
	# 		}
	# 		sort_key={
	# 			'name':'<sort-key-name>',
	# 			'value':'<sort-key-value>'
	# 		}
	# 	"""

	# 	"""
	# 	FilterExpression="enterprise_role_id = :enterprise_role_id_1_value1"
	# 	ExpressionAttributeValues={":enterprise_role_id": "1"})

	# 	"""

	# 	return_response = {}
	# 	if not table:
	# 		table = self.dynamodb.Table(table_name)

	# 	pk = primary_key['name']
	# 	pkv = primary_key['value']
		
	# 	if not start_key:
	# 		if index_name:
	# 			if sort_key:
	# 				sk = sort_key['name']
	# 				skv = sort_key['value']
	# 				response = table.query(IndexName=index_name, KeyConditionExpression=Key(sk).eq(skv) & Key(pk).eq(pkv))
	# 			else:
	# 				response = table.query(IndexName=index_name, KeyConditionExpression=Key(pk).eq(pkv))
	# 		else:
	# 			if sort_key:
	# 				sk = sort_key['name']
	# 				skv = sort_key['value']
	# 				response = table.query(KeyConditionExpression=Key(sk).eq(skv) & Key(pk).eq(pkv))
	# 			else:
	# 				response = table.query(KeyConditionExpression=Key(pk).eq(pkv))
	# 	else:
	# 		if index_name:
	# 			if sort_key:
	# 				sk = sort_key['name']
	# 				skv = sort_key['value']
	# 				response = table.query(IndexName=index_name, KeyConditionExpression=Key(sk).eq(skv) & Key(pk).eq(pkv), ExclusiveStartKey=start_key)
	# 			else:
	# 				response = table.query(IndexName=index_name, KeyConditionExpression=Key(pk).eq(pkv), ExclusiveStartKey=start_key)

	# 		else:
	# 			if sort_key:
	# 				sk = sort_key['name']
	# 				skv = sort_key['value']
	# 				response = table.query(KeyConditionExpression=Key(sk).eq(skv) & Key(pk).eq(pkv), ExclusiveStartKey=start_key)
	# 			else:
	# 				response = table.query(KeyConditionExpression=Key(pk).eq(pkv), ExclusiveStartKey=start_key)

	# 	if not total_items:
	# 		total_items = response['Items']
	# 	else:
	# 		total_items.extend(response['Items'])

	# 	if response.get('LastEvaluatedKey'):
	# 		start_key = response['LastEvaluatedKey']
	# 		return_items = self.query_item(
	# 			table_name=table_name, sort_key=sort_key,
	# 			primary_key=primary_key, total_items=total_items,
	# 			start_key=start_key, table=table
	# 		)
	# 		return return_items
	# 	else:
	# 		return_response['response_code'] = '20000'
	# 		return_response['response_desc'] = 'Success'
	# 		return_response['response_data'] = total_items
	# 		return return_response

	def scan_item(self, table_name, filter_expression, expression_attribute_values, total_items=None, start_key=None, table=None):
		"""
		FilterExpression="enterprise_role_id = :enterprise_role_id_1_value1"
		ExpressionAttributeValues={":enterprise_role_id": "1"})

		"""
		return_response = {}
		if not table:
			table = self.dynamodb.Table(table_name)

		if not start_key:
			response = table.scan(
				FilterExpression=filter_expression,
				ExpressionAttributeValues=expression_attribute_values
			)
		else:
			response = table.scan(
				FilterExpression=filter_expression,
				ExclusiveStartKey=start_key,
				ExpressionAttributeValues=expression_attribute_values
			)
		if not total_items:
			total_items = response['Items']
		else:
			total_items.extend(response['Items'])
		if response.get('LastEvaluatedKey'):
			start_key = response['LastEvaluatedKey']
			return_items = self.query_item(
				table_name=table_name, filter_expression=filter_expression,
				expression_attribute_values=expression_attribute_values, total_items=total_items,
				start_key=start_key, table=table
			)
			return return_items
		else:
			return_response['response_code'] = '20000'
			return_response['response_desc'] = 'Success'
			return_response['response_data'] = total_items
			return return_response



# example request
dynamo = DynamodbUtil()

#r = dynamo.create('18_enterprise_role_hierarchy',[{'enterprise_role_id':'3','enterprise_role_id_1':'123456'}])
#print(r)

# in develope
#r = dynamo.get_item('18_enterprise_role_hierarchy',{'enterprise_role_id':'3'})
#print(r)


# data = {
# 			"data" : [{
# 				"key" : {
# 					"enterprise_role_id" : "3"
# 				},
# 				"update_data" : {
# 					"enterprise_role_id_1" : "78888"
# 				}
# 			}]
# 		}
# r = dynamo.update('18_enterprise_role_hierarchy',data)
# print(r)


# data = [{"enterprise_role_id" : "3"}]
# r = dynamo.delete('18_enterprise_role_hierarchy',data)
# print(r)


# filter_expression = "enterprise_role_id = :enterprise_role_id_1_value1"
# expression_attribute_values = {":enterprise_role_id_1_value1": "1"}
# r = dynamo.search('18_enterprise_role_hierarchy', filter_expression, expression_attribute_values)
# print(r)

filter_expression = "enterprise_role_id_1 = :enterprise_role_id_1_value1 OR contains(enterprise_role_id_1, :enterprise_role_id_1_value2)"
expression_attribute_values = {":enterprise_role_id_1_value1": "123456",":enterprise_role_id_1_value2": "12"}
r = dynamo.search('18_enterprise_role_hierarchy', filter_expression, expression_attribute_values, use_scan=True)
print(r)

#response
# {'response_code': '20000', 'response_desc': 'Success', 'response_data': [{'response_code': '20000', 'response_desc': 'Success', 'response_data': {'enterprise_role_id_1': '123456', 'enterprise_role_id': '3'}}]}
# {'response_code': '20000', 'response_desc': 'Success', 'response_data': None}
# {'response_code': '20000', 'response_desc': 'Success', 'response_data': [{'response_code': '20000', 'response_desc': 'Success', 'response_data': {'key': {'enterprise_role_id': '3'}, 'update_data': {'enterprise_role_id_1': '777777'}}}]}
# {'response_code': '20000', 'response_desc': 'Success'}
# {'response_code': '20000', 'response_desc': 'Success', 'response_data': [{'enterprise_role_id_1': '123456', 'enterprise_role_id': '1'}]}
# {'response_code': '20000', 'response_desc': 'Success', 'response_data': [{'enterprise_role_id_1': '123456', 'enterprise_role_id': '2'}, {'enterprise_role_id_1': '123456', 'enterprise_role_id': '1'}]}