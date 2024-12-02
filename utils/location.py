class Location:
    def __init__(self, x, y):
        """        
        Args:
            x (int): The x-coordinate.
            y (int): The y-coordinate.
        
        Raises:
            ValueError: If x or y is not an integer.
        """
        if not isinstance(x, int) or not isinstance(y, int):
            raise ValueError("Both x and y must be integers.")
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y
    
    def __repr__(self):
        return f"location x:{self.x}, y:{self.y}"