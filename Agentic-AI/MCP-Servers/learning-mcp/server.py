from mcp.server import MCPServer


# mcp server
mcp = MCPServer("hello-mcp")

@mcp.tool()
def add(a: int, b: int) -> int:
    """ This will add two numbers and return the result.

    Args:
        a (int): The first number.
        b (int): The second number.
    Result:
        int: The sum of the two numbers.

    """
    return a + b
@mcp.tool()
def sub(a: int, b: int) -> int:
    """ This function does the subtracction between two numbers, subtracting one number from another number and gives the result.

    Args:
        a (int): First number
        b (int): Second number
    Result:
        int: The sub of the two nums.
    """
    return a - b
@mcp.tool()
def mul(a: int, b: int) -> int:
	""" This function does the multiplication of two numbers and gives the result 
	
	Args:
		a (int): First number
		b (int): Second number

	Result:
		int: Multiplication of two numbers
	"""
	return a * b
@mcp.tool()
def div(a: int, b: int) -> float:
	""" This function does the division of two numbers and gives the result.

	Args:
		a(int): First number
		b(int): Second number
	
	Result:
		int: Division of two numbers
	"""
	return a / b
@mcp.tool()
def modulus(a: int, b: int) -> float:
	""" This function does the modulus of two numbers.

	Args:
		a(int): First number
		b(int): Second number

	Result: 
		int: Modulus of two numbers
	"""
	return a % b

if __name__ == "__main__":
    mcp.run(transport = "stdio")