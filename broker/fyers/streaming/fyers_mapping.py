import logging

class FyersExchangeMapper:
    """Maps OpenAlgo exchange codes to Fyers-specific exchange types"""
    
    # Exchange type mapping for Fyers broker
    EXCHANGE_TYPES = {
        'NSE': 'NSE',
        'BSE': 'BSE', 
        'NFO': 'NSE',  # NFO uses NSE in Fyers
        'BFO': 'BSE',  # BFO uses BSE in Fyers
        'MCX': 'MCX',
        'CDS': 'NSE'   # Currency derivatives use NSE
    }
    
    # Fyers uses specific segment codes
    SEGMENT_CODES = {
        'NSE': 10,  # Equity
        'BSE': 10,  # Equity
        'NFO': 11,  # F&O
        'BFO': 11,  # F&O
        'MCX': 20,  # Commodity
        'CDS': 12   # Currency
    }
    
    @staticmethod
    def get_exchange_type(exchange):
        """
        Convert exchange code to Fyers-specific exchange type
        
        Args:
            exchange (str): Exchange code (e.g., 'NSE', 'BSE')
            
        Returns:
            str: Fyers-specific exchange type
        """
        return FyersExchangeMapper.EXCHANGE_TYPES.get(exchange, 'NSE')
    
    @staticmethod
    def get_segment_code(exchange):
        """
        Get Fyers segment code for the exchange
        
        Args:
            exchange (str): Exchange code
            
        Returns:
            int: Segment code
        """
        return FyersExchangeMapper.SEGMENT_CODES.get(exchange, 10)


class FyersCapabilityRegistry:
    """
    Registry of Fyers broker's capabilities including supported exchanges, 
    subscription modes, and market depth levels
    """
    
    # Fyers broker capabilities
    exchanges = ['NSE', 'BSE', 'NFO', 'BFO', 'MCX', 'CDS']
    
    # Fyers subscription modes
    # According to docs: SymbolsData, SymbolsUpdate, Depth
    subscription_modes = [1, 2, 3]  # 1: LTP, 2: Quote, 3: Depth
    
    # Fyers supports market depth for all exchanges
    depth_support = {
        'NSE': [5, 20],   # NSE supports 5 and 20 levels
        'BSE': [5, 20],   # BSE supports 5 and 20 levels  
        'NFO': [5, 20],   # NFO supports 5 and 20 levels
        'BFO': [5, 20],   # BFO supports 5 and 20 levels
        'MCX': [5, 20],   # MCX supports 5 and 20 levels
        'CDS': [5, 20]    # CDS supports 5 and 20 levels
    }
    
    @classmethod
    def get_supported_depth_levels(cls, exchange):
        """
        Get supported depth levels for an exchange
        
        Args:
            exchange (str): Exchange code (e.g., 'NSE', 'BSE')
            
        Returns:
            list: List of supported depth levels (e.g., [5, 20])
        """
        return cls.depth_support.get(exchange, [5])
    
    @classmethod
    def is_depth_level_supported(cls, exchange, depth_level):
        """
        Check if a depth level is supported for the given exchange
        
        Args:
            exchange (str): Exchange code
            depth_level (int): Requested depth level
            
        Returns:
            bool: True if supported, False otherwise
        """
        supported_depths = cls.get_supported_depth_levels(exchange)
        return depth_level in supported_depths
    
    @classmethod
    def get_fallback_depth_level(cls, exchange, requested_depth):
        """
        Get the best available depth level as a fallback
        
        Args:
            exchange (str): Exchange code
            requested_depth (int): Requested depth level
            
        Returns:
            int: Highest supported depth level that is ≤ requested depth
        """
        supported_depths = cls.get_supported_depth_levels(exchange)
        # Find the highest supported depth that's less than or equal to requested depth
        fallbacks = [d for d in supported_depths if d <= requested_depth]
        if fallbacks:
            return max(fallbacks)
        return 5  # Default to basic depth