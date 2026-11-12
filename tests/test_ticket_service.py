import unittest

from support_agent.agent import SupportAgent
from support_agent.ticket_service import Ticket, TicketService
from support_agent.tools import TicketTool


class TicketServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = TicketService()

    def test_create_ticket_persists_request_fields(self) -> None:
        ticket = self.service.create_ticket(
            operation_id="request-1",
            customer_id="customer-1",
            subject="Cannot sign in",
        )

        self.assertEqual(
            ticket,
            Ticket(
                ticket_id=1,
                operation_id="request-1",
                customer_id="customer-1",
                subject="Cannot sign in",
            ),
        )
        self.assertEqual(self.service.list_tickets(), (ticket,))

    def test_identical_request_returns_original_ticket(self) -> None:
        request = {
            "operation_id": "request-1",
            "customer_id": "customer-1",
            "subject": "Cannot sign in",
        }
        original = self.service.create_ticket(**request)

        replay = self.service.create_ticket(**request)

        self.assertIs(replay, original)
        self.assertEqual(self.service.list_tickets(), (original,))

    def test_conflicting_request_preserves_stored_tickets(self) -> None:
        request = {
            "operation_id": "request-1",
            "customer_id": "customer-1",
            "subject": "Cannot sign in",
        }
        original = self.service.create_ticket(**request)
        other_request = {**request, "operation_id": "request-2"}
        other = self.service.create_ticket(**other_request)
        for field, value in (
            ("customer_id", "customer-2"),
            ("subject", "Cannot reset password"),
        ):
            with self.subTest(field=field):
                conflicting_request = {**request, field: value}
                with self.assertRaisesRegex(
                    ValueError, "request-1.*different request details"
                ):
                    self.service.create_ticket(**conflicting_request)
                self.assertEqual(self.service.list_tickets(), (original, other))
                self.assertIs(self.service.create_ticket(**request), original)

    def test_distinct_operations_create_distinct_tickets(self) -> None:
        agent = SupportAgent(TicketTool(self.service))
        first = agent.open_ticket(
            operation_id="request-1",
            customer_id="customer-1",
            subject="Cannot sign in",
        )
        second = agent.open_ticket(
            operation_id="request-2",
            customer_id="customer-1",
            subject="Cannot sign in",
        )

        self.assertNotEqual(first.ticket_id, second.ticket_id)
        self.assertEqual(self.service.list_tickets(), (first, second))
