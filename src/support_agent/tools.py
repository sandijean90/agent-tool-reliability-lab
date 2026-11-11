"""Adapter from the agent's tool arguments to the ticket service."""

from .ticket_service import Ticket, TicketService


class TicketTool:
    def __init__(self, service: TicketService) -> None:
        self._service = service

    def create_ticket(
        self,
        *,
        operation_id: str,
        customer_id: str,
        subject: str,
    ) -> Ticket:
        return self._service.create_ticket(
            operation_id=operation_id,
            customer_id=customer_id,
            subject=subject,
        )
