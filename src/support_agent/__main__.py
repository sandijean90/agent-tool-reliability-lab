"""Run the service ticket creation demo."""

from .agent import SupportAgent
from .ticket_service import TicketService
from .tools import TicketTool


if __name__ == "__main__":
    service = TicketService()
    agent = SupportAgent(TicketTool(service))
    ticket = agent.open_ticket(
        operation_id="request-1",
        customer_id="customer-1",
        subject="Cannot sign in",
    )
    print(ticket)
