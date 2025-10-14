# Copyright (c) 2025, Sanjaa and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase
import frappe.utils


# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]



class TestLibraryTransaction(IntegrationTestCase):


    def setUp(self):
        # setup
        self.member1 = frappe.get_doc({
            "doctype": "Library Member",
            "first_name": "Test1",
            "last_name": "User1",
            "email_address": "testuser1@gmail.com",
            "phone": "11111111"
        }).insert()

        self.member1_membership = frappe.get_doc({
            "doctype": "Library Membership",
            "library_member": self.member1.name,
            "full_name": self.member1.full_name,
            "from_date": frappe.utils.add_days(frappe.utils.today(), -1),
            "to_date": frappe.utils.add_days(frappe.utils.today(), 30),
            "paid": 1,
        }).insert()
        self.member1_membership.submit()
        
        self.member2 = frappe.get_doc({
                "doctype": "Library Member",
                "first_name": "Test2",
                "last_name": "User2",
                "email_address": "testuser2@gmail.com",
                "phone": "11111111"
        }).insert()

        self.member2_membership = frappe.get_doc({
            "doctype": "Library Membership",
            "library_member": self.member2.name,
            "from_date": frappe.utils.add_days(frappe.utils.today(), -1),
            "to_date": frappe.utils.add_days(frappe.utils.today(), 10),
            "paid": 1,
        }).insert()
        self.member2_membership.submit()

        self.book = frappe.get_doc({
            "doctype": "Article",
            "article_name": "Test Book",
            "status": "Available",
            "isbn": "12345"
        }).insert()

    def test_issue_and_return(self):
        # Номын хүсэлт гаргах
        issue = frappe.get_doc({
            "doctype": "Library Transaction",
            "type": "Issue",
            "date": frappe.utils.today(),
            "library_member": self.member1.name,
            "article": self.book.name
        })
        issue.insert()
        issue.submit()

        # хүсэлт гаргасан номд дахин хүсэлт гаргах
        with self.assertRaises(frappe.ValidationError):
            duplicate_issue = frappe.get_doc({
                "doctype": "Library Transaction",
                "type": "Issue",
                "date": frappe.utils.today(),
                "library_member": self.member1.name,
                "article": self.book.name
            })
            duplicate_issue.insert()

        # ном буцаах
        ret = frappe.get_doc({
            "doctype": "Library Transaction",
            "type": "Return",
            "date": frappe.utils.today(),
            "library_member": self.member1.name,
            "article": self.book.name
        })
        ret.insert()
        ret.submit()

        # буцаасан номд дахин хүсэлт гаргах
        issue_again = frappe.get_doc({
            "doctype": "Library Transaction",
            "type": "Issue",
            "date": frappe.utils.today(),
            "library_member": self.member1.name,
            "article": self.book.name
        })
        issue_again.insert()
        issue_again.submit()
                    
    def test_issue_same_article(self):
        issue_one = frappe.get_doc({
            "doctype": "Library Transaction",
            "type": "Issue",
            "date": frappe.utils.today(),
            "library_member": self.member1.name,
            "article": self.book.name
        })
        issue_one.insert()
        issue_one.submit()

        issue_two = frappe.get_doc({
            "doctype": "Library Transaction",
            "type": "Issue",
            "date": frappe.utils.today(),
            "library_member": self.member2.name,
            "article": self.book.name
        })
        issue_two.insert()
        issue_two.submit()