# Copyright (c) 2023, Benjamin and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class Ride(Document):
	def before_save(self):
         cost_breakup = self.cost_breakup
         total_hours = 0
         for item in cost_breakup:
          total_hours += item.hours

          self.total_hours = total_hours

         total_amount = 0
         for item in cost_breakup:
          total_amount += item.amount

         self.total_amount = total_amount

         rate_per_hour = total_amount/total_hours

         self.rate_per_hour = rate_per_hour
