import unittest

from support_agent.agent import SupportAgent
from support_agent.ticket_service import Ticket, TicketService
from support_agent.tools import TicketTool


class DropFirstResponseTool(TicketTool):
    """Simulate a lost response after the first successful write."""

    def __init__(self, service: TicketService) -> None:
        super().__init__(service)
        self.attempt_operation_ids: list[str] = []
        self.first_committed_ticket: Ticket | None = None

    def create_ticket(
        self,
        *,
        operation_id: str,
        customer_id: str,
        subject: str,
    ) -> Ticket:
        self.attempt_operation_ids.append(operation_id)
        ticket = super().create_ticket(
            operation_id=operation_id,
            customer_id=customer_id,
            subject=subject,
        )
        if len(self.attempt_operation_ids) == 1:
            self.first_committed_ticket = ticket
            raise TimeoutError("Ticket response was lost after creation")
        return ticket


class RetryBehaviorTests(unittest.TestCase):
    def test_retry_after_lost_response_creates_one_ticket(self) -> None:
        service = TicketService()
        tool = DropFirstResponseTool(service)
        agent = SupportAgent(tool)

        ticket = agent.open_ticket(
            operation_id="request-104",
            customer_id="customer-1",
            subject="Cannot sign in",
        )

        self.assertEqual(tool.attempt_operation_ids, ["request-104", "request-104"])
        self.assertIsNotNone(tool.first_committed_ticket)
        stored_tickets = service.list_tickets()
        self.assertEqual(
            len(stored_tickets),
            1,
            f"Expected one stored ticket after retry, got {stored_tickets!r}",
        )
        self.assertEqual(ticket, tool.first_committed_ticket)
        self.assertEqual(stored_tickets, (ticket,))
