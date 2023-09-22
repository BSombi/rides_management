# Copyright (c) 2023, Benjamin and contributors
# For license information, please see license.txt

import frappe
from frappe.query_builder.functions import Sum
from frappe.query_builder.functions import Round

def execute(filters=None):
	columns, data = [
		{
			"label": "Make",
			"fieldname": "make",
			"fieldtype": "Data",
			"width": 230,
		},
		{
			"label": "Revenue",
			"fieldname": "revenue",
			"fieldtype": "float",
			"width": 200,
		},
		{
			"label": "Total Hours",
			"fieldname": "total_hours",
			"fieldtype": "float",
			"width": 200,
		},
		{
			"label": "Total Rate per Hour",
			"fieldname": "rate_per_hour",
			"fieldtype": "float",
			"width": 200,
		}
	], []

	ride = frappe.qb.DocType("Ride")
	vehicle = frappe.qb.DocType("Vehicle")

	data = frappe.qb.from_(ride).left_join(vehicle).on(ride.vehicle == vehicle.name).groupby(
		vehicle.make
	).select(vehicle.make,
		  Sum(ride.total_amount).as_('revenue'), 
		  Sum(ride.total_hours).as_('total_hours'), 
		  Round(Sum(ride.rate_per_hour)).as_('rate_per_hour')).run(as_dict=True)

	
	chart = {
			"data": {
				"labels": [d.make for d in data],
				"datasets": [
					{
						"name": "Revenue by Make",
						"values": [d.revenue for d in data]
					},
				]
			},
			"type": "pie"
		}

	return columns, data, None, chart
