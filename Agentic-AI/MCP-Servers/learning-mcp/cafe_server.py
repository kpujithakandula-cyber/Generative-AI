from mcp.server import MCPServer
from cafe_data import MENU, COUPONS
from pydantic import BaseModel

mcp = MCPServer(
    "Charminar Cafe",
    instructions = "Order food from charminar cafe in hyderabad, read the menu, place orders, apply coupons and track delivery"
)

ORDERS: dict[str, dict] = {}

@mcp.resource("cafe://menu")
def menu_card() -> str:
    """ The full charminar cafe menu card with prices, veg, non-veg and spice level"""
    lines = ["CHARMINAR CAFE MENU"]
    for name, item in MENU.items():
        tag = "veg" if item["veg"] else "non-veg"
        spice = f"spice {item['spicy']/4}" if item["spicy"] else "mild"
        lines.append(f"{name.title():<20} Rs {item["price"]:>4} {tag:<8} {spice}")
    return "\n".join(lines)


def todays_special() -> str:
    pass

def cafe_policies() -> str:
    pass


@mcp.resource("cafe://order/{order_id}")
def order_reciept(order_id: str) -> str:
    pass

class OrderLine(BaseModel):
    item: str
    quantity: int

class OrderConfirmation(BaseModel):
    order_id: str
    total_rupees: int|float
    eta: str
    message: str


class OrderStatus(BaseModel):
    order_id: str
    status: str
    minutes_left: str


def get_unique_order_id():
    count = len(ORDERS) + 1
    return f"ORDER_{count}"

@mcp.tool()    
def place_order(customer: str, items: list[OrderLine], table_no: str) -> OrderConfirmation:
    order_id = get_unique_order_id()
    total_rupees = 100
    eta = "30 minutes"
    message = "Enjoy the food in our restaurant!"
    confirmation = OrderConfirmation(
        order_id = order_id,
        total_rupees = total_rupees,
        eta = eta,
        message = message
    )

    ORDERS[order_id] = confirmation.dict()
    return confirmation

@mcp.tool()
def apply_coupon(order_id: str, code: str) -> OrderConfirmation:
    pass

@mcp.tool()
def track_order(order_id: str) -> OrderStatus:
    pass


@mcp.prompt(title = "Daily sales summary")
def daily_summary() -> str:
    if not ORDERS:
        return "No orders placed so far."
    total = sum(ORDERS[order_id]['total_rupees'] for order_id in ORDERS)
    return f"Sales so far today in the restaurant is {total} rupees"


if __name__ == "__main__":
    mcp.run("streamable-http", host="localhost", port=9000)