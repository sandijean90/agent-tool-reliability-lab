"""Invoke the ticket tool and retry once on a timeout."""

from .ticket_service import Ticket
from .tools import TicketTool


class SupportAgent:
    def __init__(self, ticket_tool: TicketTool) -> None:
        self._ticket_tool = ticket_tool

    def open_ticket(
        self,
        *,
        operation_id: str,
        customer_id: str,
        subject: str,
    ) -> Ticket:
        # The caller supplies one operation ID per logical request.
        try:
            return self._ticket_tool.create_ticket(
                operation_id=operation_id,
                customer_id=customer_id,
                subject=subject,
            )
        except TimeoutError:
            return self._ticket_tool.create_ticket(
                operation_id=operation_id,
                customer_id=customer_id,
                subject=subject,
            )
