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
        self._tickets_by_operation: dict[str, Ticket] = {}

    def create_ticket(
        self,
        *,
        operation_id: str,
        customer_id: str,
        subject: str,
    ) -> Ticket:
        """Create or replay a ticket, raising ValueError for conflicting details."""
        existing = self._tickets_by_operation.get(operation_id)
        if existing is not None:
            if existing.customer_id != customer_id or existing.subject != subject:
                raise ValueError(f"Operation {operation_id!r} already has different ticket details")
            return existing

        ticket = Ticket(
            ticket_id=len(self._tickets_by_operation) + 1,
            operation_id=operation_id,
            customer_id=customer_id,
            subject=subject,
        )
        self._tickets_by_operation[operation_id] = ticket
        return ticket

    def list_tickets(self) -> tuple[Ticket, ...]:
        return tuple(self._tickets_by_operation.values())
