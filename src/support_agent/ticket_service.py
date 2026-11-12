"""In-memory ticket storage for a single service instance."""

from dataclasses import dataclass
from threading import Lock


@dataclass(frozen=True)
class Ticket:
    ticket_id: int
    operation_id: str
    customer_id: str
    subject: str


class TicketService:
    def __init__(self) -> None:
        self._tickets: dict[str, Ticket] = {}
        self._lock = Lock()

    def create_ticket(
        self,
        *,
        operation_id: str,
        customer_id: str,
        subject: str,
    ) -> Ticket:
        with self._lock:
            existing = self._tickets.get(operation_id)
            if existing is not None:
                if (existing.customer_id, existing.subject) != (customer_id, subject):
                    raise ValueError(
                        f"Operation ID {operation_id!r} already has a ticket "
                        "with different request details"
                    )
                return existing

            ticket = Ticket(
                ticket_id=len(self._tickets) + 1,
                operation_id=operation_id,
                customer_id=customer_id,
                subject=subject,
            )
            self._tickets[operation_id] = ticket
            return ticket

    def list_tickets(self) -> tuple[Ticket, ...]:
        with self._lock:
            return tuple(self._tickets.values())
