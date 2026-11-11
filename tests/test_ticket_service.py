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
