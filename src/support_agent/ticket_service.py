"""In-memory ticket storage for a single service instance."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Ticket:
    ticket_id: int
    operation_id: str
    customer_id: str
    subject: str


class TicketService:
    def __init__(self) -> None:
        self._tickets: list[Ticket] = []

    def create_ticket(
        self,
        *,
        operation_id: str,
        customer_id: str,
        subject: str,
    ) -> Ticket:
        ticket = Ticket(
            ticket_id=len(self._tickets) + 1,
            operation_id=operation_id,
            customer_id=customer_id,
            subject=subject,
        )
        self._tickets.append(ticket)
        return ticket

    def list_tickets(self) -> tuple[Ticket, ...]:
        return tuple(self._tickets)
